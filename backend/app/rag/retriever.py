import os
import json
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGRetriever:
    """
    Offline TF-IDF Knowledge Retrieval Engine for safety guidelines & citations.
    """

    def __init__(self, kb_path: Optional[str] = None):
        if kb_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            kb_path = os.path.join(base_dir, "knowledge_base.json")
        
        self.kb_path = kb_path
        self.chunks = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        if not os.path.exists(self.kb_path):
            print(f"[RAG Warning] Knowledge base file not found at {self.kb_path}")
            return

        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        # Build corpus
        corpus = [
            f"{c['title']} {c['content']} {' '.join(c.get('tags', []))} {c.get('actionable_guidance', '')} {c.get('category', '')}"
            for c in self.chunks
        ]

        if corpus:
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                sublinear_tf=True,
                stop_words="english"
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def retrieve(
        self,
        query: str,
        category: Optional[str] = None,
        top_k: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most relevant knowledge citations for a given query and category context.
        """
        if not self.chunks or self.vectorizer is None or not query.strip():
            return []

        # Vectorize query
        query_vec = self.vectorizer.transform([query])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        scored_results = []
        for idx, score in enumerate(sim_scores):
            chunk = self.chunks[idx]
            boost = 0.0

            # Boost if matching detected scam category or general helpline
            if category and chunk.get("category") == category:
                boost += 0.20
            elif chunk.get("category") == "general":
                boost += 0.10

            final_score = float(score + boost)
            scored_results.append((final_score, chunk))

        # Sort descending by score
        scored_results.sort(key=lambda x: x[0], reverse=True)

        citations = []
        for score, chunk in scored_results[:top_k]:
            citations.append({
                "title": chunk["title"],
                "content": chunk["content"],
                "source": chunk["source"],
                "actionable_guidance": chunk.get("actionable_guidance", ""),
                "relevance_score": round(score, 3)
            })

        return citations

rag_retriever = RAGRetriever()
