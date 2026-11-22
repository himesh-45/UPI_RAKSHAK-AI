# UPI Rakshak AI — Empirical User Study Report

> [!NOTE]
> **Status**: Study Harness Active (0 Participant Responses Recorded).
> The study protocol and web harness are deployed at `/study`.
> In strict adherence to our anti-fabrication rules, zero artificial responses have been synthesized.

---

## 1. Study Methodology & Experimental Design

- **Protocol**: Within-subjects randomized trial comparing human fraud detection accuracy before vs after evidence disclosure.
- **Sample Size Target**: 30+ independent human participants (300+ total decision trials across en, hi, te).
- **Phased Evaluation Protocol**:
  1. **Phase 1 (Pre-Tool Baseline)**: Participant evaluates randomized payment communication (Scam vs Genuine) and indicates confidence (1-5).
  2. **Phase 2 (Evidence Disclosure)**: System displays multi-layer verdict, risk score, and top 3 evidence points.
  3. **Phase 3 (Post-Tool Decision Impact)**: Participant reports if evidence altered their decision, provides revised verdict, and rates explanation clarity.
- **Admin Export**: Responses can be exported via `GET /api/study/export` (authorized admin endpoint) or evaluated programmatically with `make study-report`.
