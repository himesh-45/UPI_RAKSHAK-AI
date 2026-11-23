import React, { useState, useEffect } from 'react';
import {
  ShieldAlert, ShieldCheck, CheckCircle2, XCircle, AlertTriangle,
  Download, RefreshCw, FileText, ExternalLink, Sparkles, Database,
  Cpu, Activity, Lock, Trash2, Plus, Clock, UserCheck, Eye, X
} from 'lucide-react';
import {
  getAdminSystemInfo, getAdminReports, updateAdminReportStatus,
  getAdminEntities, addAdminEntity, deleteAdminEntity,
  export1930Incidents, getAdminAuditLog
} from '../api/client';

export default function AdminPage({ token, onOpenLogin }) {
  const [activeSubTab, setActiveSubTab] = useState('telemetry'); // 'telemetry', 'inbox', 'entities', 'audit', 'export'
  const [systemInfo, setSystemInfo] = useState(null);
  const [reports, setReports] = useState([]);
  const [reportFilter, setReportFilter] = useState('ALL');
  const [entities, setEntities] = useState([]);
  const [auditLog, setAuditLog] = useState({ total: 0, items: [] });
  const [auditFilter, setAuditFilter] = useState('all');
  const [selectedReport, setSelectedReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Add entity form state
  const [showAddEntity, setShowAddEntity] = useState(false);
  const [newEntityType, setNewEntityType] = useState('vpa');
  const [newEntityValue, setNewEntityValue] = useState('');
  const [newEntityCategory, setNewEntityCategory] = useState('phishing_kyc');

  const loadData = async () => {
    if (!token) return;
    setLoading(true);
    setErrorMessage('');
    try {
      if (activeSubTab === 'telemetry') {
        const info = await getAdminSystemInfo(token);
        setSystemInfo(info);
      } else if (activeSubTab === 'inbox') {
        const reps = await getAdminReports(token, reportFilter);
        setReports(reps);
      } else if (activeSubTab === 'entities') {
        const ents = await getAdminEntities(token);
        setEntities(ents);
      } else if (activeSubTab === 'audit') {
        const logs = await getAdminAuditLog(50, 0, auditFilter, token);
        setAuditLog(logs);
      }
    } catch (err) {
      setErrorMessage(err.message || 'Error loading admin data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [token, activeSubTab, reportFilter, auditFilter]);

  const handleUpdateReportStatus = async (reportId, newStatus) => {
    setActionLoading(true);
    setStatusMessage('');
    try {
      await updateAdminReportStatus(reportId, newStatus, token);
      setStatusMessage(`Report #${reportId} updated to ${newStatus}`);
      const reps = await getAdminReports(token, reportFilter);
      setReports(reps);
      if (selectedReport && selectedReport.id === reportId) {
        setSelectedReport(prev => ({ ...prev, status: newStatus }));
      }
    } catch (err) {
      setErrorMessage(err.message || 'Failed to update report status');
    } finally {
      setActionLoading(false);
    }
  };

  const handleAddEntity = async (e) => {
    e.preventDefault();
    if (!newEntityValue.trim()) return;
    setActionLoading(true);
    try {
      await addAdminEntity(newEntityType, newEntityValue, newEntityCategory, token);
      setStatusMessage(`Entity added to threat intelligence database`);
      setNewEntityValue('');
      setShowAddEntity(false);
      const ents = await getAdminEntities(token);
      setEntities(ents);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to add entity');
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeleteEntity = async (entityId) => {
    if (!window.confirm('Are you sure you want to remove this entity?')) return;
    setActionLoading(true);
    try {
      await deleteAdminEntity(entityId, token);
      setStatusMessage('Entity removed from watch list');
      const ents = await getAdminEntities(token);
      setEntities(ents);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to remove entity');
    } finally {
      setActionLoading(false);
    }
  };

  const handleExport = async (format) => {
    try {
      const res = await export1930Incidents(format, token);
      if (format === 'csv') {
        const url = window.URL.createObjectURL(res);
        const a = document.createElement('a');
        a.href = url;
        a.download = `1930_incident_summary_${new Date().toISOString().slice(0, 10)}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
      } else {
        const blob = new Blob([JSON.stringify(res, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `1930_incident_summary_${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
      }
      setStatusMessage(`1930 incident dossier successfully exported (${format.toUpperCase()})`);
    } catch (err) {
      setErrorMessage(err.message || 'Export failed');
    }
  };

  if (!token) {
    return (
      <div className="max-w-xl mx-auto my-16 px-4 text-center">
        <div className="glass-card rounded-3xl p-8 border border-border space-y-5 shadow-2xl">
          <div className="w-14 h-14 mx-auto rounded-2xl bg-teal/15 text-teal border border-teal/40 flex items-center justify-center">
            <Lock className="w-7 h-7 text-teal" />
          </div>
          <div>
            <h2 className="text-xl font-black text-ink">Admin Authentication Required</h2>
            <p className="text-xs text-ink-muted mt-2 leading-relaxed">
              The Admin Console contains sensitive fraud moderation queues, entity controls, and forensic audit logs. Please sign in with administrator credentials.
            </p>
          </div>
          <button
            onClick={onOpenLogin}
            className="btn-gold-primary px-6 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider shadow-lg"
          >
            Authenticate as Admin
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 animate-fade-in text-ink">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-5">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal/15 text-teal border border-teal/40 text-xs font-bold uppercase tracking-wider mb-1.5">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>Restricted Access Control</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-ink font-display">
            Administrative Operations & Governance Console
          </h1>
          <p className="text-xs text-ink-muted mt-0.5">
            Audit logging, incident moderation, crowdsourced entity registry, and statutory 1930 reporting.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            disabled={loading}
            className="p-2 rounded-xl bg-navy hover:bg-navy-raised text-ink-muted hover:text-teal border border-border transition"
            title="Refresh active view"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Sub-tab Navigation */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none border-b border-border">
        <button
          onClick={() => setActiveSubTab('telemetry')}
          className={`px-4 py-2 rounded-t-xl text-xs font-bold flex items-center gap-2 transition ${
            activeSubTab === 'telemetry'
              ? 'bg-navy-surface text-gold-400 border-b-2 border-gold-500 shadow-xs'
              : 'text-ink-muted hover:text-ink'
          }`}
        >
          <Cpu className="w-3.5 h-3.5 text-teal" />
          <span>System Telemetry</span>
        </button>
        <button
          onClick={() => setActiveSubTab('inbox')}
          className={`px-4 py-2 rounded-t-xl text-xs font-bold flex items-center gap-2 transition ${
            activeSubTab === 'inbox'
              ? 'bg-navy-surface text-gold-400 border-b-2 border-gold-500 shadow-xs'
              : 'text-ink-muted hover:text-ink'
          }`}
        >
          <ShieldAlert className="w-3.5 h-3.5 text-verdict-danger" />
          <span>Moderation Inbox</span>
        </button>
        <button
          onClick={() => setActiveSubTab('entities')}
          className={`px-4 py-2 rounded-t-xl text-xs font-bold flex items-center gap-2 transition ${
            activeSubTab === 'entities'
              ? 'bg-navy-surface text-gold-400 border-b-2 border-gold-500 shadow-xs'
              : 'text-ink-muted hover:text-ink'
          }`}
        >
          <Database className="w-3.5 h-3.5 text-teal" />
          <span>Community Entities</span>
        </button>
        <button
          onClick={() => setActiveSubTab('audit')}
          className={`px-4 py-2 rounded-t-xl text-xs font-bold flex items-center gap-2 transition ${
            activeSubTab === 'audit'
              ? 'bg-navy-surface text-gold-400 border-b-2 border-gold-500 shadow-xs'
              : 'text-ink-muted hover:text-ink'
          }`}
        >
          <FileText className="w-3.5 h-3.5 text-teal" />
          <span>Forensic Audit Log</span>
        </button>
        <button
          onClick={() => setActiveSubTab('export')}
          className={`px-4 py-2 rounded-t-xl text-xs font-bold flex items-center gap-2 transition ${
            activeSubTab === 'export'
              ? 'bg-navy-surface text-gold-400 border-b-2 border-gold-500 shadow-xs'
              : 'text-ink-muted hover:text-ink'
          }`}
        >
          <Download className="w-3.5 h-3.5 text-gold-400" />
          <span>1930 Incident Export</span>
        </button>
      </div>

      {/* Messages */}
      {statusMessage && (
        <div className="p-3 rounded-xl bg-verdict-safe/15 text-[#A7F3D0] border border-verdict-safe/30 text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-verdict-safe shrink-0" />
            <span>{statusMessage}</span>
          </div>
          <button onClick={() => setStatusMessage('')} className="text-ink-muted hover:text-ink">✕</button>
        </div>
      )}
      {errorMessage && (
        <div className="p-3 rounded-xl bg-verdict-danger/15 text-[#FDA4AF] border border-verdict-danger/30 text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-verdict-danger shrink-0" />
            <span>{errorMessage}</span>
          </div>
          <button onClick={() => setErrorMessage('')} className="text-ink-muted hover:text-ink">✕</button>
        </div>
      )}

      {/* TAB 1: System Telemetry */}
      {activeSubTab === 'telemetry' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="glass-card rounded-2xl p-5 border border-border">
              <span className="text-[11px] font-bold text-ink-muted uppercase tracking-wider">Live User Scans</span>
              <div className="text-3xl font-black text-ink font-mono mt-1">
                {systemInfo?.database_counts?.live_user ?? '--'}
              </div>
              <span className="text-[10px] text-teal font-semibold">Real Citizen Activity</span>
            </div>
            <div className="glass-card rounded-2xl p-5 border border-border">
              <span className="text-[11px] font-bold text-ink-muted uppercase tracking-wider">Demo Seed Scans</span>
              <div className="text-3xl font-black text-ink font-mono mt-1">
                {systemInfo?.database_counts?.demo_seed ?? '--'}
              </div>
              <span className="text-[10px] text-gold-400 font-semibold">Evaluation Samples</span>
            </div>
            <div className="glass-card rounded-2xl p-5 border border-border">
              <span className="text-[11px] font-bold text-ink-muted uppercase tracking-wider">Test Traffic</span>
              <div className="text-3xl font-black text-ink font-mono mt-1">
                {systemInfo?.database_counts?.test_traffic ?? '--'}
              </div>
              <span className="text-[10px] text-ink-faint font-semibold">Automated Test Runs</span>
            </div>
            <div className="glass-card rounded-2xl p-5 border border-border">
              <span className="text-[11px] font-bold text-ink-muted uppercase tracking-wider">System Uptime</span>
              <div className="text-2xl font-black text-teal font-mono mt-1">
                {systemInfo?.uptime ?? '--'}
              </div>
              <span className="text-[10px] text-verdict-safe font-semibold">Offline Core Engine Ready</span>
            </div>
          </div>

          <div className="glass-card rounded-3xl p-6 border border-border space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-ink flex items-center gap-2">
              <Cpu className="w-4 h-4 text-teal" />
              Active Detector Architecture & Model Versions
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-3.5 rounded-xl bg-navy border border-border space-y-1">
                <span className="font-bold text-gold-400">NLP Classifier</span>
                <p className="text-ink-muted">{systemInfo?.models?.nlp_classifier || 'Multilingual N-gram Platt Sigmoid'}</p>
              </div>
              <div className="p-3.5 rounded-xl bg-navy border border-border space-y-1">
                <span className="font-bold text-teal">Rule Engine</span>
                <p className="text-ink-muted">{systemInfo?.models?.rule_engine || 'Negation-Aware Rules'}</p>
              </div>
              <div className="p-3.5 rounded-xl bg-navy border border-border space-y-1">
                <span className="font-bold text-verdict-safe">Static URL Scanner</span>
                <p className="text-ink-muted">{systemInfo?.models?.url_scanner || 'Pure Static Structural Scanner'}</p>
              </div>
              <div className="p-3.5 rounded-xl bg-navy border border-border space-y-1">
                <span className="font-bold text-verdict-suspicious">Risk Fusion</span>
                <p className="text-ink-muted">{systemInfo?.models?.risk_fusion || 'Dominant Signal Corroboration'}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: Moderation Inbox */}
      {activeSubTab === 'inbox' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-2 bg-navy p-1 rounded-xl border border-border text-xs font-bold">
              {['ALL', 'PENDING_REVIEW', 'RESOLVED', 'DISMISSED'].map(st => (
                <button
                  key={st}
                  onClick={() => setReportFilter(st)}
                  className={`px-3 py-1.5 rounded-lg transition ${
                    reportFilter === st ? 'bg-gold-500/20 text-gold-400 border border-gold-500/40' : 'text-ink-muted hover:text-ink'
                  }`}
                >
                  {st.replace('_', ' ')}
                </button>
              ))}
            </div>
            <span className="text-xs text-ink-muted font-mono">{reports.length} reports</span>
          </div>

          <div className="glass-card rounded-3xl border border-border overflow-x-auto shadow-md">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-border text-ink-muted font-semibold uppercase text-[10px]">
                  <th className="py-3 px-4">Case #</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Content Preview (Masked)</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Source</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-ink">
                {reports.map(r => (
                  <tr key={r.id} className="hover:bg-navy-raised/40 transition">
                    <td className="py-3 px-4 font-mono font-bold text-teal">#{r.id}</td>
                    <td className="py-3 px-4 text-ink-muted">{r.scam_category.replace(/_/g, ' ')}</td>
                    <td className="py-3 px-4 font-mono text-[11px] max-w-sm truncate text-ink-muted">
                      {r.suspicious_content_masked || 'No preview'}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        r.status === 'RESOLVED'
                          ? 'bg-verdict-safe/15 text-verdict-safe border border-verdict-safe/40'
                          : (r.status === 'DISMISSED'
                              ? 'bg-navy text-ink-faint border border-border'
                              : 'bg-verdict-danger/15 text-verdict-danger border border-verdict-danger/40')
                      }`}>
                        {r.status || 'PENDING'}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-1.5 py-0.5 rounded text-[10px] font-bold uppercase bg-navy border border-border text-ink-muted">
                        {r.data_source}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right space-x-1.5">
                      <button
                        onClick={() => setSelectedReport(r)}
                        className="px-2 py-1 rounded bg-navy text-teal hover:bg-navy-raised border border-border text-[11px] font-semibold"
                      >
                        Inspect
                      </button>
                      {r.status !== 'RESOLVED' && (
                        <button
                          onClick={() => handleUpdateReportStatus(r.id, 'RESOLVED')}
                          disabled={actionLoading}
                          className="px-2 py-1 rounded bg-verdict-safe/15 text-verdict-safe hover:bg-verdict-safe/30 border border-verdict-safe/40 text-[11px] font-semibold"
                        >
                          Resolve
                        </button>
                      )}
                      {r.status !== 'DISMISSED' && (
                        <button
                          onClick={() => handleUpdateReportStatus(r.id, 'DISMISSED')}
                          disabled={actionLoading}
                          className="px-2 py-1 rounded bg-navy text-ink-muted hover:text-ink border border-border text-[11px] font-semibold"
                        >
                          Dismiss
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Detail Drawer for Selected Report */}
      {selectedReport && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-deep/80 backdrop-blur-md animate-fade-in">
          <div className="relative w-full max-w-xl glass-card rounded-3xl p-6 shadow-2xl border border-border text-ink space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <span className="text-xs font-bold uppercase tracking-wider text-teal">
                Incident Dossier #{selectedReport.id}
              </span>
              <button
                onClick={() => setSelectedReport(null)}
                className="w-7 h-7 rounded-lg text-ink-muted hover:text-ink flex items-center justify-center font-bold"
              >
                ✕
              </button>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <span className="font-bold text-ink-muted uppercase text-[10px] block">Category</span>
                <span className="text-sm font-bold text-ink">{selectedReport.scam_category.replace(/_/g, ' ')}</span>
              </div>
              <div>
                <span className="font-bold text-ink-muted uppercase text-[10px] block">Masked Submitted Content</span>
                <div className="p-3 rounded-xl bg-navy font-mono text-[11px] text-ink border border-border mt-1">
                  {selectedReport.suspicious_content_masked || 'None provided'}
                </div>
              </div>
              <div>
                <span className="font-bold text-ink-muted uppercase text-[10px] block">Reporter Comments</span>
                <p className="text-ink-muted mt-0.5">{selectedReport.reporter_comments || 'No comments provided'}</p>
              </div>
              <div className="flex items-center justify-between pt-2 border-t border-border">
                <span className="text-ink-faint">Status: <strong className="text-teal">{selectedReport.status}</strong></span>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleUpdateReportStatus(selectedReport.id, 'RESOLVED')}
                    className="px-3 py-1.5 rounded-xl bg-verdict-safe/20 text-verdict-safe border border-verdict-safe/40 font-bold"
                  >
                    Mark Resolved
                  </button>
                  <button
                    onClick={() => handleUpdateReportStatus(selectedReport.id, 'DISMISSED')}
                    className="px-3 py-1.5 rounded-xl bg-navy text-ink-muted border border-border font-bold hover:text-ink"
                  >
                    Dismiss
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: Community Entities */}
      {activeSubTab === 'entities' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold uppercase tracking-wider text-ink flex items-center gap-2">
              <Database className="w-4 h-4 text-teal" />
              Flagged Community Fraud Entities ({entities.length})
            </h3>
            <button
              onClick={() => setShowAddEntity(!showAddEntity)}
              className="px-3 py-1.5 rounded-xl bg-teal/15 text-teal hover:bg-teal/25 border border-teal/40 text-xs font-bold flex items-center gap-1.5 transition"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>{showAddEntity ? 'Close Form' : 'Add Entity'}</span>
            </button>
          </div>

          {showAddEntity && (
            <form onSubmit={handleAddEntity} className="glass-card rounded-2xl p-4 border border-border space-y-3">
              <span className="text-xs font-bold text-gold-400 uppercase tracking-wider block">Add Entity to Watch Registry</span>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <select
                  value={newEntityType}
                  onChange={e => setNewEntityType(e.target.value)}
                  className="px-3 py-2 rounded-xl bg-navy border border-border text-xs text-ink"
                >
                  <option value="vpa">UPI VPA</option>
                  <option value="phone">Phone Number</option>
                  <option value="domain">Domain</option>
                  <option value="url">URL</option>
                </select>
                <input
                  type="text"
                  required
                  placeholder="e.g. sbi-refunds@paytm or +919876543210"
                  value={newEntityValue}
                  onChange={e => setNewEntityValue(e.target.value)}
                  className="px-3 py-2 rounded-xl bg-navy border border-border text-xs text-ink"
                />
                <select
                  value={newEntityCategory}
                  onChange={e => setNewEntityCategory(e.target.value)}
                  className="px-3 py-2 rounded-xl bg-navy border border-border text-xs text-ink"
                >
                  <option value="phishing_kyc">Bank KYC Phishing</option>
                  <option value="electricity_disconnection">Electricity Bill Fraud</option>
                  <option value="upi_collect_fraud">UPI Collect PIN Fraud</option>
                  <option value="digital_arrest">Digital Arrest Extortion</option>
                  <option value="remote_access_scam">Remote Access (AnyDesk)</option>
                </select>
              </div>
              <button
                type="submit"
                disabled={actionLoading}
                className="btn-gold-primary px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider"
              >
                Register Entity
              </button>
            </form>
          )}

          <div className="glass-card rounded-3xl border border-border overflow-x-auto shadow-md">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-border text-ink-muted font-semibold uppercase text-[10px]">
                  <th className="py-3 px-4">Type</th>
                  <th className="py-3 px-4">Masked Entity Value</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Flags</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-ink">
                {entities.map(e => (
                  <tr key={e.id} className="hover:bg-navy-raised/40 transition">
                    <td className="py-3 px-4 font-mono uppercase text-teal font-bold">{e.entity_type}</td>
                    <td className="py-3 px-4 font-mono text-ink font-semibold">{e.entity_value_masked}</td>
                    <td className="py-3 px-4 text-ink-muted">{e.scam_category.replace(/_/g, ' ')}</td>
                    <td className="py-3 px-4 font-mono font-bold">{e.report_count}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-verdict-danger/15 text-verdict-danger border border-verdict-danger/40 uppercase">
                        {e.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleDeleteEntity(e.id)}
                        className="p-1.5 rounded bg-navy text-verdict-danger hover:bg-navy-raised border border-border"
                        title="Remove entity"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 4: Forensic Audit Log */}
      {activeSubTab === 'audit' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-2 bg-navy p-1 rounded-xl border border-border text-xs font-bold">
              {['all', 'live_user', 'demo_seed', 'test_traffic'].map(ds => (
                <button
                  key={ds}
                  onClick={() => setAuditFilter(ds)}
                  className={`px-3 py-1.5 rounded-lg transition ${
                    auditFilter === ds ? 'bg-gold-500/20 text-gold-400 border border-gold-500/40' : 'text-ink-muted hover:text-ink'
                  }`}
                >
                  {ds === 'all' ? 'All Traffic' : ds.replace('_', ' ')}
                </button>
              ))}
            </div>
            <span className="text-xs text-ink-muted font-mono">{auditLog.total} total logged scans</span>
          </div>

          <div className="glass-card rounded-3xl border border-border overflow-x-auto shadow-md">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-border text-ink-muted font-semibold uppercase text-[10px]">
                  <th className="py-3 px-4">Verdict</th>
                  <th className="py-3 px-4">Score</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Masked Input</th>
                  <th className="py-3 px-4">Channel</th>
                  <th className="py-3 px-4">Source</th>
                  <th className="py-3 px-4 text-right">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-ink">
                {auditLog.items?.map(it => (
                  <tr key={it.id} className="hover:bg-navy-raised/40 transition">
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        it.verdict === 'HIGH RISK'
                          ? 'bg-verdict-danger/15 text-verdict-danger border border-verdict-danger/40'
                          : (it.verdict === 'SUSPICIOUS'
                              ? 'bg-verdict-suspicious/15 text-verdict-suspicious border border-verdict-suspicious/40'
                              : 'bg-verdict-safe/15 text-verdict-safe border border-verdict-safe/40')
                      }`}>
                        {it.verdict}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-ink">{it.risk_score}</td>
                    <td className="py-3 px-4 text-ink-muted">{it.detected_category.replace(/_/g, ' ')}</td>
                    <td className="py-3 px-4 font-mono text-[11px] max-w-xs truncate text-ink-muted">
                      {it.raw_input_masked}
                    </td>
                    <td className="py-3 px-4 uppercase text-[10px] font-bold text-teal">{it.channel}</td>
                    <td className="py-3 px-4">
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                        it.data_source === 'live_user' ? 'bg-gold-500/15 text-gold-400 border border-gold-500/40' : 'bg-navy text-ink-faint'
                      }`}>
                        {it.data_source}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-ink-faint text-[11px]">
                      {it.created_at}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 5: 1930 Incident Export */}
      {activeSubTab === 'export' && (
        <div className="max-w-2xl mx-auto space-y-6 text-center">
          <div className="glass-card rounded-3xl p-8 border border-border space-y-5 shadow-xl">
            <div className="w-14 h-14 mx-auto rounded-2xl bg-gold-400/15 text-gold-400 border border-gold-400/40 flex items-center justify-center">
              <Download className="w-7 h-7 text-gold-400" />
            </div>
            <div>
              <h2 className="text-xl font-black text-ink">Export Incident Dossier for 1930 Cyber Helpline</h2>
              <p className="text-xs text-ink-muted mt-2 leading-relaxed">
                Download structured records of reported cyber fraud incidents formatted for submission to the National Cyber Crime Reporting Portal (cybercrime.gov.in) and state cyber cells.
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-navy border border-gold-500/40 text-gold-300 text-xs font-semibold text-left">
              ⚠️ <strong className="text-ink">Statutory Disclaimer:</strong> Summary prepared to help the user file a complaint; it is not an official complaint or FIR.
            </div>

            <div className="flex items-center justify-center gap-4 pt-2">
              <button
                onClick={() => handleExport('csv')}
                className="btn-gold-primary px-5 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                <span>Export as CSV</span>
              </button>
              <button
                onClick={() => handleExport('json')}
                className="btn-teal-outline px-5 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider flex items-center gap-2"
              >
                <FileText className="w-4 h-4" />
                <span>Export as Masked JSON</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
