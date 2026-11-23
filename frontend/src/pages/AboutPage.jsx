import React from 'react';
import {
  Shield, Cpu, Globe, QrCode, BookOpen, Layers,
  AlertTriangle, PhoneCall, CheckCircle, ArrowRight, GitBranch,
  Lock, Eye, FileText, Zap
} from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import ModelHonestyPanel from '../components/ModelHonestyPanel';

export default function AboutPage() {
  const { t } = useTranslation();

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-12 animate-fade-in text-ink">
      
      {/* Title */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-navy text-teal border border-teal/40">
          <Shield className="w-3.5 h-3.5" />
          <span>Evidence-Based Security Architecture</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-ink font-display tracking-tight">
          How UPI Rakshak AI Works
        </h1>
        <p className="text-sm sm:text-base text-ink-muted max-w-2xl mx-auto leading-relaxed">
          UPI Rakshak AI rejects the naive approach of asking a generic LLM <em>"is this a scam?"</em>.
          The verdict is forged through five independent deterministic & ML engines fused via a dominant-signal risk pipeline with zero network execution.
        </p>
      </div>

      {/* Visual Architecture Flowchart */}
      <div className="p-6 sm:p-8 rounded-3xl bg-navy-surface/90 border border-border shadow-2xl space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-border">
          <div className="flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-teal" />
            <h3 className="font-bold text-lg text-ink">End-to-End Threat Pipeline Flow</h3>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-navy text-teal border border-teal/30 font-mono">
            Zero Network Calls • Offline
          </span>
        </div>

        {/* 4-Stage Flow Diagram */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 relative">
          {/* Stage 1: Input */}
          <div className="p-4 rounded-2xl bg-navy border border-border space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-teal block">Layer 1: Input</span>
            <h4 className="font-bold text-sm text-ink">Suspicious Artifact</h4>
            <ul className="text-xs text-ink-muted space-y-1">
              <li>• SMS / WhatsApp Text</li>
              <li>• Payment Link / Domain</li>
              <li>• Image / Screenshot (OCR)</li>
              <li>• UPI QR Code / VPA</li>
            </ul>
          </div>

          {/* Stage 2: Independent Detectors */}
          <div className="p-4 rounded-2xl bg-navy border border-border space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-gold-400 block">Layer 2: Detectors</span>
            <h4 className="font-bold text-sm text-ink">Multi-Engine Audit</h4>
            <ul className="text-xs text-ink-muted space-y-1">
              <li>• Hybrid NLP (Char+Word+Features)</li>
              <li>• Rule Layer (Negation-Aware)</li>
              <li>• Static URL Engine (88 Brands)</li>
              <li>• QR / UPI Pay Parameter Parser</li>
            </ul>
          </div>

          {/* Stage 3: Risk Fusion */}
          <div className="p-4 rounded-2xl bg-navy border border-border space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-verdict-danger block">Layer 3: Fusion</span>
            <h4 className="font-bold text-sm text-ink">Dominant Signal Fusion</h4>
            <ul className="text-xs text-ink-muted space-y-1">
              <li>• Max-Signal Routing</li>
              <li>• Corroboration Bonus (+12)</li>
              <li>• Hard Overrides (OTP/PIN)</li>
              <li>• Advisory Context Suppression</li>
            </ul>
          </div>

          {/* Stage 4: Output & Action */}
          <div className="p-4 rounded-2xl bg-navy border border-border space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-verdict-safe block">Layer 4: Action</span>
            <h4 className="font-bold text-sm text-ink">Defensible Output</h4>
            <ul className="text-xs text-ink-muted space-y-1">
              <li>• Calibrated Verdict (0–100)</li>
              <li>• Token Highlight & Waterfall</li>
              <li>• 3-Stage Attack Timeline</li>
              <li>• Pre-Filled 1930 Complaint</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Multi-Layer Engine Modules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Module 1: NLP Classifier */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-navy text-teal border border-border flex items-center justify-center">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-ink">1. NLP Scam Classifier</h3>
          <p className="text-xs text-ink-muted leading-relaxed">
            Multilingual hybrid classifier (Word 1-2 + Char 3-5 n-grams + engineered text features + Platt sigmoid calibration) trained across English, Hindi, Telugu, Hinglish, and Romanized Telugu over 15 distinct scam categories and hard negatives.
          </p>
        </div>

        {/* Module 2: Rule Safety Layer */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-navy text-verdict-danger border border-border flex items-center justify-center">
            <Shield className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-ink">2. Negation-Aware Safety Rules</h3>
          <p className="text-xs text-ink-muted leading-relaxed">
            Context-aware regex rules with 80-character preceding negation checking. Distinguishes attack demands (<em>"enter your OTP"</em>) from genuine bank safety advisories (<em>"NEVER share OTP with anyone"</em>), preventing catastrophic false alarms.
          </p>
        </div>

        {/* Module 3: Static URL Scanner */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-navy text-verdict-suspicious border border-border flex items-center justify-center">
            <Globe className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-ink">3. Static URL Scanner</h3>
          <p className="text-xs text-ink-muted leading-relaxed">
            Strictly static analysis: NEVER fetches, opens, or resolves links. Detects IP hosts, shorteners, punycode, brand typosquatting via edit distance against 88 Indian banks/fintechs, and multi-label subdomain deception (e.g. <code>sbi.co.in.fake.xyz</code>).
          </p>
        </div>

        {/* Module 4: QR & OCR Module */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-navy text-verdict-safe border border-border flex items-center justify-center">
            <QrCode className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-ink">4. Honest Screenshot & QR Engine</h3>
          <p className="text-xs text-ink-muted leading-relaxed">
            Decodes QR codes without visiting them. Parses <code>upi://pay</code> parameters (pa, pn, am, cu, tn) and flags anomalies. If OCR is unavailable, it honestly returns an unavailable state rather than hallucinating text.
          </p>
        </div>

        {/* Module 5: RAG Knowledge Engine */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-navy text-gold-400 border border-border flex items-center justify-center">
            <BookOpen className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-ink">5. 89 Verified RAG Citations</h3>
          <p className="text-xs text-ink-muted leading-relaxed">
            Offline factual knowledge base citing official NPCI guidelines, RBI master circulars on customer zero-liability, 24x7 bank fraud desks, and MHA cybercrime protocols.
          </p>
        </div>

        {/* Module 6: Risk Fusion Engine */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-navy text-teal border border-border flex items-center justify-center">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-ink">6. Dominant-Signal Risk Fusion</h3>
          <p className="text-xs text-ink-muted leading-relaxed">
            Avoids score dilution by anchoring on the maximum detector signal, adding +12 corroboration bonuses when multiple modules confirm danger, and decomposing the output into an explainable score waterfall.
          </p>
        </div>
      </div>

      {/* 15 Scam Categories Covered */}
      <div className="p-6 sm:p-8 rounded-3xl bg-navy-surface/90 border border-border space-y-4">
        <h3 className="text-base font-bold text-ink flex items-center gap-2">
          <Zap className="w-4 h-4 text-gold-400" />
          15 Specialized Fraud Categories Classified
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 text-xs text-ink-muted">
          <div className="p-2 rounded-lg bg-navy border border-border">1. Fake Bank KYC Phishing</div>
          <div className="p-2 rounded-lg bg-navy border border-border">2. Electricity Disconnection Scam</div>
          <div className="p-2 rounded-lg bg-navy border border-border">3. Fake UPI Refund / Cashback</div>
          <div className="p-2 rounded-lg bg-navy border border-border">4. UPI Collect Request PIN Fraud</div>
          <div className="p-2 rounded-lg bg-navy border border-border">5. KBC Lottery / Prize Fraud</div>
          <div className="p-2 rounded-lg bg-navy border border-border">6. Fake Customer Care Helpline</div>
          <div className="p-2 rounded-lg bg-navy border border-border">7. Remote Access Takeover (AnyDesk)</div>
          <div className="p-2 rounded-lg bg-navy border border-border">8. OTP / UPI PIN Theft</div>
          <div className="p-2 rounded-lg bg-navy border border-border">9. Fake Government Schemes / Subsidy</div>
          <div className="p-2 rounded-lg bg-navy border border-border">10. Part-Time Task & Crypto Scam</div>
          <div className="p-2 rounded-lg bg-navy border border-border">11. Predatory Loan App Blackmail</div>
          <div className="p-2 rounded-lg bg-navy border border-border">12. Courier Narcotics / Digital Arrest</div>
          <div className="p-2 rounded-lg bg-navy border border-border">13. OLX / Marketplace Fake QR</div>
          <div className="p-2 rounded-lg bg-navy border border-border">14. Accidental Transfer Trap</div>
          <div className="p-2 rounded-lg bg-navy border border-border">15. Legitimate Banking Alerts</div>
        </div>
      </div>

      {/* Model Reliability & Quality Gates Panel */}
      <ModelHonestyPanel defaultOpen={true} />

      {/* Honest Limitations & Ethical Disclosure */}
      <div className="p-6 sm:p-8 rounded-3xl bg-navy-surface/90 border border-gold-500/40 space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-gold-400 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-gold-400" />
          Honest Limitations & Defensible Scope
        </h3>
        <ul className="text-xs text-ink-muted space-y-2.5 list-disc list-inside leading-relaxed">
          <li><strong>Heuristic Risk Indicator:</strong> The 0–100 score is an evidence-based risk metric tuned to hit ≥95% scam recall at ≤3% legitimate false-positive rate. It is NOT mathematical certainty.</li>
          <li><strong>Definition of "SAFE":</strong> A verdict of <code>SAFE</code> (0–34) means <em>"no strong scam patterns were detected"</em>. It does not certify that a completely novel attack is impossible.</li>
          <li><strong>Zero Network Resolution:</strong> Suspicious URLs are never opened, resolved, or requested. All URL signals are derived purely from static structural and lexical analysis.</li>
          <li><strong>Privacy First:</strong> Masking happens client-side and server-side before persistence. Phone numbers, credit cards, and OTPs are redacted into <code>[REDACTED]</code> tokens.</li>
          <li><strong>Channel Roadmap:</strong> WhatsApp integration is a planned future channel (requires Meta Business API approval).</li>
        </ul>
      </div>
    </div>
  );
}
