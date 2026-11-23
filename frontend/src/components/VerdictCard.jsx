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

  // Status colors & styles (Strictly semantic: Safe=#34D399, Suspicious=#FB923C, High Risk=#F43F5E)
  const cardBorder = isHighRisk
    ? 'border-[#F43F5E]/40 border-t-2 border-t-[#F43F5E] bg-[#0F1D3A]/90'
    : (isSuspicious
      ? 'border-[#FB923C]/40 border-t-2 border-t-[#FB923C] bg-[#0F1D3A]/90'
      : 'border-[#34D399]/40 border-t-2 border-t-[#34D399] bg-[#0F1D3A]/90');

  const titleColor = isHighRisk ? 'text-[#F43F5E]' : (isSuspicious ? 'text-[#FB923C]' : 'text-[#34D399]');
  const badgeBg = isHighRisk
    ? 'bg-[#F43F5E]/15 text-[#F43F5E] border-[#F43F5E]/30'
    : (isSuspicious
      ? 'bg-[#FB923C]/15 text-[#FB923C] border-[#FB923C]/30'
      : 'bg-[#34D399]/15 text-[#34D399] border-[#34D399]/30');

  return (
    <div className={`mt-3 p-4 rounded-xl border ${cardBorder} shadow-xl backdrop-blur-md text-[#F5F1E6]`}>
      {/* Header Bar */}
      <div className="flex items-center justify-between pb-3 border-b border-[#1E3A5F]">
        <div className="flex items-center gap-2.5">
          {isHighRisk && <ShieldAlert className="w-5 h-5 text-[#F43F5E] animate-pulse" />}
          {isSuspicious && <AlertTriangle className="w-5 h-5 text-[#FB923C]" />}
          {isSafe && <ShieldCheck className="w-5 h-5 text-[#34D399]" />}
          <div>
            <h3 className={`text-xs font-bold font-mono tracking-wider ${titleColor}`}>
              {isHighRisk ? t.highRisk : (isSuspicious ? t.suspicious : t.safe)}
            </h3>
            {category && (
              <span className="text-[10px] text-[#A9B4CC] font-mono">
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
          <span className="text-[10px] font-mono text-[#A9B4CC] mt-1">{t.scoreLabel}</span>
        </div>

        {/* Evidence Chips */}
        <div className="flex-1 w-full space-y-1.5">
          <span className="text-[11px] font-semibold text-[#A9B4CC] uppercase font-mono">
            {t.evidenceTitle}
          </span>
          <div className="space-y-1">
            {topEvidence.map((ev, i) => (
              <div
                key={i}
                className="flex items-center gap-2 px-2.5 py-1 rounded-lg bg-[#0B1530] border border-[#1E3A5F] text-xs text-[#F5F1E6]"
              >
                <span className={`w-1.5 h-1.5 rounded-full ${isHighRisk ? 'bg-[#F43F5E]' : (isSuspicious ? 'bg-[#FB923C]' : 'bg-[#34D399]')}`} />
                <span className="truncate">{ev}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Primary Action Buttons */}
      <div className="mt-4 pt-3 border-t border-[#1E3A5F] flex flex-wrap gap-2">
        {isHighRisk && (
          <>
            {onOpenReport && (
              <button
                onClick={onOpenReport}
                className="flex-1 min-w-[140px] px-3 py-2 rounded-lg bg-[#F43F5E] hover:bg-[#E11D48] text-white text-xs font-semibold flex items-center justify-center gap-1.5 shadow-lg shadow-rose-950/50 transition-all"
              >
                <PhoneCall className="w-3.5 h-3.5" />
                {t.reportBtn}
              </button>
            )}
            {onEmergency && (
              <button
                onClick={onEmergency}
                className="px-3 py-2 rounded-lg bg-[#14254B] hover:bg-[#1E3A5F] text-[#F5F1E6] text-xs font-medium border border-[#1E3A5F] flex items-center gap-1 transition-all"
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
                className="flex-1 min-w-[140px] px-3 py-2 rounded-lg bg-[#FB923C] hover:bg-[#F97316] text-[#050A18] text-xs font-bold flex items-center justify-center gap-1.5 shadow-lg shadow-orange-950/50 transition-all"
              >
                {t.verifyBtn}
              </button>
            )}
            {onOpenReport && (
              <button
                onClick={onOpenReport}
                className="px-3 py-2 rounded-lg bg-[#14254B] hover:bg-[#1E3A5F] text-[#F5F1E6] text-xs font-medium border border-[#1E3A5F] transition-all"
              >
                {t.reportBtn}
              </button>
            )}
          </>
        )}

        {isSafe && onShare && (
          <button
            onClick={onShare}
            className="flex-1 min-w-[140px] px-3 py-2 rounded-lg bg-[#0E8F89] hover:bg-[#1FB5AD] text-white text-xs font-semibold flex items-center justify-center gap-1.5 shadow-lg shadow-teal-950/50 transition-all"
          >
            <Share2 className="w-3.5 h-3.5" />
            {t.shareBtn}
          </button>
        )}
      </div>
    </div>
  );
}
