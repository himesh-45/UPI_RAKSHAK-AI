import pytest
from backend.app.rag.retriever import rag_retriever

def test_rag_retrieval_collect_request():
    query = "Sender asking to accept collect request and enter UPI PIN to receive cashback"
    citations = rag_retriever.retrieve(query, category="fake_upi_refund_cashback", top_k=2)

    assert len(citations) >= 1
    top_citation = citations[0]
    assert "Receiving Money Never Requires a PIN" in top_citation["title"]
    assert "NPCI" in top_citation["source"]
    assert "Decline all collect requests" in top_citation["actionable_guidance"]

def test_rag_retrieval_electricity_bill():
    query = "Electricity line will be disconnected tonight at 9:30 PM due to unpaid bill"
    citations = rag_retriever.retrieve(query, category="electricity_disconnection", top_k=2)

    assert len(citations) >= 1
    assert any("Electricity Disconnection" in c["title"] for c in citations)
    assert any("CERT-In" in c["source"] or "Power Distribution" in c["source"] for c in citations)

def test_rag_retrieval_helpline():
    query = "I shared my OTP and lost money where do I report fraud immediately"
    citations = rag_retriever.retrieve(query, top_k=2)

    assert len(citations) >= 1
    assert any("1930" in c["title"] or "1930" in c["content"] for c in citations)

def test_rag_empty_query():
    citations = rag_retriever.retrieve("", top_k=2)
    assert citations == []
