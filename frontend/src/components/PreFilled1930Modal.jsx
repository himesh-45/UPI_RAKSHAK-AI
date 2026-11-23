import React, { useState } from 'react';
import { X, Copy, Check, ExternalLink, ShieldAlert, FileText } from 'lucide-react';

export default function PreFilled1930Modal({ isOpen, onClose, summary }) {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !summary) return null;

  const narrative = summary.formal_complaint_narrative || '';

  const handleCopy = () => {
    navigator.clipboard.writeText(narrative);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#050A18]/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-[#0F1D3A] border border-[#1E3A5F] border-t-2 border-t-[#D9A441] w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] text-[#F5F1E6]">
        {/* Header */}
        <div className="p-5 border-b border-[#1E3A5F] flex items-center justify-between bg-[#0B1530]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#0B1530] border border-[#F43F5E]/30 flex items-center justify-center text-[#F43F5E]">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-[#F5F1E6] flex items-center gap-2">
                Pre-Filled 1930 Formal Cybercrime Complaint
              </h3>
              <p className="text-xs text-[#A9B4CC]">
                Official Incident Summary formatted for Citizen Financial Cyber Fraud Reporting (CFCFRMS)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-[#A9B4CC] hover:text-[#F5F1E6] hover:bg-[#14254B] transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-5 text-sm">
          {/* Metadata Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="bg-[#0B1530] p-3 rounded-lg border border-[#1E3A5F]">
              <span className="text-[11px] text-[#A9B4CC] uppercase tracking-wider block font-medium">Category</span>
              <span className="font-semibold text-[#F5F1E6]">{summary.incident_category}</span>
            </div>
            <div className="bg-[#0B1530] p-3 rounded-lg border border-[#1E3A5F]">
              <span className="text-[11px] text-[#A9B4CC] uppercase tracking-wider block font-medium">Helpline & Portal</span>
              <span className="font-semibold text-[#34D399]">Call 1930 / cybercrime.gov.in</span>
            </div>
          </div>

          {/* Suspect Artifacts */}
          {((summary.suspect_phones && summary.suspect_phones.length > 0) ||
            (summary.suspect_urls && summary.suspect_urls.length > 0) ||
            (summary.suspect_vpas && summary.suspect_vpas.length > 0)) && (
            <div className="bg-[#0B1530] p-4 rounded-xl border border-[#1E3A5F] space-y-2">
              <span className="text-xs font-bold text-[#F5F1E6] block">Extracted Adversary Artifacts:</span>
              <div className="flex flex-wrap gap-2">
                {summary.suspect_phones?.map((p, i) => (
                  <span key={`p-${i}`} className="px-2 py-0.5 rounded bg-[#14254B] text-[#35D0C8] border border-[#35D0C8]/30 text-xs font-mono">
                    Phone: {p}
                  </span>
                ))}
                {summary.suspect_urls?.map((u, i) => (
                  <span key={`u-${i}`} className="px-2 py-0.5 rounded bg-[#F43F5E]/15 text-[#FDA4AF] border border-[#F43F5E]/30 text-xs font-mono truncate max-w-xs">
                    URL: {u}
                  </span>
                ))}
                {summary.suspect_vpas?.map((v, i) => (
                  <span key={`v-${i}`} className="px-2 py-0.5 rounded bg-[#14254B] text-[#F5C96A] border border-[#D9A441]/30 text-xs font-mono">
                    VPA: {v}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Formal Complaint Narrative */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-[#F5F1E6] flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-[#35D0C8]" />
                Formal Incident Description (Copy & Paste directly into portal):
              </span>
              <button
                onClick={handleCopy}
                className="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-lg bg-[#14254B] hover:bg-[#1E3A5F] text-[#35D0C8] border border-[#35D0C8]/40 transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-[#34D399]" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Copied to Clipboard!' : 'Copy Complaint'}
              </button>
            </div>

            <textarea
              readOnly
              value={narrative}
              rows={8}
              className="w-full bg-[#070E22] p-4 rounded-xl border border-[#1E3A5F] text-xs font-mono text-[#F5F1E6] focus:outline-none focus:border-[#35D0C8] leading-relaxed resize-none selection:bg-[#35D0C8]/30 selection:text-[#F5F1E6]"
            />
          </div>

          <div className="p-3.5 rounded-xl bg-[#FB923C]/10 border border-[#FB923C]/30 text-xs text-[#FB923C]">
            <strong>Golden Hour Protocol:</strong> Lodging this complaint within the first 2-3 hours of an unauthorized transfer increases the probability of freezing the suspect beneficiary account from 14% to over 85%.
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-[#1E3A5F] bg-[#0B1530] flex items-center justify-between flex-wrap gap-2">
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#35D0C8] hover:text-[#35D0C8]/80"
          >
            Visit National Cyber Crime Portal (cybercrime.gov.in)
            <ExternalLink className="w-3.5 h-3.5" />
          </a>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-[#14254B] hover:bg-[#1E3A5F] text-[#F5F1E6] border border-[#1E3A5F] text-xs font-semibold transition-colors"
            >
              Close
            </button>
            <a
              href="tel:1930"
              className="px-4 py-2 rounded-lg bg-[#F43F5E] hover:bg-[#E11D48] text-white text-xs font-bold transition-colors inline-flex items-center gap-1.5 shadow-md shadow-rose-950/50"
            >
              Call 1930 Now
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
