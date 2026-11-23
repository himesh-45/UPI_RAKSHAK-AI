import React, { useState } from 'react';
import { PhoneCall, CheckCircle, XCircle, AlertOctagon, ShieldAlert, FileText, ChevronDown, ChevronUp } from 'lucide-react';

const BANK_FRAUD_DESKS = [
  { bank: 'State Bank of India (SBI)', phone: '1800111109', sms: 'BLOCK to 567676' },
  { bank: 'HDFC Bank', phone: '18002026161', sms: 'Freeze via NetBanking' },
  { bank: 'ICICI Bank', phone: '18001080', sms: 'BLOCK to 9215667788' },
  { bank: 'Axis Bank', phone: '18004190068', sms: 'BLOCK to 56161600' },
  { bank: 'Punjab National Bank (PNB)', phone: '18001802222', sms: 'HOT to 5607040' },
  { bank: 'Bank of Baroda', phone: '18002584455', sms: 'BLOCK to 8422009988' },
];

export default function ActionBox({
  actions = [],
  verdict = 'SAFE',
  prefilled1930 = null,
  onOpen1930Modal = null
}) {
  const [showEmergencyChecklist, setShowEmergencyChecklist] = useState(false);
  const isHighRisk = verdict === 'HIGH RISK' || verdict === 'SUSPICIOUS';

  return (
    <div className="space-y-4">
      {/* 1930 Emergency Helpline Banner */}
      <div className="p-4 rounded-2xl bg-gradient-to-r from-[#0F1D3A] via-[#0B1530] to-[#050A18] text-ink shadow-md border border-[#1E3A5F] border-t-2 border-t-gold-400 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gold-400/10 border border-gold-400/30 text-gold-300">
            <PhoneCall className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider text-gold-300 font-bold">
              National Cyber Crime Reporting Helpline
            </div>
            <div className="text-xl font-extrabold tracking-tight flex items-center gap-2">
              <span className="text-ink">Dial 1930</span>
              <span className="text-xs font-normal text-ink-muted">| 24x7 Toll-Free</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <a
            href="tel:1930"
            className="px-3 py-1.5 rounded-xl bg-verdict-danger hover:bg-rose-500 text-white font-bold text-xs uppercase tracking-wider shadow transition"
          >
            Call 1930
          </a>
          {prefilled1930 && onOpen1930Modal && (
            <button
              onClick={onOpen1930Modal}
              className="px-3 py-1.5 rounded-xl btn-gold-primary text-xs transition inline-flex items-center gap-1 shadow"
            >
              <FileText className="w-3.5 h-3.5" />
              Pre-Filled 1930 Report
            </button>
          )}
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-xl bg-[#070E22] hover:bg-[#0B1530] border border-[#1E3A5F] text-ink-muted hover:text-ink font-semibold text-xs transition"
          >
            cybercrime.gov.in
          </a>
        </div>
      </div>

      {/* Emergency Golden-Hour Mode Toggle */}
      {isHighRisk && (
        <div className="border border-verdict-danger/30 rounded-2xl bg-verdict-danger/10 overflow-hidden">
          <button
            onClick={() => setShowEmergencyChecklist(!showEmergencyChecklist)}
            className="w-full p-3.5 flex items-center justify-between text-left text-xs font-bold text-verdict-danger hover:bg-verdict-danger/15 transition-colors"
          >
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-verdict-danger" />
              <span>EMERGENCY PROTOCOL: "I already entered my PIN or sent money"</span>
            </div>
            {showEmergencyChecklist ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showEmergencyChecklist && (
            <div className="p-4 border-t border-verdict-danger/20 space-y-4 text-xs text-ink-muted">
              <div className="bg-[#0B1530] p-3 rounded-xl border border-verdict-danger/30 leading-relaxed text-ink">
                <strong className="text-verdict-danger">The Golden Hour (First 2-3 Hours):</strong> Money transferred via UPI lands in a scammer's mule bank account before being laundered through ATM withdrawals. Calling <strong className="text-gold-300">1930</strong> immediately enables police to freeze the beneficiary account.
              </div>

              <div className="space-y-2">
                <span className="font-bold text-ink block">Immediate Golden Hour Steps:</span>
                <ol className="list-decimal pl-5 space-y-1.5 text-ink-muted">
                  <li><strong className="text-ink">Call 1930 right now:</strong> Provide the 12-digit UPI UTR number from your bank debit SMS.</li>
                  <li><strong className="text-ink">Block your debit card and NetBanking:</strong> Call your bank's 24x7 fraud desk below.</li>
                  <li><strong className="text-ink">Do not delete chats or SMS:</strong> Take screenshots showing caller phone numbers and timestamps.</li>
                  <li><strong className="text-ink">File formal report:</strong> Use our 1-click pre-filled complaint on cybercrime.gov.in.</li>
                </ol>
              </div>

              {/* Bank Fraud Desk Quick Contacts */}
              <div className="space-y-2">
                <span className="font-bold text-ink block">Bank 24x7 Emergency Fraud Numbers:</span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {BANK_FRAUD_DESKS.map((b, idx) => (
                    <div key={idx} className="p-2.5 rounded-xl bg-[#070E22] border border-[#1E3A5F] flex items-center justify-between">
                      <div>
                        <span className="font-semibold text-ink block text-[11px]">{b.bank}</span>
                        <span className="text-[10px] text-ink-muted">{b.sms}</span>
                      </div>
                      <a
                        href={`tel:${b.phone}`}
                        className="px-2 py-1 rounded-lg bg-verdict-danger hover:bg-rose-500 text-white font-bold text-[10px]"
                      >
                        Call {b.phone}
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Action items list */}
      <div className="p-4 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm">
        <h4 className="text-xs font-bold uppercase tracking-wider text-teal-400 mb-3 flex items-center gap-1.5">
          <AlertOctagon className="w-4 h-4 text-teal-400" />
          Recommended Immediate Action Steps
        </h4>

        <div className="space-y-2.5">
          {actions.map((act, idx) => {
            const isNegative = act.toLowerCase().includes('not') || act.toLowerCase().includes('never') || act.toLowerCase().includes('न करें') || act.toLowerCase().includes('వద్దు');
            return (
              <div key={idx} className="flex items-start gap-2.5 text-xs text-ink-muted">
                {isNegative ? (
                  <XCircle className="w-4 h-4 text-verdict-danger shrink-0 mt-0.5" />
                ) : (
                  <CheckCircle className="w-4 h-4 text-verdict-safe shrink-0 mt-0.5" />
                )}
                <span className="text-ink">{act}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
