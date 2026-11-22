import React, { useState } from 'react';
import {
  ShieldAlert, ShieldCheck, AlertTriangle, Scale, PhoneCall,
  CheckCircle2, ArrowRight, Video, FileWarning, HelpCircle
} from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';

const DEMO_SCENARIOS = [
    {
      title: 'FedEx Narcotics Parcel',
      lang: 'English',
      text: 'This is Inspector Vijay Rathore from Mumbai Crime Branch. A FedEx parcel sent in your name to Taiwan was intercepted with 16 fake passports and 140 grams of MDMA drugs. You are being placed under Digital Arrest right now. Stay on this Skype video call and do not disconnect.'
    },
    {
      title: 'सीबीआई वर्चुअल कोर्ट समन',
      lang: 'Hindi',
      text: 'सीबीआई मुख्यालय नई दिल्ली: मनी लॉन्ड्रिंग के मामले में आपके खिलाफ गैर-जमानती गिरफ्तारी वारंट जारी हुआ है। तुरंत हमारे वर्चुअल कोर्ट रूम में स्काइप कैमरा चालू करके जुड़ें, अन्यथा आपके घर पर पुलिस टीम भेजी जा रही है। सुरक्षा के लिए आरबीआई सत्यापन खाते में पैसे डालें।'
    },
    {
      title: 'ముంబై పోలీస్ డిజిటల్ అరెస్ట్',
      lang: 'Telugu',
      text: 'ఇది ముంబై క్రైమ్ బ్రాంచ్ నుండి ఇన్‌స్పెక్టర్. మీ ఆధార్ కార్డు పేరుతో పంపిన ఫెడెక్స్ పార్శిల్ లో 150 గ్రాముల ఎండీఎంఏ డ్రగ్స్ దొరికాయి. మిమ్మల్ని డిజిటల్ అరెస్ట్ చేస్తున్నాము. స్కైప్ వీడియో కాల్ లోనే ఉండండి, కాల్ కట్ చేయవద్దు.'
    },
    {
      title: 'Genuine Courier SMS (Safe)',
      lang: 'English / Negative',
      text: 'FedEx Express: Your shipment with tracking number FX-78219482 is out for delivery today with courier executive Ramesh. Track live on fedex.com.'
    }
];

