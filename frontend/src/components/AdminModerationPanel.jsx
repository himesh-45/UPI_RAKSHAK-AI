import React, { useState, useEffect } from 'react';
import {
  ShieldAlert, ShieldCheck, CheckCircle2, XCircle, AlertTriangle,
  Download, RefreshCw, FileText, ExternalLink, Sparkles
} from 'lucide-react';
import {
  getPendingModeration, resolveModerationReport, resolveModerationDispute,
  seedDemoModeration, exportStudyCsv
} from '../api/client';

export default function AdminModerationPanel({ token }) {
  const [data, setData] = useState({ active_reports: [], pending_disputes: [] });
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const fetchQueue = async () => {
    if (!token) return;
    setLoading(true);
    setError('');
    try {
      const res = await getPendingModeration(token);
      setData(res);
    } catch (err) {
      setError(err.message || 'Failed to load moderation items');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
  }, [token]);

  const handleResolveReport = async (reportId, action) => {
    setActionLoading(true);
    setMessage('');
    setError('');
    try {
      await resolveModerationReport(reportId, action, token);
      setMessage(`Report #${reportId} successfully marked as ${action}.`);
      await fetchQueue();
    } catch (err) {
      setError(err.message || 'Failed to resolve report');
    } finally {
      setActionLoading(false);
    }
  };

  const handleResolveDispute = async (disputeId, action) => {
    setActionLoading(true);
    setMessage('');
    setError('');
    try {
      await resolveModerationDispute(disputeId, action, token);
      setMessage(`Dispute #${disputeId} successfully marked as ${action}.`);
      await fetchQueue();
    } catch (err) {
      setError(err.message || 'Failed to resolve dispute');
    } finally {
      setActionLoading(false);
    }
  };

  const handleSeedDemo = async () => {
    setActionLoading(true);
    setMessage('');
    setError('');
    try {
      await seedDemoModeration(token);
      setMessage('Demo report & merchant dispute injected for live review testing.');
      await fetchQueue();
    } catch (err) {
      setError(err.message || 'Failed to seed demo items');
    } finally {
      setActionLoading(false);
    }
  };

  const handleExportCsv = async () => {
    try {
      const blob = await exportStudyCsv(token);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `upi_rakshak_study_telemetry_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
      setMessage('Research study CSV exported successfully.');
    } catch (err) {
      setError(err.message || 'CSV export failed');
    }
  };

  return (
    <div className="bg-[#0F1D3A]/90 rounded-3xl border border-[#1E3A5F] shadow-lg p-6 space-y-6 text-[#F5F1E6]">
      
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#1E3A5F]">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-[#0B1530] text-[#35D0C8] border border-[#1E3A5F]">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-extrabold text-[#F5F1E6]">
                Admin Governance & Dispute Moderation Queue
              </h2>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#0B1530] text-[#35D0C8] border border-[#35D0C8]/30">
                Live Admin Mode
              </span>
            </div>
            <p className="text-xs text-[#A9B4CC] mt-0.5">
              Review community reports, adjudicate merchant false positive appeals, and download research telemetry.
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={fetchQueue}
            disabled={loading}
            className="p-2 rounded-xl bg-[#0B1530] text-[#A9B4CC] hover:text-[#35D0C8] hover:bg-[#14254B] border border-[#1E3A5F] transition"
            title="Refresh queue"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          
          <button
            onClick={handleExportCsv}
            className="px-3 py-1.5 rounded-xl bg-[#14254B] hover:bg-[#1E3A5F] text-[#F5C96A] text-xs font-bold flex items-center gap-1.5 transition border border-[#D9A441]/40"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Study CSV</span>
          </button>

          <button
            onClick={handleSeedDemo}
            disabled={actionLoading}
            className="px-3 py-1.5 rounded-xl bg-[#0B1530] hover:bg-[#14254B] text-[#35D0C8] text-xs font-bold flex items-center gap-1.5 transition border border-[#35D0C8]/40"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Seed Demo Items</span>
          </button>
        </div>
      </div>

      {/* Status Messages */}
      {message && (
        <div className="p-3 rounded-xl bg-[#34D399]/15 text-[#A7F3D0] border border-[#34D399]/30 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-[#34D399] shrink-0" />
          <span>{message}</span>
        </div>
      )}
      {error && (
        <div className="p-3 rounded-xl bg-[#F43F5E]/15 text-[#FDA4AF] border border-[#F43F5E]/30 text-xs flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-[#F43F5E] shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Grid: Active Reports & Pending Disputes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Column 1: Active Community Reports */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-extrabold uppercase tracking-wider text-[#A9B4CC] flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#F43F5E]"></span>
              Active Community Scam Reports ({data.active_reports?.length || 0})
            </h3>
            <span className="text-[10px] text-[#7C89A6]">Consensus threshold $\ge 2$</span>
          </div>

          {data.active_reports?.length === 0 ? (
            <div className="p-8 rounded-2xl bg-[#0B1530] border border-dashed border-[#1E3A5F] text-center text-xs text-[#A9B4CC]">
              No active community reports pending review. Click "Seed Demo Items" to test live adjudication.
            </div>
          ) : (
            <div className="space-y-3">
              {data.active_reports.map((r) => (
                <div
                  key={r.id}
                  className="p-4 rounded-2xl bg-[#0B1530] border border-[#1E3A5F] space-y-2.5 transition"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-[#F5F1E6] text-xs">
                          {r.masked_display}
                        </span>
                        <span className="px-1.5 py-0.5 rounded text-[9px] font-bold uppercase bg-[#14254B] text-[#A9B4CC] border border-[#1E3A5F]">
                          {r.entity_type}
                        </span>
                      </div>
                      <p className="text-[11px] text-[#35D0C8] font-semibold mt-0.5">
                        Category: {r.scam_category.replace(/_/g, ' ')}
                      </p>
                    </div>
                    <span className="text-[10px] text-[#7C89A6] font-mono">
                      Report #{r.id}
                    </span>
                  </div>

                  {r.evidence_text && (
                    <div className="p-2 rounded-xl bg-[#070E22] border border-[#1E3A5F] text-[11px] text-[#A9B4CC]">
                      <span className="font-semibold text-[#7C89A6] text-[10px] block">Evidence Notes:</span>
                      {r.evidence_text}
                    </div>
                  )}

                  <div className="flex items-center justify-end gap-2 pt-1">
                    <button
                      onClick={() => handleResolveReport(r.id, 'DISMISS')}
                      disabled={actionLoading}
                      className="px-2.5 py-1 rounded-lg bg-[#14254B] hover:bg-[#1E3A5F] text-[#F5F1E6] text-xs font-bold transition flex items-center gap-1 border border-[#1E3A5F]"
                    >
                      <XCircle className="w-3.5 h-3.5 text-[#A9B4CC]" />
                      <span>Dismiss Flag</span>
                    </button>
                    <button
                      onClick={() => handleResolveReport(r.id, 'CONFIRM')}
                      disabled={actionLoading}
                      className="px-2.5 py-1 rounded-lg bg-[#F43F5E] hover:bg-[#E11D48] text-white text-xs font-bold transition flex items-center gap-1 shadow-xs"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Confirm Scam (Blacklist)</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Column 2: Pending Merchant Disputes */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-extrabold uppercase tracking-wider text-[#A9B4CC] flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#FB923C]"></span>
              Merchant Dispute Appeals ({data.pending_disputes?.length || 0})
            </h3>
            <span className="text-[10px] text-[#7C89A6]">Anti-Competitive Defense</span>
          </div>

          {data.pending_disputes?.length === 0 ? (
            <div className="p-8 rounded-2xl bg-[#0B1530] border border-dashed border-[#1E3A5F] text-center text-xs text-[#A9B4CC]">
              No merchant disputes pending adjudication.
            </div>
          ) : (
            <div className="space-y-3">
              {data.pending_disputes.map((d) => (
                <div
                  key={d.id}
                  className="p-4 rounded-2xl bg-[#0B1530] border border-[#1E3A5F] space-y-2.5 transition"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="font-semibold text-xs text-[#F5F1E6]">
                        Claimant: <span className="font-mono text-[#35D0C8]">{d.claimant_email_masked}</span>
                      </p>
                      <p className="text-[10px] text-[#7C89A6] mt-0.5">
                        Dispute #{d.id} {d.created_at ? `• ${d.created_at.slice(0, 10)}` : ''}
                      </p>
                    </div>
                    <span className="px-1.5 py-0.5 rounded text-[9px] font-bold uppercase bg-[#FB923C]/15 text-[#FB923C] border border-[#FB923C]/30">
                      PENDING REVIEW
                    </span>
                  </div>

                  <div className="p-2 rounded-xl bg-[#070E22] border border-[#1E3A5F] text-[11px] text-[#A9B4CC]">
                    <span className="font-semibold text-[#7C89A6] text-[10px] block">Claimant Appeal:</span>
                    {d.dispute_reason}
                  </div>

                  {d.proof_url && (
                    <a
                      href={d.proof_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] text-[#35D0C8] hover:underline font-semibold"
                    >
                      <ExternalLink className="w-3 h-3" />
                      <span>Inspect Verification / GST Proof</span>
                    </a>
                  )}

                  <div className="flex items-center justify-end gap-2 pt-1">
                    <button
                      onClick={() => handleResolveDispute(d.id, 'REJECT')}
                      disabled={actionLoading}
                      className="px-2.5 py-1 rounded-lg bg-[#F43F5E]/15 hover:bg-[#F43F5E]/25 text-[#F43F5E] text-xs font-bold transition flex items-center gap-1 border border-[#F43F5E]/30"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Reject Appeal</span>
                    </button>
                    <button
                      onClick={() => handleResolveDispute(d.id, 'APPROVE')}
                      disabled={actionLoading}
                      className="px-2.5 py-1 rounded-lg bg-[#0E8F89] hover:bg-[#1FB5AD] text-white text-xs font-bold transition flex items-center gap-1 shadow-xs"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Approve (Clear Entity)</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
