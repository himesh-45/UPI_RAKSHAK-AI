import React from 'react';
import { Shield, Cpu, Globe, QrCode, BookOpen, Layers, AlertTriangle, PhoneCall, CheckCircle } from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';

export default function AboutPage() {
  const { t } = useTranslation();

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-12 animate-fade-in">
      
      {/* Title */}
      <div className="text-center space-y-3">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white">
          Architecture & Principles
        </h1>
        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          UPI Rakshak AI is built on the core principle of <strong>EVIDENCE-BASED detection</strong>.
          The verdict comes from independent deterministic detectors fused together, not by asking an LLM "is this a scam?".
        </p>
      </div>

      {/* Multi-Layer Engine Modules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Module 1: NLP Classifier */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 flex items-center justify-center">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-white">1. NLP Scam Classifier</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Multilingual classifier (Word 1-2 + Char 3-5 n-grams + Logistic Regression) trained across English, Hindi, Telugu, and Hinglish over 8 distinct scam categories and hard negatives.
          </p>
        </div>

        {/* Module 2: Rule Safety Layer */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-rose-50 dark:bg-rose-950 text-rose-600 dark:text-rose-400 flex items-center justify-center">
            <Shield className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-white">2. Deterministic Safety Layer</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Hard-override safety rules that always flag OTP/PIN requests, collect request tricks (receiving money requires no PIN), urgency block threats, and remote access apps (AnyDesk/TeamViewer).
          </p>
        </div>

        {/* Module 3: Static URL Scanner */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-amber-50 dark:bg-amber-950 text-amber-600 dark:text-amber-400 flex items-center justify-center">
            <Globe className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-white">3. Static URL Scanner</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Strictly static analysis: NEVER fetches, opens, or resolves links. Detects IP hosts, shorteners, punycode, brand typosquatting via edit distance against Indian banks, and disposable TLDs.
          </p>
        </div>

        {/* Module 4: QR & OCR Module */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <QrCode className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-white">4. Screenshot & QR Engine</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Decodes QR codes without visiting them. Parses <code>upi://pay</code> parameters (pa, pn, am, cu, tn) and detects institutional name / VPA mismatches and deceptive cashback lures.
          </p>
        </div>

        {/* Module 5: RAG Knowledge Engine */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-violet-50 dark:bg-violet-950 text-violet-600 dark:text-violet-400 flex items-center justify-center">
            <BookOpen className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-white">5. Verified RAG Engine</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Offline factual knowledge base citing official NPCI, RBI, and MHA cybercrime protocols. Automatically attaches cited guidance to explain why signals matter and what actions to take.
          </p>
        </div>

        {/* Module 6: Risk Fusion Engine */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-2xl bg-cyan-50 dark:bg-cyan-950 text-cyan-600 dark:text-cyan-400 flex items-center justify-center">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-white">6. Risk Fusion Engine</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Mathematical, explainable aggregation into a 0–100 risk score and calibrated verdicts: SAFE (0–34), SUSPICIOUS (35–69), and HIGH RISK (70–100) with hard-override guarantees.
          </p>
        </div>
      </div>

      {/* Honest Limitations & Ethical Disclosure */}
      <div className="p-6 rounded-3xl bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-500" />
          Honest Limitations & Ethical Disclosure
        </h3>
        <ul className="text-xs text-slate-600 dark:text-slate-400 space-y-2 list-disc list-inside leading-relaxed">
          <li><strong>Heuristic Risk Indicator:</strong> The score (0–100) is a weighted heuristic risk metric, NOT a calibrated statistical probability or mathematical certainty.</li>
          <li><strong>No Guarantee of Absolute Safety:</strong> A verdict of <code>SAFE</code> signifies that "no strong scam signals were found" on the analyzed sample. Users must always verify transactions directly with their bank.</li>
          <li><strong>Zero Network Resolution:</strong> Suspicious links are analyzed statically. We deliberately avoid active HTTP fetching to protect users from drive-by attacks and tracking tokens.</li>
          <li><strong>Synthetic Data Notice:</strong> The NLP model was trained on an algorithmic synthetic dataset. Metrics reflect this synthetic test set and should not be construed as real-world field benchmarks.</li>
        </ul>
      </div>
    </div>
  );
}
