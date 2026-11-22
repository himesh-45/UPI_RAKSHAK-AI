import React, { useState } from 'react';
import {
  QrCode, Shield, Smartphone, Send, MessageSquare,
  CheckCircle2, AlertTriangle, ArrowRight, Printer, Sparkles, Scale,
  ExternalLink, Copy, Check
} from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import ModelHonestyPanel from '../components/ModelHonestyPanel';

const PRELOADED_TESTS = [
  {
    id: 'digital_arrest',
    title: '🚨 Digital Arrest Extortion',
    lang: 'English / Hindi',
    category: 'digital_arrest_extortion',
    text: 'This is Inspector Vijay Rathore from Mumbai Crime Branch. A FedEx parcel sent in your name to Taiwan was intercepted with 140g MDMA drugs. You are being placed under Digital Arrest right now. Stay on Skype video call or police will reach your house. Transfer verification funds to RBI escrow account.',
    expected: 'HIGH RISK (Score: 100)'
  },
  {
    id: 'olx_collect',
    title: '🛒 OLX "Scan QR to Receive Money"',
    lang: 'English',
    category: 'fake_collect_request',
    text: 'Dear seller, I am buying your sofa for Rs 18,000. I have sent a PhonePe QR code. Please scan it and enter your 6-digit UPI PIN to immediately receive the Rs 18,000 in your bank account.',
    expected: 'HIGH RISK (Score: 100)'
  },
  {
    id: 'part_time_job',
    title: '💼 YouTube Like Part-Time Job Scam',
    lang: 'English / Hinglish',
    category: 'job_investment_scam',
    text: 'Work from home opportunity! Earn daily Rs 2500 - 5000 just by liking YouTube videos and rating hotels on Google Maps. No experience needed. Daily instant UPI payment. Contact HR Priya on Telegram @earnmoney_daily_in',
    expected: 'HIGH RISK (Score: 90+)'
  },
  {
    id: 'bank_kyc',
    title: '🏦 SBI YONO KYC Suspension Trap',
    lang: 'English',
    category: 'fake_bank_kyc',
    text: 'URGENT SBI ALERT: Your YONO NetBanking account has been blocked due to pending KYC verification. Update your PAN card and Aadhaar details immediately at http://sbi-kyc-update.top to prevent permanent closure.',
    expected: 'HIGH RISK (Score: 100)'
  },
  {
    id: 'legit_refund',
    title: '✅ Genuine Swiggy Refund & Bank SMS',
    lang: 'English (Negative Control)',
    category: 'legitimate',
    text: 'Dear Customer, your refund of INR 320.00 for Order #SW91823 has been processed to your HDFC Bank A/c ending 4821 via UPI. Updated Balance: INR 14,250.00. - HDFC Bank',
    expected: 'SAFE (Score: 0 - Low Risk)'
  }
];

