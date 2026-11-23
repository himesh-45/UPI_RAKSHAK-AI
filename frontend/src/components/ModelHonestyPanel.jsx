import React, { useState } from 'react';
import {
  ChevronDown, ChevronUp, CheckCircle2, ShieldCheck, Activity,
  Cpu, Database, AlertCircle, HelpCircle, BookOpen, Sparkles
} from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import reportData from '../data/evaluation_report.json';

const GLOSSARY_I18N = {
  en: {
    title: 'What does this mean?',
    recall_term: 'Scam Recall (Detection Rate)',
    recall_def: 'Recall measures the percentage of actual scam attacks that the tool successfully catches without missing them.',
    fpr_term: 'False Alarms (Legitimate False Positive Rate)',
    fpr_def: 'False alarms measure how often genuine, safe messages or transactions are mistakenly flagged as suspicious.',
    calib_term: 'Calibration (Confidence Alignment / ECE)',
    calib_def: 'Calibration measures whether a stated risk score genuinely matches real-world likelihood, so an 80% score truly reflects an 80% chance of fraud.'
  },
  hi: {
    title: 'इसका क्या मतलब है? (शब्दावली)',
    recall_term: 'स्कैम रिकॉल (पकड़ने की दर)',
    recall_def: 'रिकॉल यह मापता है कि यह टूल कितने प्रतिशत वास्तविक धोखाधड़ी हमलों को बिना छूटे सफलतापूर्वक पकड़ लेता है।',
    fpr_term: 'फाल्स अलार्म (गलत चेतावनी दर)',
    fpr_def: 'फाल्स अलार्म यह मापते हैं कि सुरक्षित और प्रामाणिक संदेशों को गलती से कितनी बार संदिग्ध माना गया।',
    calib_term: 'कैलिब्रेशन (आत्मविश्वास संरेखण / ECE)',
    calib_def: 'कैलिब्रेशन यह मापता है कि क्या प्रदर्शित जोखिम स्कोर वास्तव में वास्तविक दुनिया के जोखिम से मेल खाता है (जैसे 80% स्कोर का मतलब 80% खतरा हो)।'
  },
  te: {
    title: 'దీని అర్థం ఏమిటి? (పదకోశం)',
    recall_term: 'స్కామ్ రీకాల్ (గుర్తించే రేటు)',
    recall_def: 'రీకాల్ అనేది ఈ సాధనం ఎన్ని శాతం నిజమైన మోసపూరిత దాడులను తప్పిపోకుండా విజయవంతంగా గుర్తిస్తుందో కొలుస్తుంది.',
    fpr_term: 'ఫాల్స్ అలారమ్స్ (తప్పుడు హెచ్చరికల రేటు)',
    fpr_def: 'ఫాల్స్ అలారమ్స్ అనేది సురక్షితమైన మరియు నిజమైన సందేశాలను పొరపాటున ఎన్నిసార్లు అనుమానాస్పదంగా గుర్తించారో కొలుస్తుంది.',
    calib_term: 'క్యాలిబ్రేషన్ (విశ్వాస సమలేఖనం / ECE)',
    calib_def: 'క్యాలిబ్రేషన్ అనేది చూపించిన ప్రమాద స్కోరు వాస్తవ సంభావ్యతకు అనుగుణంగా ఉందో లేదో కొలుస్తుంది (80% స్కోరు నిజంగా 80% ప్రమాదాన్ని సూచిస్తుంది).'
  }
};

