import React from 'react';
import { AlertCircle, CheckCircle2, ShieldAlert, Cpu, Globe, QrCode, FileText, Users } from 'lucide-react';

export default function EvidenceList({ evidence = [] }) {
  if (!evidence || evidence.length === 0) {
    return (
      <div className="p-4 rounded-xl bg-navy border border-border text-sm text-ink-muted">
        No specific detection signals flagged.
      </div>
    );
  }

  const getSourceIcon = (mod) => {
    switch (mod) {
      case 'RULE_SAFETY_LAYER': return <ShieldAlert className="w-3.5 h-3.5" />;
      case 'NLP_CLASSIFIER': return <Cpu className="w-3.5 h-3.5" />;
      case 'URL_SCANNER': return <Globe className="w-3.5 h-3.5" />;
      case 'QR_PARSER': return <QrCode className="w-3.5 h-3.5" />;
      case 'COMMUNITY_REPUTATION': return <Users className="w-3.5 h-3.5" />;
      default: return <FileText className="w-3.5 h-3.5" />;
    }
  };

  const getSeverityStyle = (sev) => {
    switch (sev) {
      case 'CRITICAL':
        return 'bg-verdict-danger/15 text-verdict-danger border-verdict-danger/40';
      case 'HIGH':
        return 'bg-verdict-suspicious/15 text-verdict-suspicious border-verdict-suspicious/40';
      case 'MEDIUM':
        return 'bg-gold-400/15 text-gold-400 border-gold-500/40';
      case 'INFO':
        return 'bg-verdict-safe/15 text-verdict-safe border-verdict-safe/40';
      default:
        return 'bg-navy text-ink-muted border-border';
    }
  };

  return (
    <div className="space-y-3">
      {evidence.map((item, idx) => (
        <div
          key={idx}
          className="p-3.5 rounded-xl bg-navy-surface/90 border border-border hover:border-teal/40 transition-colors shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3"
        >
          <div className="flex items-start gap-3 flex-1">
            <span className="mt-0.5 text-ink-faint font-mono text-xs">#{idx + 1}</span>
            <div>
              <p className="text-sm font-medium text-ink leading-snug">
                {item.signal}
              </p>
              <div className="mt-1.5 flex items-center gap-2 flex-wrap">
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold bg-navy text-ink-muted border border-border">
                  {getSourceIcon(item.source_module)}
                  {item.source_module.replace('_', ' ')}
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase border ${getSeverityStyle(item.severity)}`}>
                  {item.severity}
                </span>
              </div>
            </div>
          </div>

          <div className="text-right sm:self-center font-mono text-xs font-semibold shrink-0">
            <span className={item.weight > 0 ? 'text-verdict-danger' : 'text-verdict-safe'}>
              {item.weight > 0 ? `+${item.weight}` : item.weight} pts
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