export default function JudgeTryPage() {
  const { t } = useTranslation();
  const [selectedTest, setSelectedTest] = useState(PRELOADED_TESTS[0]);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  const originUrl = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:5173';
  const telegramBotUrl = 'https://t.me/upi_rakshak_bot';
  const whatsappUrl = 'https://wa.me/14155238886?text=join%20smooth-compass';

  const handleRunAnalysis = async (testItem) => {
    setSelectedTest(testItem);
    setAnalyzing(true);
    setAnalysisResult(null);

    try {
      const res = await fetch('/api/analyze/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: testItem.text,
          language: 'auto',
          save_history: false
        })
      });
      if (!res.ok) throw new Error('Analysis failed');
      const data = await res.json();
      setAnalysisResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      
      {/* Top Banner & Title */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 text-xs font-bold uppercase tracking-wider mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            Hackathon Judge Evaluation Portal
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">
            Live Testing & Defensibility Bench
          </h1>
          <p className="text-slate-600 dark:text-slate-400 text-sm mt-1 max-w-3xl">
            Test UPI Rakshak AI live on your smartphone, run instant adversarial scenarios, or examine technical defenses against fraud evasion.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => window.print()}
            className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-bold flex items-center gap-2 transition shadow-sm"
          >
            <Printer className="w-4 h-4" />
            Print Judge Handout
          </button>
        </div>
      </div>

      {/* Live QR Codes Section */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Smartphone className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
          <h2 className="text-lg font-bold text-slate-900 dark:text-white">
            Scan to Test Live on Your Phone
          </h2>
        </div>
        <p className="text-xs text-slate-500 mb-6">
          Judges can scan these QR codes using their iOS/Android camera to test the web interface or interact directly with the conversational bots.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Card 1: Web Interface */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 flex flex-col items-center text-center shadow-sm">
            <div className="p-2 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 mb-3">
              <QrCode className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 dark:text-white text-sm">Web Application</h3>
            <p className="text-xs text-slate-500 mt-1 mb-4">Scan to open mobile responsive client</p>
            <div className="bg-white p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner">
              <img
                src={`/api/report/generate-qr?text=${encodeURIComponent(originUrl)}`}
                alt="Web App QR"
                className="w-36 h-36 object-contain"
              />
            </div>
            <a
              href={originUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 text-xs font-bold text-indigo-600 dark:text-indigo-400 flex items-center gap-1 hover:underline"
            >
              <span>{originUrl}</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

          {/* Card 2: Telegram Bot */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 flex flex-col items-center text-center shadow-sm">
            <div className="p-2 rounded-xl bg-sky-50 dark:bg-sky-950/50 text-sky-600 dark:text-sky-400 mb-3">
              <Send className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 dark:text-white text-sm">Telegram Bot</h3>
            <p className="text-xs text-slate-500 mt-1 mb-4">Forward SMS or paste screenshots to @upi_rakshak_bot</p>
            <div className="bg-white p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner">
              <img
                src={`/api/report/generate-qr?text=${encodeURIComponent(telegramBotUrl)}`}
                alt="Telegram Bot QR"
                className="w-36 h-36 object-contain"
              />
            </div>
            <a
              href={telegramBotUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 text-xs font-bold text-sky-600 dark:text-sky-400 flex items-center gap-1 hover:underline"
            >
              <span>t.me/upi_rakshak_bot</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

          {/* Card 3: WhatsApp Bot */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 flex flex-col items-center text-center shadow-sm">
            <div className="p-2 rounded-xl bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400 mb-3">
              <MessageSquare className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 dark:text-white text-sm">WhatsApp Bot</h3>
            <p className="text-xs text-slate-500 mt-1 mb-4">Twilio Sandbox / Meta Cloud API webhook</p>
            <div className="bg-white p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner">
              <img
                src={`/api/report/generate-qr?text=${encodeURIComponent(whatsappUrl)}`}
                alt="WhatsApp Bot QR"
                className="w-36 h-36 object-contain"
              />
            </div>
            <a
              href={whatsappUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1 hover:underline"
            >
              <span>Connect on WhatsApp</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

        </div>
      </div>

      {/* Interactive 1-Click Evaluation Station */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <Shield className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
          <h2 className="text-lg font-bold text-slate-900 dark:text-white">
            1-Click Interactive Adversarial Scenarios
          </h2>
        </div>
        <p className="text-xs text-slate-500 mb-6">
          Click any scenario to execute live CPU inference and examine the multi-detector risk waterfall in real time.
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Scenario Buttons */}
          <div className="lg:col-span-5 space-y-2.5">
            {PRELOADED_TESTS.map((test) => {
              const isActive = selectedTest?.id === test.id;
              return (
                <div
                  key={test.id}
                  onClick={() => handleRunAnalysis(test)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition flex flex-col gap-1 text-left ${
                    isActive
                      ? 'bg-indigo-50/70 dark:bg-indigo-950/40 border-indigo-300 dark:border-indigo-800 shadow-xs'
                      : 'bg-slate-50 dark:bg-slate-800/40 border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-slate-900 dark:text-white">
                      {test.title}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded font-mono font-bold bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                      {test.lang}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500 line-clamp-2 mt-0.5">
                    "{test.text}"
                  </p>
                  <div className="flex items-center justify-between mt-1 text-[10px] text-slate-400">
                    <span>Expected: <strong className="text-slate-600 dark:text-slate-300">{test.expected}</strong></span>
                    <span className="text-indigo-600 dark:text-indigo-400 font-bold flex items-center gap-0.5">
                      Run Live <ArrowRight className="w-3 h-3" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Real-Time Result Box */}
          <div className="lg:col-span-7 bg-slate-50 dark:bg-slate-950 rounded-xl p-5 border border-slate-200 dark:border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
                <span className="text-xs font-extrabold uppercase tracking-wider text-slate-500">
                  Live Execution Inspector
                </span>
                {analysisResult && (
                  <span
                    className={`px-2.5 py-0.5 rounded text-xs font-black uppercase tracking-wider ${
                      analysisResult.verdict === 'HIGH RISK'
                        ? 'bg-rose-100 dark:bg-rose-900/60 text-rose-700 dark:text-rose-300'
                        : analysisResult.verdict === 'SUSPICIOUS'
                        ? 'bg-amber-100 dark:bg-amber-900/60 text-amber-700 dark:text-amber-300'
                        : 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300'
                    }`}
                  >
                    {analysisResult.verdict} • {analysisResult.risk_score}/100
                  </span>
                )}
              </div>

              {analyzing ? (
                <div className="py-16 text-center text-slate-500 space-y-2">
                  <div className="w-6 h-6 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto" />
                  <p className="text-xs">Executing multi-layer CPU risk fusion...</p>
                </div>
              ) : analysisResult ? (
                <div className="mt-4 space-y-4">
                  {/* Category & Confidence */}
                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div className="bg-white dark:bg-slate-900 p-2.5 rounded-lg border border-slate-200 dark:border-slate-800">
                      <span className="text-slate-400 block text-[10px]">Detected Category</span>
                      <strong className="text-slate-800 dark:text-slate-200 font-mono">
                        {analysisResult.detected_category}
                      </strong>
                    </div>
                    <div className="bg-white dark:bg-slate-900 p-2.5 rounded-lg border border-slate-200 dark:border-slate-800">
                      <span className="text-slate-400 block text-[10px]">Language Detected</span>
                      <strong className="text-slate-800 dark:text-slate-200 uppercase font-mono">
                        {analysisResult.language}
                      </strong>
                    </div>
                  </div>

                  {/* Plain Language Explanation */}
                  <div className="bg-white dark:bg-slate-900 p-3.5 rounded-lg border border-slate-200 dark:border-slate-800">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                      Plain Language Defense Explanation
                    </span>
                    <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                      {analysisResult.plain_language_explanation}
                    </p>
                  </div>

                  {/* Evidence Items */}
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
                      Independent Technical Evidence ({analysisResult.evidence?.length || 0} signals)
                    </span>
                    <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                      {analysisResult.evidence?.map((ev, i) => (
                        <div
                          key={i}
                          className="text-xs p-2 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-start gap-2"
                        >
                          <span className="px-1.5 py-0.5 rounded text-[9px] font-mono font-bold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 shrink-0">
                            {ev.source_module}
                          </span>
                          <span className="text-slate-700 dark:text-slate-300 leading-snug">
                            {ev.signal}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="py-16 text-center text-slate-400 text-xs">
                  Click any scenario on the left or press "Run Live" to view instant results.
                </div>
              )}
            </div>

            {/* Input snippet display */}
            <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500">
              <span className="truncate max-w-md italic">"{selectedTest?.text}"</span>
              <button
                onClick={() => copyToClipboard(selectedTest?.text, 'snippet')}
                className="shrink-0 p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 transition"
                title="Copy snippet"
              >
                {copiedId === 'snippet' ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Model Reliability & Quality Gates Panel (For Judges) */}
      <ModelHonestyPanel defaultOpen={true} />

      {/* Judge Cheat Sheet / Architecture Highlights */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Scale className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">
              Judge Defensibility & Technical Architecture Matrix
            </h2>
          </div>
          <p className="text-xs text-slate-500">
            Answers to tough architectural and practical questions for hackathon judges.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs leading-relaxed">
          
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800 space-y-2">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              1. Why Evidence-Based Fusion over Pure LLM?
            </h3>
            <p className="text-slate-600 dark:text-slate-300">
              Asking a cloud LLM <em>"is this message a scam?"</em> suffers from severe prompt injection vulnerability, hallucination, non-deterministic latency (1.5s - 4s), and high inference cost. UPI Rakshak AI uses a deterministic multi-engine pipeline (NLP char+word n-grams + Regex safety rules + Algorithmic URL/QR static parsers). The LLM/template layer is strictly constrained to <strong>explaining verifiable evidence</strong> in the user's native tongue.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800 space-y-2">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              2. How is Sub-50ms CPU Latency Achieved?
            </h3>
            <p className="text-slate-600 dark:text-slate-300">
              Our TF-IDF char+word n-gram vectorizers and calibrated linear classifiers evaluate in ~11 ms on ordinary CPU hardware (~32 ms end-to-end multi-detector fusion). Pure algorithmic parsing of URLs (Trie matching + Levenshtein distance) runs in under 8ms. Under 50 concurrent client load, text inference achieves 25.0 req/s with 0 errors, requiring zero GPU instances and enabling local offline operation without internet (core engine runs without internet; bots need internet).
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800 space-y-2">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              3. Statutory Indian Legal Grounding
            </h3>
            <p className="text-slate-600 dark:text-slate-300">
              Unlike generic toxicity or spam filters, UPI Rakshak AI grounds coercion threats in Indian statutory law (CrPC Section 41 / BNSS Section 35). The system directly informs victims that Indian law recognizes no concept of "Digital Arrest" or Skype police trials, and generates a structured, pre-filled complaint dossier formatted for immediate <strong>1930 / cybercrime.gov.in</strong> reporting.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800 space-y-2">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              4. Anti-Poisoning & Privacy Architecture
            </h3>
            <p className="text-slate-600 dark:text-slate-300">
              Our Community Reputation database prevents sybil attacks via strict consensus gating (&ge; 2 distinct reporter hashes), 24h per-entity reporter caps, 30-day half-life recency decay, and an automated immune whitelist protecting authorized banks and utility handles. All phone, UPI, and account identifiers are masked with salted SHA-256 hashes prior to storage.
            </p>
          </div>

        </div>
      </div>

    </div>
  );
}
