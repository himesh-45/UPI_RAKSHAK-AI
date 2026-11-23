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
    <div className="bg-navy-surface/90 rounded-3xl border border-border shadow-lg p-6 space-y-6 text-ink">
      
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-navy text-teal border border-border">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-extrabold text-ink">
                Admin Governance & Dispute Moderation Queue
              </h2>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-navy text-teal border border-teal/30">
                Live Admin Mode
              </span>
            </div>
            <p className="text-xs text-ink-muted mt-0.5">
              Review community reports, adjudicate merchant false positive appeals, and download research telemetry.
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={fetchQueue}
            disabled={loading}
            className="p-2 rounded-xl bg-navy text-ink-muted hover:text-teal hover:bg-navy-raised border border-border transition"
            title="Refresh queue"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          
          <button
            onClick={handleExportCsv}
            className="px-3 py-1.5 rounded-xl bg-navy-raised hover:bg-border text-gold-400 text-xs font-bold flex items-center gap-1.5 transition border border-gold-500/40"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Study CSV</span>
          </button>

          <button
            onClick={handleSeedDemo}
            disabled={actionLoading}
            className="px-3 py-1.5 rounded-xl bg-navy hover:bg-navy-raised text-teal text-xs font-bold flex items-center gap-1.5 transition border border-teal/40"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Seed Demo Items</span>
          </button>
        </div>
      </div>

      {/* Status Messages */}
      {message && (
        <div className="p-3 rounded-xl bg-verdict-safe/15 text-[#A7F3D0] border border-verdict-safe/30 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-verdict-safe shrink-0" />
          <span>{message}</span>
        </div>
      )}
      {error && (
        <div className="p-3 rounded-xl bg-verdict-danger/15 text-[#FDA4AF] border border-verdict-danger/30 text-xs flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-verdict-danger shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Grid: Active Reports & Pending Disputes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Column 1: Active Community Reports */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-extrabold uppercase tracking-wider text-ink-muted flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-verdict-danger"></span>
              Active Community Scam Reports ({data.active_reports?.length || 0})
            </h3>
            <span className="text-[10px] text-ink-faint">Consensus threshold $\ge 2$</span>
          </div>

          {data.active_reports?.length === 0 ? (
            <div className="p-8 rounded-2xl bg-navy border border-dashed border-border text-center text-xs text-ink-muted">
              No active community reports pending review. Click "Seed Demo Items" to test live adjudication.
            </div>
          ) : (
            <div className="space-y-3">
              {data.active_reports.map((r) => (
                <div
                  key={r.id}
                  className="p-4 rounded-2xl bg-navy border border-border space-y-2.5 transition"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-ink text-xs">
                          {r.masked_display}
                        </span>
                        <span className="px-1.5 py-0.5 rounded text-[9px] font-bold uppercase bg-navy-raised text-ink-muted border border-border">
                          {r.entity_type}
                        </span>
                      </div>
                      <p className="text-[11px] text-teal font-semibold mt-0.5">
                        Category: {r.scam_category.replace(/_/g, ' ')}
                      </p>
                    </div>
                    <span className="text-[10px] text-ink-faint font-mono">
                      Report #{r.id}
                    </span>
                  </div>

                  {r.evidence_text && (
                    <div className="p-2 rounded-xl bg-navy border border-border text-[11px] text-ink-muted">
                      <span className="font-semibold text-ink-faint text-[10px] block">Evidence Notes:</span>
                      {r.evidence_text}
                    </div>
                  )}

                  <div className="flex items-center justify-end gap-2 pt-1">
                    <button
                      onClick={() => handleResolveReport(r.id, 'DISMISS')}
                      disabled={actionLoading}
                      className="px-2.5 py-1 rounded-lg bg-navy-raised hover:bg-border text-ink text-xs font-bold transition flex items-center gap-1 border border-border"
                    >
                      <XCircle className="w-3.5 h-3.5 text-ink-muted" />
                      <span>Dismiss Flag</span>
                    </button>
                    <button
                      onClick={() => handleResolveReport(r.id, 'CONFIRM')}
                      disabled={actionLoading}
                      className="px-2.5 py-1 rounded-lg bg-verdict-danger hover:bg-[#E11D48] text-white text-xs font-bold transition flex items-center gap-1 shadow-xs"
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
            <h3 className="text-xs font-extrabold uppercase tracking-wider text-ink-muted flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-verdict-suspicious"></span>
              Merchant Dispute Appeals ({data.pending_disputes?.length || 0})
            </h3>
            <span className="text-[10px] text-ink-faint">Anti-Competitive Defense</span>
          </div>

          {data.pending_disputes?.length === 0 ? (
            <div className="p-8 rounded-2xl bg-navy border border-dashed border-border text-center text-xs text-ink-muted">
              No merchant disputes pending adjudication.
            </div>
          ) : (
            <div className="space-y-3">
              {data.pending_disputes.map((d) => (
                <div
                  key={d.id}
                  className="p-4 rounded-2xl bg-navy border border-border space-y-2.5 transition"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="font-semibold text-xs text-ink">
                        Claimant: <span className="font-mono text-teal">{d.claimant_email_masked}</span>
                      </p>
                      <p className="text-[10px] text-ink-faint mt-0.5">
                        Dispute #{d.id} {d.created_at ? `• ${d.created_at.slice(0, 10)}` : ''}
                      </p>
                    </div>
                    <span className="px-1.5 py-0.5 rounded text-[9px] font-bold uppercase bg-verdict-suspicious/15 text-verdict-suspicious border border-verdict-suspicious/30">
                      PENDING REVIEW
                    </span>
                  </div>

                  <div className="p-2 rounded-xl bg-navy border border-border text-[11px] text-ink-muted">
                    <span className="font-semibold text-ink-faint text-[10px] block">Claimant Appeal:</span>
                    {d.dispute_reason}
                  </div>

                  {d.proof_url && (
                    <a
                      href={d.proof_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] text-teal hover:underline font-semibold"
                    >
                      <ExternalLink className="w-3 h-3" />
                      <span>Inspect Verification / GST Proof</span>
                    </a>
                  )}

                  <div className="flex items-center justify-end gap-2 pt-1">
                    <button
                      onClick={() => handleResolveDispute(d.id, 'REJECT')}
                      disabled={actionLoading}
                      className="px-2.5 py-1 rounded-lg bg-verdict-danger/15 hover:bg-verdict-danger/25 text-verdict-danger text-xs font-bold transition flex items-center gap-1 border border-verdict-danger/30"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Reject Appeal</span>
                    </button>
                    <button
                      onClick={() => handleResolveDispute(d.id, 'APPROVE')}
                      disabled={actionLoading}
                      className="px-2.5 py-1 rounded-lg bg-[#0E8F89] hover:bg-teal text-white text-xs font-bold transition flex items-center gap-1 shadow-xs"
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
