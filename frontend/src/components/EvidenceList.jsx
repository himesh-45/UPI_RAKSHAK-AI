import React from 'react';
import { AlertCircle, CheckCircle2, ShieldAlert, Cpu, Globe, QrCode, FileText } from 'lucide-react';

export default function EvidenceList({ evidence = [] }) {
  if (!evidence || evidence.length === 0) {
    return (
      <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 text-sm text-slate-500">
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
      default: return <FileText className="w-3.5 h-3.5" />;
    }
  };

  const getSeverityStyle = (sev) => {
    switch (sev) {
      case 'CRITICAL':
        return 'bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-300 border-rose-300 dark:border-rose-800';
      case 'HIGH':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300 border-orange-300 dark:border-orange-800';
      case 'MEDIUM':
        return 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300 border-amber-300 dark:border-amber-800';
      case 'INFO':
        return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800';
      default:
        return 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300 border-slate-300 dark:border-slate-700';
    }
  };

  return (
    <div className="space-y-3">
      {evidence.map((item, idx) => (
        <div
          key={idx}
          className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3"
        >
          <div className="flex items-start gap-3 flex-1">
            <span className="mt-0.5 text-slate-400 font-mono text-xs">#{idx + 1}</span>
            <div>
              <p className="text-sm font-medium text-slate-900 dark:text-slate-100 leading-snug">
                {item.signal}
              </p>
              <div className="mt-1.5 flex items-center gap-2 flex-wrap">
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
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
            <span className={item.weight > 0 ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'}>
              {item.weight > 0 ? `+${item.weight}` : item.weight} pts
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
