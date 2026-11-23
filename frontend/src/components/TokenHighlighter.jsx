import React from 'react';
import { AlertCircle, Link, Phone, ShieldAlert, Zap } from 'lucide-react';

const SEVERITY_COLORS = {
  CRITICAL: 'bg-verdict-danger/20 text-verdict-danger border-verdict-danger/40 hover:bg-verdict-danger/30',
  HIGH: 'bg-verdict-suspicious/20 text-verdict-suspicious border-verdict-suspicious/40 hover:bg-verdict-suspicious/30',
  MEDIUM: 'bg-gold-400/20 text-gold-300 border-gold-400/40 hover:bg-gold-400/30',
  LOW: 'bg-teal-500/20 text-teal-300 border-teal-500/40 hover:bg-teal-500/30',
  INFO: 'bg-navy text-ink-muted border-border hover:bg-navy-surface',
};

const LABEL_ICONS = {
  CREDENTIAL_THEFT: ShieldAlert,
  SUSPICIOUS_LINK: Link,
  URGENCY_THREAT: Zap,
  COLLECT_TRICK: AlertCircle,
  PHONE_NUMBER: Phone,
  REMOTE_APP_TAKEOVER: ShieldAlert,
};

export default function TokenHighlighter({ text, highlightSpans = [] }) {
  if (!text) return null;
  if (!highlightSpans || highlightSpans.length === 0) {
    return <div className="text-ink leading-relaxed font-mono text-sm whitespace-pre-wrap">{text}</div>;
  }

  // Sort spans ascending by start index and filter non-overlapping
  const sorted = [...highlightSpans].sort((a, b) => a.start - b.start);
  const segments = [];
  let lastIdx = 0;

  sorted.forEach((span, idx) => {
    if (span.start < lastIdx) return; // Skip overlapping
    if (span.start > lastIdx) {
      segments.push({
        type: 'text',
        content: text.slice(lastIdx, span.start),
        key: `txt-${lastIdx}`
      });
    }

    segments.push({
      type: 'highlight',
      content: text.slice(span.start, span.end),
      label: span.label,
      severity: span.severity || 'MEDIUM',
      key: `hl-${idx}-${span.start}`
    });

    lastIdx = span.end;
  });

  if (lastIdx < text.length) {
    segments.push({
      type: 'text',
      content: text.slice(lastIdx),
      key: `txt-${lastIdx}`
    });
  }

  return (
    <div className="bg-navy/90 rounded-2xl p-4 border border-border text-sm font-mono leading-loose whitespace-pre-wrap">
      {segments.map((seg) => {
        if (seg.type === 'text') {
          return <span key={seg.key} className="text-ink">{seg.content}</span>;
        }

        const Icon = LABEL_ICONS[seg.label] || AlertCircle;
        const colorClasses = SEVERITY_COLORS[seg.severity] || SEVERITY_COLORS.MEDIUM;

        return (
          <span
            key={seg.key}
            className={`inline-flex items-center gap-1 px-1.5 py-0.5 mx-0.5 rounded border text-xs font-semibold transition-all ${colorClasses}`}
            title={`Evidence Signal: ${seg.label} (${seg.severity})`}
          >
            <Icon className="w-3 h-3 inline-block shrink-0" />
            <span>{seg.content}</span>
            <span className="text-[10px] uppercase opacity-75 font-sans font-bold tracking-wider ml-0.5">
              [{seg.label.replace(/_/g, ' ')}]
            </span>
          </span>
        );
      })}
    </div>
  );
}
