import React from 'react';
import { ShieldCheck, ShieldAlert, AlertTriangle, ArrowRight, Share2, PhoneCall, ExternalLink } from 'lucide-react';
import ScoreGauge from './ScoreGauge';

export default function VerdictCard({
  verdict = 'SAFE',
  score = 0,
  signals = [],
  reasons = [],
  category = '',
  language = 'en',
  onOpenReport = null,
  onEmergency = null,
  onShare = null
}) {
  const isHighRisk = verdict === 'HIGH RISK' || verdict === 'DANGER' || score >= 70;
  const isSuspicious = verdict === 'SUSPICIOUS' || verdict === 'WARNING' || (score >= 35 && score < 70);
  const isSafe = !isHighRisk && !isSuspicious;

  const topEvidence = (reasons && reasons.length > 0)
    ? reasons.slice(0, 3)
    : (signals && signals.length > 0 ? signals.slice(0, 3) : ["Standard verified pattern"]);

  const textMap = {
    en: {
      highRisk: "HIGH RISK THREAT DETECTED",
      suspicious: "SUSPICIOUS ACTIVITY DETECTED",
      safe: "NO KNOWN THREAT DETECTED",
      scoreLabel: "Fraud Risk Index",
      evidenceTitle: "Why was this flagged?",
      reportBtn: "Report This Scam (1930)",
      emergencyBtn: "Emergency Action Steps",
      verifyBtn: "How To Verify With Bank",
      shareBtn: "Share Tip With Family",
      recheckBtn: "Check Another Message"
    },
    hi: {
      highRisk: "गंभीर साइबर धोखाधड़ी का खतरा",
      suspicious: "संदिग्ध गतिविधि की पहचान",
      safe: "कोई ज्ञात खतरा नहीं मिला",
      scoreLabel: "धोखाधड़ी जोखिम स्कोर",
      evidenceTitle: "यह क्यों चिन्हित किया गया?",
      reportBtn: "इस घोटाले की शिकायत करें (1930)",
      emergencyBtn: "आपातकालीन सुरक्षा कदम",
      verifyBtn: "बैंक से कैसे पुष्टि करें",
      shareBtn: "परिवार के साथ साझा करें",
      recheckBtn: "अन्य संदेश की जांच करें"
    },
    te: {
      highRisk: "తీవ్రమైన సైబర్ ముప్పు గుర్తించబడింది",
      suspicious: "అనుమానాస్పద లావాదేవీ గుర్తించబడింది",
      safe: "ఎటువంటి ముప్పు గుర్తించబడలేదు",
      scoreLabel: "ఫ్రాడ్ రిస్క్ స్కోర్",
      evidenceTitle: "ఎందుకు హెచ్చరిక జారీ చేయబడింది?",
      reportBtn: "ఈ మోసాన్ని రిపోర్ట్ చేయండి (1930)",
      emergencyBtn: "తక్షణ రక్షణ చర్యలు",
      verifyBtn: "బ్యాంకుతో ఎలా సరిచూసుకోవాలి",
      shareBtn: "కుటుంబంతో పంచుకోండి",
      recheckBtn: "మరో మెసేజ్ తనిఖీ చేయండి"
    }
  };

  const t = textMap[language] || textMap.en;

  // Status colors & styles
  const cardBorder = isHighRisk
    ? 'border-red-500/40 bg-red-950/15'
    : (isSuspicious ? 'border-amber-500/40 bg-amber-950/15' : 'border-emerald-500/40 bg-emerald-950/15');

  const titleColor = isHighRisk ? 'text-red-400' : (isSuspicious ? 'text-amber-400' : 'text-emerald-400');
  const badgeBg = isHighRisk ? 'bg-red-500/20 text-red-300 border-red-500/40' : (isSuspicious ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40');

  return (
    <div className={`mt-3 p-4 rounded-xl border ${cardBorder} shadow-xl backdrop-blur-md text-slate-100`}>
      {/* Header Bar */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          {isHighRisk && <ShieldAlert className="w-5 h-5 text-red-400 animate-pulse" />}
          {isSuspicious && <AlertTriangle className="w-5 h-5 text-amber-400" />}
          {isSafe && <ShieldCheck className="w-5 h-5 text-emerald-400" />}
          <div>
            <h3 className={`text-xs font-bold font-mono tracking-wider ${titleColor}`}>
              {isHighRisk ? t.highRisk : (isSuspicious ? t.suspicious : t.safe)}
            </h3>
            {category && (
              <span className="text-[10px] text-slate-400 font-mono">
                Category: {category.replace(/_/g, ' ')}
              </span>
            )}
          </div>
        </div>

        <span className={`px-2.5 py-1 rounded-full text-xs font-mono font-bold border ${badgeBg}`}>
          {score}/100
        </span>
      </div>

      {/* Main Stats & Visual Gauge */}
      <div className="mt-3.5 flex flex-col sm:flex-row items-center gap-4">
        <div className="shrink-0 flex flex-col items-center">
          <ScoreGauge score={score} size={88} strokeWidth={8} showLabel={false} />
          <span className="text-[10px] font-mono text-slate-400 mt-1">{t.scoreLabel}</span>
        </div>

        {/* Evidence Chips */}
        <div className="flex-1 w-full space-y-1.5">
          <span className="text-[11px] font-semibold text-slate-300 uppercase font-mono">
            {t.evidenceTitle}
          </span>
          <div className="space-y-1">
            {topEvidence.map((ev, i) => (
              <div
                key={i}
                className="flex items-center gap-2 px-2.5 py-1 rounded-lg bg-slate-900/80 border border-slate-800 text-xs text-slate-300"
              >
                <span className={`w-1.5 h-1.5 rounded-full ${isHighRisk ? 'bg-red-400' : (isSuspicious ? 'bg-amber-400' : 'bg-emerald-400')}`} />
                <span className="truncate">{ev}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Primary Action Buttons */}
      <div className="mt-4 pt-3 border-t border-slate-800 flex flex-wrap gap-2">
        {isHighRisk && (
          <>
            {onOpenReport && (
              <button
                onClick={onOpenReport}
                className="flex-1 min-w-[140px] px-3 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-semibold flex items-center justify-center gap-1.5 shadow-lg shadow-red-950/50 transition-all"
              >
                <PhoneCall className="w-3.5 h-3.5" />
                {t.reportBtn}
              </button>
            )}
            {onEmergency && (
              <button
                onClick={onEmergency}
                className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 flex items-center gap-1 transition-all"
              >
                {t.emergencyBtn}
              </button>
            )}
          </>
        )}

        {isSuspicious && (
          <>
            {onEmergency && (
              <button
                onClick={onEmergency}
                className="flex-1 min-w-[140px] px-3 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold flex items-center justify-center gap-1.5 shadow-lg shadow-amber-950/50 transition-all"
              >
                {t.verifyBtn}
              </button>
            )}
            {onOpenReport && (
              <button
                onClick={onOpenReport}
                className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-all"
              >
                {t.reportBtn}
              </button>
            )}
          </>
        )}

        {isSafe && onShare && (
          <button
            onClick={onShare}
            className="flex-1 min-w-[140px] px-3 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold flex items-center justify-center gap-1.5 shadow-lg shadow-emerald-950/50 transition-all"
          >
            <Share2 className="w-3.5 h-3.5" />
            {t.shareBtn}
          </button>
        )}
      </div>
    </div>
  );
}
