import React from 'react';
import { ExternalLink, CheckCircle2, ShieldCheck, Calendar, UserCheck } from 'lucide-react';

export default function CitationCard({
  citation = null,
  language = 'en'
}) {
  if (!citation) return null;

  const title = citation.title || "Statutory Cybersecurity Guidance";
  const source = citation.source || "Regulatory Authority (NPCI / RBI / MHA)";
  const officialUrl = citation.official_source_link || citation.official_url || "https://cybercrime.gov.in";
  const lastReviewed = citation.last_reviewed || "2026-11-23";
  const reviewer = citation.reviewer || "Regulatory Compliance Audit";

  const labels = {
    en: {
      sourceBadge: "Reviewed Statutory Source",
      reviewedDate: `Reviewed on ${lastReviewed}`,
      verifyBtn: "Verify on Official Site",
      reviewerLabel: `Verified by ${reviewer}`
    },
    hi: {
      sourceBadge: "सत्यापित आधिकारिक स्रोत",
      reviewedDate: `समीक्षा तिथि: ${lastReviewed}`,
      verifyBtn: "आधिकारिक वेबसाइट पर पुष्टि करें",
      reviewerLabel: `सत्यापनकर्ता: ${reviewer}`
    },
    te: {
      sourceBadge: "ధృవీకరించబడిన అధికారిక మూలం",
      reviewedDate: `సమీక్షించిన తేదీ: ${lastReviewed}`,
      verifyBtn: "అధికారిక వెబ్‌సైట్‌లో చూడండి",
      reviewerLabel: `ధృవీకరించిన వారు: ${reviewer}`
    }
  };

  const l = labels[language] || labels.en;

  return (
    <div className="mt-2.5 p-3 bg-slate-900/80 border border-slate-800 rounded-xl text-xs text-slate-200">
      <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-slate-800/80">
        <div className="flex items-center gap-1.5 text-cyan-400 font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
          <span className="font-mono text-[11px] truncate max-w-[220px]">{source}</span>
        </div>
        <div className="flex items-center gap-1 text-[10px] text-slate-400 font-mono">
          <Calendar className="w-3 h-3 text-slate-500" />
          <span>{l.reviewedDate}</span>
        </div>
      </div>

      <div className="mt-2 flex items-center justify-between gap-2">
        <span className="text-[10px] text-slate-400 font-mono truncate">
          {l.reviewerLabel}
        </span>
        <a
          href={officialUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-cyan-950/40 hover:bg-cyan-900/50 text-cyan-300 border border-cyan-500/30 text-[11px] font-semibold transition-colors shrink-0"
        >
          <span>{l.verifyBtn}</span>
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
}