export default function DigitalArrestPage({ onOpenPreFilled1930 }) {
  const { t, language } = useTranslation();
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleEvaluate = async (e) => {
    if (e) e.preventDefault();
    if (!inputText.trim()) {
      setError('Please paste or type the suspicious call script or message');
      return;
    }
    setError('');
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch('/api/analyze/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText.trim(), language: 'auto' })
      });
      if (!res.ok) throw new Error('Analysis failed');
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Evaluation failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectScenario = (scen) => {
    setInputText(scen.text);
    setError('');
    setResult(null);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8 animate-fade-in">
      {/* Top Banner: National Cybercrime Advisory */}
      <div className="p-5 rounded-3xl bg-gradient-to-r from-rose-950/40 via-amber-950/20 to-slate-900 border border-rose-800/40 shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3.5">
          <div className="p-3 rounded-2xl bg-rose-500/20 text-rose-400 border border-rose-500/30">
            <Scale className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-rose-500/30 text-rose-300 border border-rose-500/50">
                Official Legal Reality Check
              </span>
              <span className="text-xs text-slate-400 font-semibold">MHA / Cyber Dost Advisory</span>
            </div>
            <h2 className="text-lg font-black text-white mt-1">
              Indian Law Does NOT Recognize "Digital Arrest"
            </h2>
            <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
              No genuine police officer, CBI/ED official, or judge conducts official investigations or arrests over Skype or WhatsApp video calls. Demands to stay in a room with cameras on are psychological extortion.
            </p>
          </div>
        </div>

        <a
          href="https://cybercrime.gov.in"
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs shadow-lg shadow-rose-600/30 transition shrink-0 flex items-center gap-1.5"
        >
          <PhoneCall className="w-3.5 h-3.5" /> Helpline 1930
        </a>
      </div>

      {/* Header & Overview */}
      <div className="text-center space-y-2">
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">
          Digital Arrest & Police Video Call Extortion Checker
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 max-w-xl mx-auto">
          Audit suspicious calls alleging contraband parcels (FedEx/DHL/Customs), non-bailable warrants, or sham "RBI safe escrow" demands.
        </p>
      </div>

      {/* Pre-fill Scenarios Chips */}
      <div className="space-y-2">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
          Quick Demo Scenarios (Click to Load):
        </span>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
          {DEMO_SCENARIOS.map((scen, idx) => (
            <button
              key={idx}
              onClick={() => handleSelectScenario(scen)}
              className="p-3 text-left rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-indigo-500 dark:hover:border-indigo-500 transition shadow-xs space-y-1 group"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900 dark:text-white group-hover:text-indigo-500 transition">
                  {scen.title}
                </span>
                <span className="text-[10px] text-slate-400 font-mono">
                  {scen.lang}
                </span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-2">
                {scen.text}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Input Form */}
      <form onSubmit={handleEvaluate} className="space-y-4">
        <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-2">
          <label className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center justify-between">
            <span>Paste Call Transcript, SMS, or Voice Note Transcript:</span>
            <span className="text-[11px] text-slate-400 font-normal">English, हिंदी, తెలుగు, Hinglish</span>
          </label>
          <textarea
            rows={5}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="e.g. This is Inspector Rathore from Mumbai Crime Branch. Your FedEx parcel containing MDMA drugs was seized. Stay on this Skype call..."
            className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-3.5 text-sm text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:border-indigo-500 leading-relaxed font-sans"
          />
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 text-xs text-rose-700 dark:text-rose-300">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3.5 rounded-xl bg-gradient-to-r from-rose-600 via-indigo-600 to-indigo-700 hover:from-rose-500 hover:to-indigo-600 text-white font-extrabold text-sm shadow-lg shadow-indigo-500/20 transition-all flex items-center justify-center gap-2"
        >
          {loading ? 'Evaluating Coercion Tactics...' : 'Audit For Digital Arrest Extortion'}
          <ArrowRight className="w-4 h-4" />
        </button>
      </form>

      {/* Results Display */}
      {result && (
        <div className="space-y-6 animate-fade-in">
          {/* Main Verdict Card */}
          <div className={`p-6 rounded-3xl border shadow-lg ${
            result.verdict === 'HIGH RISK'
              ? 'bg-rose-50 dark:bg-rose-950/30 border-rose-300 dark:border-rose-900/60'
              : (result.verdict === 'SUSPICIOUS'
                  ? 'bg-amber-50 dark:bg-amber-950/30 border-amber-300 dark:border-amber-900/60'
                  : 'bg-emerald-50 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-900/60')
          }`}>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-3">
                <span className={`px-3.5 py-1.5 rounded-full text-xs font-black tracking-wider uppercase ${
                  result.verdict === 'HIGH RISK'
                    ? 'bg-rose-600 text-white'
                    : (result.verdict === 'SUSPICIOUS' ? 'bg-amber-500 text-white' : 'bg-emerald-600 text-white')
                }`}>
                  {result.verdict === 'HIGH RISK' ? '🔴 DIGITAL ARREST SCAM DETECTED' : (result.verdict === 'SUSPICIOUS' ? '🟡 SUSPICIOUS COERCION' : '🟢 VERIFIED LEGITIMATE')}
                </span>
                <span className="text-xs font-mono font-bold text-slate-600 dark:text-slate-400">
                  Risk Score: {result.risk_score}/100
                </span>
              </div>

              <div className="text-right">
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Detected Taxonomy</span>
                <span className="text-xs font-bold text-slate-800 dark:text-slate-200">
                  {result.detected_category.replace(/_/g, ' ').toUpperCase()}
                </span>
              </div>
            </div>

            {/* Plain Explanation */}
            <div className="mt-4 text-sm text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
              {result.plain_language_explanation}
            </div>

            {/* Legal Facts Box if High Risk */}
            {result.verdict === 'HIGH RISK' && (
              <div className="mt-4 p-4 rounded-2xl bg-white dark:bg-slate-900/90 border border-rose-200 dark:border-rose-900/80 space-y-2">
                <div className="flex items-center gap-2 text-rose-600 dark:text-rose-400 font-bold text-xs uppercase tracking-wider">
                  <Scale className="w-4 h-4" />
                  <span>Statutory Legal Protection Reality</span>
                </div>
                <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                  Under the Bharatiya Nagarik Suraksha Sanhita (BNSS) and the Code of Criminal Procedure (CrPC), <strong>police cannot arrest citizens over video calls</strong>. Real police officers must serve physical summons, be in uniform with identifiable name tags, and provide a written arrest memo in the presence of family or independent witnesses.
                </p>
              </div>
            )}
          </div>

          {/* Extracted Coercion Tactics */}
          <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <FileWarning className="w-4 h-4 text-rose-500" />
              <span>Extracted Coercion Tactics & Evidence Signals</span>
            </h3>
            <div className="space-y-2.5">
              {result.evidence.map((ev, i) => (
                <div key={i} className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 flex items-start gap-2.5 text-xs text-slate-700 dark:text-slate-300">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase shrink-0 ${
                    ev.severity === 'CRITICAL' ? 'bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300' : 'bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300'
                  }`}>
                    {ev.severity}
                  </span>
                  <span>{ev.signal}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Actionable Emergency Guidance */}
          <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-emerald-500" />
              <span>Immediate Defense Actions</span>
            </h3>
            <ul className="space-y-2 text-xs text-slate-700 dark:text-slate-300">
              {result.recommended_actions.map((act, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>{act}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
