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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                Pre-Filled 1930 Formal Cybercrime Complaint
              </h3>
              <p className="text-xs text-slate-400">
                Official Incident Summary formatted for Citizen Financial Cyber Fraud Reporting (CFCFRMS)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-5 text-sm">
          {/* Metadata Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
              <span className="text-[11px] text-slate-400 uppercase tracking-wider block font-medium">Category</span>
              <span className="font-semibold text-slate-200">{summary.incident_category}</span>
            </div>
            <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
              <span className="text-[11px] text-slate-400 uppercase tracking-wider block font-medium">Helpline & Portal</span>
              <span className="font-semibold text-emerald-400">Call 1930 / cybercrime.gov.in</span>
            </div>
          </div>

          {/* Suspect Artifacts */}
          {((summary.suspect_phones && summary.suspect_phones.length > 0) ||
            (summary.suspect_urls && summary.suspect_urls.length > 0) ||
            (summary.suspect_vpas && summary.suspect_vpas.length > 0)) && (
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <span className="text-xs font-bold text-slate-300 block">Extracted Adversary Artifacts:</span>
              <div className="flex flex-wrap gap-2">
                {summary.suspect_phones?.map((p, i) => (
                  <span key={`p-${i}`} className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/30 text-xs font-mono">
                    Phone: {p}
                  </span>
                ))}
                {summary.suspect_urls?.map((u, i) => (
                  <span key={`u-${i}`} className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-300 border border-rose-500/30 text-xs font-mono truncate max-w-xs">
                    URL: {u}
                  </span>
                ))}
                {summary.suspect_vpas?.map((v, i) => (
                  <span key={`v-${i}`} className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/30 text-xs font-mono">
                    VPA: {v}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Formal Complaint Narrative */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-indigo-400" />
                Formal Incident Description (Copy & Paste directly into portal):
              </span>
              <button
                onClick={handleCopy}
                className="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-300" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Copied to Clipboard!' : 'Copy Complaint'}
              </button>
            </div>

            <textarea
              readOnly
              value={narrative}
              rows={8}
              className="w-full bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-slate-300 focus:outline-none focus:border-indigo-500 leading-relaxed resize-none selection:bg-indigo-500 selection:text-white"
            />
          </div>

          <div className="p-3.5 rounded-xl bg-amber-950/20 border border-amber-800/40 text-xs text-amber-200">
            <strong>Golden Hour Protocol:</strong> Lodging this complaint within the first 2-3 hours of an unauthorized transfer increases the probability of freezing the suspect beneficiary account from 14% to over 85%.
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/50 flex items-center justify-between flex-wrap gap-2">
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-400 hover:text-indigo-300"
          >
            Visit National Cyber Crime Portal (cybercrime.gov.in)
            <ExternalLink className="w-3.5 h-3.5" />
          </a>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors"
            >
              Close
            </button>
            <a
              href="tel:1930"
              className="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition-colors inline-flex items-center gap-1.5"
            >
              Call 1930 Now
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
