import React, { useState } from 'react';
import { ShieldCheck, ShieldAlert, AlertTriangle, ArrowRight, CheckCircle2, Info, Users } from 'lucide-react';
import { analyzeVpa, lookupReputation } from '../api/client';

export default function VpaCheckTab() {
  const [vpa, setVpa] = useState('');
  const [payeeName, setPayeeName] = useState('');
  const [amount, setAmount] = useState('');
  const [isCollect, setIsCollect] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleVerify = async (e) => {
    e.preventDefault();
    if (!vpa.trim()) {
      setError('Please enter a UPI ID (e.g. merchant@upi or user@okaxis)');
      return;
    }
    setError('');
    setLoading(true);
    setResult(null);

    try {
      const [data, repData] = await Promise.all([
        analyzeVpa(vpa.trim(), payeeName.trim(), amount, isCollect),
        lookupReputation('vpa', vpa.trim()).catch(() => null)
      ]);
      setResult({ ...data, community_reputation: repData });
    } catch (err) {
      setError(err.message || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFill = (demoVpa, demoName, demoAmt, demoCollect) => {
    setVpa(demoVpa);
    setPayeeName(demoName);
    setAmount(demoAmt);
    setIsCollect(demoCollect);
    setError('');
    setResult(null);
  };

  return (
    <div className="space-y-6 text-ink">
      {/* Introduction Card */}
      <div className="bg-navy-surface/90 p-5 rounded-2xl border border-border">
        <div className="flex items-start gap-3">
          <div className="p-2.5 rounded-xl bg-navy text-teal border border-border">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-ink">
              UPI ID (VPA) Pre-Payment Safe-Check
            </h3>
            <p className="text-xs text-ink-muted mt-1 leading-relaxed">
              Verify unknown UPI IDs and payment requests before authorizing transactions. We audit the banking PSP handle, flag brand impersonation tricks in personal handles, and alert you against dangerous collect-request scams.
            </p>
          </div>
        </div>

        {/* Quick Demo Buttons */}
        <div className="mt-4 pt-3 border-t border-border flex flex-wrap gap-2 items-center text-xs">
          <span className="text-ink-muted text-[11px] font-medium">Quick Demo Samples:</span>
          <button
            onClick={() => handleQuickFill('sbi-helpline-refund@ybl', 'SBI Customer Support', '15000', true)}
            className="px-2.5 py-1 rounded-lg bg-verdict-danger/15 hover:bg-verdict-danger/25 text-rose-600 dark:text-rose-300 border border-verdict-danger/30 font-medium transition-colors"
          >
            Impersonation Collect Trap
          </button>
          <button
            onClick={() => handleQuickFill('rahul.verma@okhdfcbank', 'Rahul Verma', '450', false)}
            className="px-2.5 py-1 rounded-lg bg-verdict-safe/15 hover:bg-verdict-safe/25 text-verdict-safe border border-verdict-safe/30 font-medium transition-colors"
          >
            Safe P2P Contact
          </button>
        </div>
      </div>

      {/* Verification Form */}
      <form onSubmit={handleVerify} className="bg-navy-surface/90 p-6 rounded-2xl border border-border space-y-4">
        <div>
          <label className="text-xs font-semibold text-ink-muted block mb-1.5">
            UPI ID / VPA <span className="text-verdict-danger">*</span>
          </label>
          <input
            type="text"
            autoCapitalize="none"
            autoCorrect="off"
            spellCheck="false"
            value={vpa}
            onChange={(e) => setVpa(e.target.value)}
            placeholder="e.g. name@oksbi, phonepe-support@ybl, 9876543210@paytm"
            className="w-full bg-navy border border-border rounded-xl px-4 py-2.5 text-sm text-ink placeholder:text-ink-faint focus:outline-none focus:border-teal font-mono"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-ink-muted block mb-1.5">
              Claimed Payee / Display Name (Optional)
            </label>
            <input
              type="text"
              value={payeeName}
              onChange={(e) => setPayeeName(e.target.value)}
              placeholder="e.g. SBI Customer Support, OLX Buyer"
              className="w-full bg-navy border border-border rounded-xl px-4 py-2 text-sm text-ink placeholder:text-ink-faint focus:outline-none focus:border-teal"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-ink-muted block mb-1.5">
              Requested Amount in ₹ (Optional)
            </label>
            <input
              type="number"
              inputMode="numeric"
              min="0"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="e.g. 5000"
              className="w-full bg-navy border border-border rounded-xl px-4 py-2 text-sm text-ink placeholder:text-ink-faint focus:outline-none focus:border-teal font-mono"
            />
          </div>
        </div>

        {/* Collect Request Checkbox */}
        <div className="bg-navy p-4 rounded-xl border border-border flex items-start gap-3">
          <input
            type="checkbox"
            id="isCollectReq"
            checked={isCollect}
            onChange={(e) => setIsCollect(e.target.checked)}
            className="mt-1 w-4 h-4 rounded border-border bg-navy text-verdict-danger focus:ring-verdict-danger/20"
          />
          <label htmlFor="isCollectReq" className="text-xs text-ink-muted cursor-pointer">
            <span className="font-bold text-ink block">
              Is this a "Payment / Collect Request" received on your phone?
            </span>
            Check this if your UPI app says "Payment Request from...", "Approve to receive", or asks for your 4/6 digit UPI PIN.
          </label>
        </div>

        {error && (
          <div className="p-3 rounded-lg bg-verdict-danger/15 border border-verdict-danger/30 text-xs text-rose-600 dark:text-rose-300">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="btn-gold-primary w-full py-3 rounded-xl text-sm font-bold shadow-lg transition-all flex items-center justify-center gap-2"
        >
          {loading ? 'Analyzing UPI Handle...' : 'Safe-Check This UPI ID'}
          <ArrowRight className="w-4 h-4" />
        </button>
      </form>

      {/* Analysis Results */}
      {result && (
        <div
          className={`p-6 rounded-2xl border transition-all animate-fade-in ${
            result.verdict === 'HIGH RISK'
              ? 'bg-navy-surface border-verdict-danger/60 border-t-2 border-t-verdict-danger'
              : result.verdict === 'SUSPICIOUS'
              ? 'bg-navy-surface border-verdict-suspicious/60 border-t-2 border-t-verdict-suspicious'
              : 'bg-navy-surface border-verdict-safe/60 border-t-2 border-t-verdict-safe'
          }`}
        >
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border">
            <div>
              <div className="flex items-center gap-2">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-black tracking-wider ${
                    result.verdict === 'HIGH RISK'
                      ? 'bg-verdict-danger/15 text-verdict-danger border border-verdict-danger/40'
                      : result.verdict === 'SUSPICIOUS'
                      ? 'bg-verdict-suspicious/15 text-verdict-suspicious border border-verdict-suspicious/40'
                      : 'bg-verdict-safe/15 text-verdict-safe border border-verdict-safe/40'
                  }`}
                >
                  VERDICT: {result.verdict}
                </span>
                <span className="text-xs text-ink-muted font-mono">
                  Risk Score: {result.risk_score} / 100
                </span>
              </div>
              <h4 className="text-lg font-bold text-ink font-mono mt-2">{result.vpa}</h4>
            </div>

            <div className="text-right sm:border-l sm:border-border sm:pl-4">
              <span className="text-[11px] text-ink-muted uppercase tracking-wider block">PSP Provider</span>
              <span className="text-xs font-semibold text-ink">{result.provider}</span>
            </div>
          </div>

          {/* Warning Notice Banner */}
          <div
            className={`mt-4 p-3.5 rounded-xl text-xs font-medium flex items-start gap-2.5 ${
              result.verdict === 'HIGH RISK'
                ? 'bg-verdict-danger/15 text-rose-600 dark:text-rose-300 border border-verdict-danger/40'
                : result.verdict === 'SUSPICIOUS'
                ? 'bg-verdict-suspicious/15 text-verdict-suspicious border border-verdict-suspicious/40'
                : 'bg-verdict-safe/15 text-emerald-600 dark:text-emerald-300 border border-verdict-safe/40'
            }`}
          >
            {result.verdict === 'HIGH RISK' ? (
              <ShieldAlert className="w-5 h-5 text-verdict-danger shrink-0" />
            ) : result.verdict === 'SUSPICIOUS' ? (
              <AlertTriangle className="w-5 h-5 text-verdict-suspicious shrink-0" />
            ) : (
              <CheckCircle2 className="w-5 h-5 text-verdict-safe shrink-0" />
            )}
            <span>{result.warning_notice}</span>
          </div>

          {/* Community Consensus Reputation Banner */}
          {result.community_reputation && (
            <div className="mt-3 p-3 rounded-xl bg-navy border border-border flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <span className="text-ink-muted font-semibold">Community Reputation:</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                  result.community_reputation.reputation_status === 'KNOWN_SCAM'
                    ? 'bg-verdict-danger/15 text-verdict-danger border border-verdict-danger/40'
                    : result.community_reputation.reputation_status === 'WHITELISTED'
                    ? 'bg-verdict-safe/15 text-verdict-safe border border-verdict-safe/40'
                    : result.community_reputation.reputation_status === 'PENDING_CONSENSUS'
                    ? 'bg-verdict-suspicious/15 text-verdict-suspicious border border-verdict-suspicious/40'
                    : 'bg-navy-raised text-ink-muted'
                }`}>
                  {result.community_reputation.reputation_status}
                </span>
              </div>
              <span className="text-[11px] text-ink-muted">
                {result.community_reputation.distinct_reporters || 0} distinct reporters
              </span>
            </div>
          )}

          {/* Reasons List */}
          <div className="mt-4 space-y-2">
            <span className="text-xs font-bold text-ink-muted block">Analysis Signals:</span>
            <ul className="space-y-1.5">
              {result.reasons.map((r, i) => (
                <li key={i} className="text-xs text-ink flex items-start gap-2">
                  <span className="text-teal font-bold">•</span>
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
