import React from 'react';
import { AlertCircle, CheckCircle2, ShieldAlert, Cpu, Globe, QrCode, FileText, Users } from 'lucide-react';

export default function EvidenceList({ evidence = [] }) {
  if (!evidence || evidence.length === 0) {
    return (
      <div className="p-4 rounded-xl bg-[#0B1530] border border-[#1E3A5F] text-sm text-[#A9B4CC]">
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
        return 'bg-[#F43F5E]/15 text-[#F43F5E] border-[#F43F5E]/40';
      case 'HIGH':
        return 'bg-[#FB923C]/15 text-[#FB923C] border-[#FB923C]/40';
      case 'MEDIUM':
        return 'bg-[#F5C96A]/15 text-[#F5C96A] border-[#D9A441]/40';
      case 'INFO':
        return 'bg-[#34D399]/15 text-[#34D399] border-[#34D399]/40';
      default:
        return 'bg-[#0B1530] text-[#A9B4CC] border-[#1E3A5F]';
    }
  };

  return (
    <div className="space-y-3">
      {evidence.map((item, idx) => (
        <div
          key={idx}
          className="p-3.5 rounded-xl bg-[#0F1D3A]/90 border border-[#1E3A5F] hover:border-[#35D0C8]/40 transition-colors shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3"
        >
          <div className="flex items-start gap-3 flex-1">
            <span className="mt-0.5 text-[#7C89A6] font-mono text-xs">#{idx + 1}</span>
            <div>
              <p className="text-sm font-medium text-[#F5F1E6] leading-snug">
                {item.signal}
              </p>
              <div className="mt-1.5 flex items-center gap-2 flex-wrap">
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold bg-[#0B1530] text-[#A9B4CC] border border-[#1E3A5F]">
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
            <span className={item.weight > 0 ? 'text-[#F43F5E]' : 'text-[#34D399]'}>
              {item.weight > 0 ? `+${item.weight}` : item.weight} pts
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