export default function ModelHonestyPanel({ defaultOpen = false, className = '' }) {
  const { language } = useTranslation();
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const [glossaryOpen, setGlossaryOpen] = useState(false);
  const [glossaryLang, setGlossaryLang] = useState(language && ['hi', 'te'].includes(language) ? language : 'en');

  const gates = reportData?.gates || [];
  const passedCount = reportData?.passed_checks ?? gates.filter(g => g.status === 'PASSED').length;
  const totalCount = reportData?.total_checks ?? gates.length;
  const badgeText = reportData?.badge_text || `Passed ${passedCount} of ${totalCount} internal checks`;
  const title = reportData?.title || 'How reliable is this tool?';
  const subtitle = reportData?.subtitle || 'Computed from our evaluation report. Blind test: Pending External Human Data Collection.';
  const eceExplanation = reportData?.ece_explanation || 'Confidence scores are not yet perfectly calibrated.';

  const currentGlossary = GLOSSARY_I18N[glossaryLang] || GLOSSARY_I18N.en;

  return (
    <div className={`bg-navy-surface/90 rounded-3xl border border-border p-5 sm:p-6 transition text-ink ${className}`}>
      
      {/* Header Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-4 text-left group"
        aria-expanded={isOpen}
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-navy text-teal border border-border">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="text-sm font-extrabold text-ink group-hover:text-gold-400 transition">
                {title}
              </h3>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-navy text-gold-400 border border-gold-500/40">
                {badgeText}
              </span>
            </div>
            <p className="text-xs text-ink-muted mt-0.5">
              {subtitle}
            </p>
          </div>
        </div>

        <div className="p-1.5 rounded-xl bg-navy border border-border text-ink-muted shrink-0">
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </button>

      {/* Collapsible Content */}
      {isOpen && (
        <div className="pt-5 mt-4 border-t border-border space-y-5 animate-fade-in">
          
          {/* Plain Language Calibration Disclosure Banner */}
          <div className="p-3.5 rounded-2xl bg-verdict-suspicious/10 border border-verdict-suspicious/30 text-xs text-verdict-suspicious flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 text-verdict-suspicious shrink-0 mt-0.5" />
            <div>
              <p className="font-bold">Honest Machine Learning Disclosure:</p>
              <p className="text-ink-muted text-[11px] leading-relaxed mt-0.5">
                {eceExplanation} Evaluated across frozen Gold Test Set v1 (untouched baseline benchmark) and Gold Test Set v2 (development set used for error analysis). High-confidence predictions on colloquial vernacular phrasing currently exhibit slight over-confidence.
              </p>
            </div>
          </div>

          {/* Quality Gates Table */}
          <div className="overflow-x-auto rounded-2xl border border-border">
            <table className="w-full text-xs text-left">
              <thead className="bg-navy text-ink-muted font-bold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="p-3">Metric Dimension</th>
                  <th className="p-3 text-center">Benchmark Gate</th>
                  <th className="p-3 text-center">Frozen Gold v1</th>
                  <th className="p-3 text-center">Gold v2 (Dev Set)</th>
                  <th className="p-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border font-medium text-ink">
                {gates.map((g, i) => (
                  <tr key={g.id || i} className="hover:bg-navy-raised/40 transition">
                    <td className="p-3">
                      <div className="font-bold text-ink">{g.name}</div>
                      <div className="text-[11px] text-ink-faint">{g.desc}</div>
                    </td>
                    <td className="p-3 text-center font-mono text-ink-muted">{g.benchmark}</td>
                    <td className="p-3 text-center font-mono font-bold text-ink">{g.goldV1}</td>
                    <td className="p-3 text-center font-mono font-bold text-ink">{g.goldV2}</td>
                    <td className="p-3 text-center">
                      {g.status === 'PASSED' ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-verdict-safe/15 text-verdict-safe border border-verdict-safe/30">
                          <CheckCircle2 className="w-3 h-3" />
                          PASSED
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-verdict-suspicious/15 text-verdict-suspicious border border-verdict-suspicious/30">
                          <AlertCircle className="w-3 h-3" />
                          {g.status}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Multilingual "What does this mean?" Accordion */}
          <div className="rounded-2xl border border-border bg-navy overflow-hidden">
            <button
              onClick={() => setGlossaryOpen(!glossaryOpen)}
              className="w-full p-3.5 flex items-center justify-between text-left hover:bg-navy-raised/50 transition"
              aria-expanded={glossaryOpen}
            >
              <div className="flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-teal" />
                <span className="text-xs font-bold text-ink">
                  {currentGlossary.title}
                </span>
                <span className="text-[10px] text-ink-muted font-normal">
                  (Recall, False Alarms, Calibration in EN / HI / TE)
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono uppercase text-ink-muted">
                  {glossaryLang}
                </span>
                {glossaryOpen ? <ChevronUp className="w-3.5 h-3.5 text-ink-muted" /> : <ChevronDown className="w-3.5 h-3.5 text-ink-muted" />}
              </div>
            </button>

            {glossaryOpen && (
              <div className="p-4 pt-1 border-t border-border space-y-3.5 animate-fade-in">
                
                {/* Language Switcher Buttons */}
                <div className="flex items-center gap-1.5 pt-1">
                  <span className="text-[10px] font-bold text-ink-muted uppercase tracking-wider mr-1">Language:</span>
                  {[
                    { id: 'en', label: 'English' },
                    { id: 'hi', label: 'हिंदी (Hindi)' },
                    { id: 'te', label: 'తెలుగు (Telugu)' }
                  ].map(lang => (
                    <button
                      key={lang.id}
                      onClick={() => setGlossaryLang(lang.id)}
                      className={`px-2 py-0.5 rounded text-[10px] font-bold transition ${
                        glossaryLang === lang.id
                          ? 'bg-gold-500 text-navy-deep shadow-xs'
                          : 'bg-navy-raised text-ink-muted hover:bg-border hover:text-ink'
                      }`}
                    >
                      {lang.label}
                    </button>
                  ))}
                </div>

                {/* 3 Concepts: Recall, False Alarms, Calibration */}
                <div className="space-y-2.5 text-xs">
                  <div className="p-2.5 rounded-xl bg-navy border border-border">
                    <span className="font-bold text-teal block text-[11px] mb-0.5">
                      1. {currentGlossary.recall_term}:
                    </span>
                    <p className="text-ink-muted text-[11px] leading-relaxed">
                      {currentGlossary.recall_def}
                    </p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-navy border border-border">
                    <span className="font-bold text-verdict-safe block text-[11px] mb-0.5">
                      2. {currentGlossary.fpr_term}:
                    </span>
                    <p className="text-ink-muted text-[11px] leading-relaxed">
                      {currentGlossary.fpr_def}
                    </p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-navy border border-border">
                    <span className="font-bold text-gold-400 block text-[11px] mb-0.5">
                      3. {currentGlossary.calib_term}:
                    </span>
                    <p className="text-ink-muted text-[11px] leading-relaxed">
                      {currentGlossary.calib_def}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Performance & Footprint Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1 text-xs">
            <div className="p-3 rounded-2xl bg-navy border border-border flex items-center gap-3">
              <Cpu className="w-5 h-5 text-teal-400 shrink-0" />
              <div>
                <p className="font-extrabold text-ink">{reportData?.latency_p50_ms || '~32 ms (p50)'}</p>
                <p className="text-[11px] text-ink-muted">Multi-detector CPU latency</p>
              </div>
            </div>

            <div className="p-3 rounded-2xl bg-navy border border-border flex items-center gap-3">
              <Database className="w-5 h-5 text-gold-400 shrink-0" />
              <div>
                <p className="font-extrabold text-ink">{reportData?.ram_mb || '< 45 MB RAM'}</p>
                <p className="text-[11px] text-ink-muted">Lightweight offline footprint</p>
              </div>
            </div>

            <div className="p-3 rounded-2xl bg-navy border border-border flex items-center gap-3">
              <ShieldCheck className="w-5 h-5 text-teal-400 shrink-0" />
              <div>
                <p className="font-extrabold text-ink">{reportData?.network_calls || 'Zero Socket Calls'}</p>
                <p className="text-[11px] text-ink-muted">Offline static analysis (runs without internet)</p>
              </div>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
