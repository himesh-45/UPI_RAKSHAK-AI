import os
import re
import json
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGRetriever:
    """
    Multilingual Subword Character N-Gram TF-IDF Knowledge Retrieval Engine.
    Filters strictly for reviewed knowledge entries (suppressing unreviewed drafts),
    indexes English, Hindi, and Telugu representations, and returns ranked citations
    with statutory official URLs and review attributions.
    """

    FALLBACK_RESPONSES = {
        "en": "I'm not sure based on verified guidance. Please check https://cybercrime.gov.in or call the 1930 national helpline for assistance.",
        "hi": "सत्यापित दिशानिर्देशों के आधार पर मुझे पूरी जानकारी नहीं है। कृपया https://cybercrime.gov.in देखें या राष्ट्रीय हेल्पलाइन 1930 पर कॉल करें।",
        "te": "ధృవీకరించబడిన మార్గదర్శకాల ప్రకారం నాకు పూర్తి సమాచారం లేదు. దయచేసి https://cybercrime.gov.in చూడండి లేదా జాతీయ హెల్ప్‌లైన్ 1930 కు కాల్ చేయండి."
    }

    def __init__(self, kb_path: Optional[str] = None):
        if kb_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            kb_path = os.path.join(base_dir, "knowledge_base.json")
        
        self.kb_path = kb_path
        self.chunks: List[Dict[str, Any]] = []
        self.draft_chunks: List[Dict[str, Any]] = []
        self.total_raw_chunks: int = 0
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        if not os.path.exists(self.kb_path):
            print(f"[RAG Warning] Knowledge base file not found at {self.kb_path}")
            return

        with open(self.kb_path, "r", encoding="utf-8") as f:
            raw_entries = json.load(f)

        self.total_raw_chunks = len(raw_entries)
        # Strict isolation: Only reviewed entries are available for retrieval
        self.chunks = [e for e in raw_entries if e.get("status") == "reviewed"]
        self.draft_chunks = [e for e in raw_entries if e.get("status") == "draft"]

        # Build multilingual corpus
        corpus = []
        for c in self.chunks:
            tags_str = " ".join(c.get("tags", []))
            text_parts = [
                c.get("title", ""),
                c.get("content", ""),
                c.get("en", ""),
                c.get("hi", ""),
                c.get("te", ""),
                tags_str,
                c.get("actionable_guidance", ""),
                c.get("category", "")
            ]
            corpus.append(" ".join(filter(None, text_parts)))

        if corpus:
            # Subword character n-grams handle English, Hindi, and Telugu scripts effectively
            self.vectorizer = TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 5),
                sublinear_tf=True,
                min_df=1
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def retrieve(
        self,
        query: str,
        category: Optional[str] = None,
        top_k: int = 2,
        min_score: float = 0.05
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most relevant reviewed knowledge citations for a given query.
        Returns empty list if top score falls below min_score (triggering conservative fallback).
        """
        if not self.chunks or self.vectorizer is None or not query.strip():
            return []

        # Vectorize query
        query_vec = self.vectorizer.transform([query])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        query_lower = query.lower()
        query_tokens = set(re.findall(r"\w+", query_lower))

        STOP_WORDS = {
            "how", "to", "what", "is", "a", "an", "the", "in", "on", "of", "and",
            "or", "for", "with", "do", "i", "my", "your", "this", "that", "it",
            "at", "by", "from", "be", "as", "are", "was", "were", "can", "you", "kb"
        }

        scored_results = []
        for idx, score in enumerate(sim_scores):
            chunk = self.chunks[idx]
            boost = 0.0

            # Only apply category or token boosts if there is meaningful base similarity
            if score > 0.03:
                # Boost if matching detected scam category or general helpline
                if category and chunk.get("category") == category:
                    boost += 0.15
                elif chunk.get("category") == "general" or chunk.get("category") == "helpline":
                    boost += 0.05

                # Direct domain token match boost (ignoring stopwords)
                c_tags = set(t.lower() for t in chunk.get("tags", [])) - STOP_WORDS
                c_id_tokens = set(chunk.get("id", "").lower().split("_")) - STOP_WORDS
                matches = (query_tokens - STOP_WORDS).intersection(c_tags | c_id_tokens)
                if matches:
                    boost += min(0.15, len(matches) * 0.05)

                if "1930" in query_lower and ("1930" in chunk.get("title", "") or "1930" in chunk.get("id", "") or "1930" in c_tags):
                    boost += 0.20

            final_score = float(score + boost)
            scored_results.append((final_score, chunk))

        # Sort descending by score
        scored_results.sort(key=lambda x: x[0], reverse=True)

        # Check if the highest score satisfies minimum confidence threshold
        if not scored_results or scored_results[0][0] < min_score:
            return []

        citations = []
        for score, chunk in scored_results[:top_k]:
            if score < min_score:
                continue
            citations.append({
                "id": chunk.get("id", ""),
                "title": chunk.get("title", ""),
                "content": chunk.get("content", ""),
                "en": chunk.get("en", chunk.get("content", "")),
                "hi": chunk.get("hi", ""),
                "te": chunk.get("te", ""),
                "source": chunk.get("source", ""),
                "official_source_link": chunk.get("official_source_link") or chunk.get("official_url") or "https://cybercrime.gov.in",
                "actionable_guidance": chunk.get("actionable_guidance", ""),
                "last_reviewed": chunk.get("last_reviewed", "2026-11-23"),
                "reviewer": chunk.get("reviewer", "Regulatory Compliance Audit"),
                "status": chunk.get("status", "reviewed"),
                "relevance_score": round(score, 3)
            })

        return citations

    def get_fallback_message(self, language: str = "en") -> str:
        """Returns the conservative fallback message in the requested language."""
        lang_code = language.lower()[:2]
        return self.FALLBACK_RESPONSES.get(lang_code, self.FALLBACK_RESPONSES["en"])


rag_retriever = RAGRetriever()
