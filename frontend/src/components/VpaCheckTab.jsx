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
    <div className="space-y-6 text-[#F5F1E6]">
      {/* Introduction Card */}
      <div className="bg-[#0F1D3A]/90 p-5 rounded-2xl border border-[#1E3A5F]">
        <div className="flex items-start gap-3">
          <div className="p-2.5 rounded-xl bg-[#0B1530] text-[#35D0C8] border border-[#1E3A5F]">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-[#F5F1E6]">
              UPI ID (VPA) Pre-Payment Safe-Check
            </h3>
            <p className="text-xs text-[#A9B4CC] mt-1 leading-relaxed">
              Verify unknown UPI IDs and payment requests before authorizing transactions. We audit the banking PSP handle, flag brand impersonation tricks in personal handles, and alert you against dangerous collect-request scams.
            </p>
          </div>
        </div>

        {/* Quick Demo Buttons */}
        <div className="mt-4 pt-3 border-t border-[#1E3A5F] flex flex-wrap gap-2 items-center text-xs">
          <span className="text-[#A9B4CC] text-[11px] font-medium">Quick Demo Samples:</span>
          <button
            onClick={() => handleQuickFill('sbi-helpline-refund@ybl', 'SBI Customer Support', '15000', true)}
            className="px-2.5 py-1 rounded-lg bg-[#F43F5E]/15 hover:bg-[#F43F5E]/25 text-[#FDA4AF] border border-[#F43F5E]/30 font-medium transition-colors"
          >
            Impersonation Collect Trap
          </button>
          <button
            onClick={() => handleQuickFill('rahul.verma@okhdfcbank', 'Rahul Verma', '450', false)}
            className="px-2.5 py-1 rounded-lg bg-[#34D399]/15 hover:bg-[#34D399]/25 text-[#34D399] border border-[#34D399]/30 font-medium transition-colors"
          >
            Safe P2P Contact
          </button>
        </div>
      </div>

      {/* Verification Form */}
      <form onSubmit={handleVerify} className="bg-[#0F1D3A]/90 p-6 rounded-2xl border border-[#1E3A5F] space-y-4">
        <div>
          <label className="text-xs font-semibold text-[#A9B4CC] block mb-1.5">
            UPI ID / VPA <span className="text-[#F43F5E]">*</span>
          </label>
          <input
            type="text"
            value={vpa}
            onChange={(e) => setVpa(e.target.value)}
            placeholder="e.g. name@oksbi, phonepe-support@ybl, 9876543210@paytm"
            className="w-full bg-[#070E22] border border-[#1E3A5F] rounded-xl px-4 py-2.5 text-sm text-[#F5F1E6] placeholder-[#7C89A6] focus:outline-none focus:border-[#35D0C8] font-mono"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#A9B4CC] block mb-1.5">
              Claimed Payee / Display Name (Optional)
            </label>
            <input
              type="text"
              value={payeeName}
              onChange={(e) => setPayeeName(e.target.value)}
              placeholder="e.g. SBI Customer Support, OLX Buyer"
              className="w-full bg-[#070E22] border border-[#1E3A5F] rounded-xl px-4 py-2 text-sm text-[#F5F1E6] placeholder-[#7C89A6] focus:outline-none focus:border-[#35D0C8]"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-[#A9B4CC] block mb-1.5">
              Requested Amount in ₹ (Optional)
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="e.g. 5000"
              className="w-full bg-[#070E22] border border-[#1E3A5F] rounded-xl px-4 py-2 text-sm text-[#F5F1E6] placeholder-[#7C89A6] focus:outline-none focus:border-[#35D0C8] font-mono"
            />
          </div>
        </div>

        {/* Collect Request Checkbox */}
        <div className="bg-[#0B1530] p-4 rounded-xl border border-[#1E3A5F] flex items-start gap-3">
          <input
            type="checkbox"
            id="isCollectReq"
            checked={isCollect}
            onChange={(e) => setIsCollect(e.target.checked)}
            className="mt-1 w-4 h-4 rounded border-[#1E3A5F] bg-[#070E22] text-[#F43F5E] focus:ring-[#F43F5E]/20"
          />
          <label htmlFor="isCollectReq" className="text-xs text-[#A9B4CC] cursor-pointer">
            <span className="font-bold text-[#F5F1E6] block">
              Is this a "Payment / Collect Request" received on your phone?
            </span>
            Check this if your UPI app says "Payment Request from...", "Approve to receive", or asks for your 4/6 digit UPI PIN.
          </label>
        </div>

        {error && (
          <div className="p-3 rounded-lg bg-[#F43F5E]/15 border border-[#F43F5E]/30 text-xs text-[#FDA4AF]">
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
              ? 'bg-[#0F1D3A] border-[#F43F5E]/60 border-t-2 border-t-[#F43F5E]'
              : result.verdict === 'SUSPICIOUS'
              ? 'bg-[#0F1D3A] border-[#FB923C]/60 border-t-2 border-t-[#FB923C]'
              : 'bg-[#0F1D3A] border-[#34D399]/60 border-t-2 border-t-[#34D399]'
          }`}
        >
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#1E3A5F]">
            <div>
              <div className="flex items-center gap-2">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-black tracking-wider ${
                    result.verdict === 'HIGH RISK'
                      ? 'bg-[#F43F5E]/15 text-[#F43F5E] border border-[#F43F5E]/40'
                      : result.verdict === 'SUSPICIOUS'
                      ? 'bg-[#FB923C]/15 text-[#FB923C] border border-[#FB923C]/40'
                      : 'bg-[#34D399]/15 text-[#34D399] border border-[#34D399]/40'
                  }`}
                >
                  VERDICT: {result.verdict}
                </span>
                <span className="text-xs text-[#A9B4CC] font-mono">
                  Risk Score: {result.risk_score} / 100
                </span>
              </div>
              <h4 className="text-lg font-bold text-[#F5F1E6] font-mono mt-2">{result.vpa}</h4>
            </div>

            <div className="text-right sm:border-l sm:border-[#1E3A5F] sm:pl-4">
              <span className="text-[11px] text-[#A9B4CC] uppercase tracking-wider block">PSP Provider</span>
              <span className="text-xs font-semibold text-[#F5F1E6]">{result.provider}</span>
            </div>
          </div>

          {/* Warning Notice Banner */}
          <div
            className={`mt-4 p-3.5 rounded-xl text-xs font-medium flex items-start gap-2.5 ${
              result.verdict === 'HIGH RISK'
                ? 'bg-[#F43F5E]/15 text-[#FDA4AF] border border-[#F43F5E]/40'
                : result.verdict === 'SUSPICIOUS'
                ? 'bg-[#FB923C]/15 text-[#FB923C] border border-[#FB923C]/40'
                : 'bg-[#34D399]/15 text-[#A7F3D0] border border-[#34D399]/40'
            }`}
          >
            {result.verdict === 'HIGH RISK' ? (
              <ShieldAlert className="w-5 h-5 text-[#F43F5E] shrink-0" />
            ) : result.verdict === 'SUSPICIOUS' ? (
              <AlertTriangle className="w-5 h-5 text-[#FB923C] shrink-0" />
            ) : (
              <CheckCircle2 className="w-5 h-5 text-[#34D399] shrink-0" />
            )}
            <span>{result.warning_notice}</span>
          </div>

          {/* Community Consensus Reputation Banner */}
          {result.community_reputation && (
            <div className="mt-3 p-3 rounded-xl bg-[#0B1530] border border-[#1E3A5F] flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <span className="text-[#A9B4CC] font-semibold">Community Reputation:</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                  result.community_reputation.reputation_status === 'KNOWN_SCAM'
                    ? 'bg-[#F43F5E]/15 text-[#F43F5E] border border-[#F43F5E]/40'
                    : result.community_reputation.reputation_status === 'WHITELISTED'
                    ? 'bg-[#34D399]/15 text-[#34D399] border border-[#34D399]/40'
                    : result.community_reputation.reputation_status === 'PENDING_CONSENSUS'
                    ? 'bg-[#FB923C]/15 text-[#FB923C] border border-[#FB923C]/40'
                    : 'bg-[#14254B] text-[#A9B4CC]'
                }`}>
                  {result.community_reputation.reputation_status}
                </span>
              </div>
              <span className="text-[11px] text-[#A9B4CC]">
                {result.community_reputation.distinct_reporters || 0} distinct reporters
              </span>
            </div>
          )}

          {/* Reasons List */}
          <div className="mt-4 space-y-2">
            <span className="text-xs font-bold text-[#A9B4CC] block">Analysis Signals:</span>
            <ul className="space-y-1.5">
              {result.reasons.map((r, i) => (
                <li key={i} className="text-xs text-[#F5F1E6] flex items-start gap-2">
                  <span className="text-[#35D0C8] font-bold">•</span>
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
