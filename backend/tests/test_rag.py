import pytest
from backend.app.rag.retriever import rag_retriever


def test_rag_retrieval_collect_request():
    query = "Sender asking to accept collect request and enter UPI PIN to receive cashback"
    citations = rag_retriever.retrieve(query, category="fake_upi_refund_cashback", top_k=2)

    assert len(citations) >= 1
    top_citation = citations[0]
    assert "Receiving" in top_citation["title"] or "PIN" in top_citation["title"]
    assert "NPCI" in top_citation["source"]
    assert "collect" in top_citation["actionable_guidance"].lower()


def test_rag_retrieval_electricity_bill():
    query = "Electricity line will be disconnected tonight at 9:30 PM due to unpaid bill"
    citations = rag_retriever.retrieve(query, category="electricity_disconnection", top_k=2)

    assert len(citations) >= 1
    assert any("Electricity" in c["title"] for c in citations)


def test_rag_retrieval_helpline():
    query = "I shared my OTP and lost money where do I report fraud immediately"
    citations = rag_retriever.retrieve(query, top_k=2)

    assert len(citations) >= 1
    assert any("1930" in c["title"] or "1930" in c["content"] or "1930" in c.get("en", "") for c in citations)


def test_rag_empty_query():
    citations = rag_retriever.retrieve("", top_k=2)
    assert citations == []


def test_rag_knowledge_base_size_and_draft_isolation():
    """Verify that KB has 150+ entries and draft entries are strictly excluded from retrieval."""
    assert rag_retriever.total_raw_chunks >= 150
    assert len(rag_retriever.draft_chunks) >= 2
    # All loaded chunks must have status == 'reviewed'
    assert len(rag_retriever.chunks) >= 150
    assert all(c.get("status") == "reviewed" for c in rag_retriever.chunks)
    assert all(c.get("status") != "draft" for c in rag_retriever.chunks)

    # Retrieval must never return a draft item
    citations = rag_retriever.retrieve("experimental telecom AI voice deepfake sandbox", top_k=5)
    for cit in citations:
        assert cit.get("status") == "reviewed"
        assert "draft" not in cit.get("id", "")


def test_rag_multilingual_hindi_retrieval():
    """Verify high-precision retrieval on Hindi Devanagari queries."""
    query = "1930 पर साइबर फ्रॉड की शिकायत कैसे दर्ज करें और क्या दस्तावेज चाहिए"
    citations = rag_retriever.retrieve(query, top_k=2)

    assert len(citations) >= 1
    top = citations[0]
    assert top["status"] == "reviewed"
    assert top["official_source_link"].startswith("http")
    assert "1930" in top["title"] or "1930" in top["content"] or "1930" in top.get("hi", "")


def test_rag_multilingual_telugu_retrieval():
    """Verify high-precision retrieval on Telugu queries."""
    query = "డిజిటల్ అరెస్ట్ అంటే ఏమిటి పోలీసులు వీడియో కాల్ చేస్తారా"
    citations = rag_retriever.retrieve(query, top_k=2)

    assert len(citations) >= 1
    top = citations[0]
    assert top["status"] == "reviewed"
    assert "digital_arrest" in top.get("id", "") or "Digital Arrest" in top["title"] or "పోలీస్" in top.get("te", "")


def test_rag_unrelated_query_conservative_fallback():
    """Completely unrelated queries should return empty citations to prevent hallucinated guidance."""
    unrelated_query = "how to bake sourdough bread with olive oil and yeast recipe"
    citations = rag_retriever.retrieve(unrelated_query, min_score=0.15)
    assert citations == []

    # Verify fallback message formats in en, hi, te
    en_msg = rag_retriever.get_fallback_message("en")
    hi_msg = rag_retriever.get_fallback_message("hi")
    te_msg = rag_retriever.get_fallback_message("te")

    assert "1930" in en_msg and "cybercrime.gov.in" in en_msg
    assert "1930" in hi_msg and "cybercrime.gov.in" in hi_msg
    assert "1930" in te_msg and "cybercrime.gov.in" in te_msg


def test_rag_statutory_and_review_metadata():
    """Verify citations contain verifiable statutory source links, last_reviewed, and reviewer attribution."""
    query = "RBI limited customer liability zero liability rule for unauthorized transaction"
    citations = rag_retriever.retrieve(query, top_k=2)

    assert len(citations) >= 1
    citation = citations[0]
    assert citation["official_source_link"] != ""
    assert citation["official_source_link"].startswith("https://")
    assert citation["last_reviewed"] != ""
    assert citation["reviewer"] != ""
