import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, AreaChart, Area, Legend
} from 'recharts';
import {
  ShieldAlert, ShieldCheck, AlertTriangle, Activity,
  Database, RefreshCw, Lock, Sparkles, Filter, Info, Shield, CheckCircle
} from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import { getDashboardStats } from '../api/client';

export default function DashboardPage({ token, onOpenLogin }) {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [scope, setScope] = useState('live'); // 'live' (default: Live users only), 'simulated', 'all'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [lastUpdated, setLastUpdated] = useState(() => new Date().toLocaleTimeString());

  const fetchStats = async (selectedScope, silent = false) => {
    if (!silent) setLoading(true);
    setError('');
    try {
      const dataSrc = selectedScope === 'live' ? 'live_user' : (selectedScope === 'simulated' ? 'demo_seed' : 'all');
      const data = await getDashboardStats(selectedScope, dataSrc);
      setStats(data);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      if (!silent) setError(err.message || 'Failed to load intelligence metrics');
    } finally {
      if (!silent) setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats(scope);

    // Live polling: refresh stats every 12 seconds when tab is visible
    const interval = setInterval(() => {
      if (typeof document !== 'undefined' && document.visibilityState === 'visible') {
        fetchStats(scope, true);
      }
    }, 12000);

    const handleVisibility = () => {
      if (document.visibilityState === 'visible') {
        fetchStats(scope, true);
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);

    // Event listener for immediate refresh after any scan finishes
    const handleScanComplete = () => {
      fetchStats(scope, true);
    };
    window.addEventListener('rakshak_scan_completed', handleScanComplete);

    return () => {
      clearInterval(interval);
      document.removeEventListener('visibilitychange', handleVisibility);
      window.removeEventListener('rakshak_scan_completed', handleScanComplete);
    };
  }, [scope]);

  const COLORS = ['#D9A441', '#35D0C8', '#F5C96A', '#34D399', '#1FB5AD', '#FB923C', '#F43F5E'];

  // Prepare chart data
  const categoryChartData = stats?.category_distribution
    ? Object.entries(stats.category_distribution).map(([cat, count]) => ({
        name: cat.replace(/_/g, ' '),
        count
      }))
    : [];

  const langChartData = stats?.language_breakdown
    ? Object.entries(stats.language_breakdown).map(([lang, count]) => ({
        name: lang === 'hi' ? 'Hindi (हिंदी)' : (lang === 'te' ? 'Telugu (తెలుగు)' : 'English'),
        value: count
      }))
    : [];

  const scoreBucketData = stats?.risk_score_distribution
    ? Object.entries(stats.risk_score_distribution).map(([bucket, count]) => ({
        bucket: bucket.split(' ')[0],
        count
      }))
    : [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 animate-fade-in text-ink">
      
      {/* Prominent Simulated Demo Notice Banner */}
      <div className="p-4 rounded-2xl bg-navy-surface/90 border border-gold-500/30 text-gold-400 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs shadow-md">
        <div className="flex items-center gap-2.5">
          <Database className="w-5 h-5 text-gold-500 shrink-0" />
          <div>
            <span className="font-extrabold tracking-wide uppercase">Notice:</span>{' '}
            <span className="text-ink">{t('dashboard.simulatedNotice')}</span>
          </div>
        </div>
        <div className="flex items-center gap-2 font-mono text-[11px] font-bold shrink-0">
          <span className="px-2 py-0.5 rounded bg-navy-raised text-teal border border-teal/30">
            Live: {stats?.seeded_vs_live?.live || 0}
          </span>
          <span className="px-2 py-0.5 rounded bg-navy-raised text-gold-400 border border-gold-500/30">
            Simulated: {stats?.seeded_vs_live?.simulated || 0}
          </span>
        </div>
      </div>

      {/* Header and Scope Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-ink font-display">
            {t('dashboard.title')}
          </h1>
          <p className="text-xs text-ink-muted mt-1">
            Aggregated threat intelligence, signal analytics, and audit logging.
          </p>
        </div>

        {/* Filter scope buttons and Live Sync Indicator */}
        <div className="flex flex-wrap items-center gap-2.5">
          <div className="flex items-center bg-navy p-1 rounded-xl border border-border text-xs font-bold">
            <button
              onClick={() => setScope('live')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'live'
                  ? 'bg-gradient-to-r from-gold-500 to-gold-400 text-navy-deep shadow-xs'
                  : 'text-ink-muted hover:text-ink'
              }`}
            >
              {t('dashboard.filterLive')}
            </button>
            <button
              onClick={() => setScope('simulated')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'simulated'
                  ? 'bg-gradient-to-r from-gold-500 to-gold-400 text-navy-deep shadow-xs'
                  : 'text-ink-muted hover:text-ink'
              }`}
            >
              {t('dashboard.filterSimulated')}
            </button>
            <button
              onClick={() => setScope('all')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'all'
                  ? 'bg-gradient-to-r from-gold-500 to-gold-400 text-navy-deep shadow-xs'
                  : 'text-ink-muted hover:text-ink'
              }`}
            >
              {t('dashboard.filterAll')}
            </button>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[11px] text-ink-faint font-mono hidden sm:inline">
              Last updated {lastUpdated}
            </span>
            <button
              onClick={() => fetchStats(scope)}
              className="p-2 rounded-xl bg-navy text-ink-muted hover:text-teal hover:bg-navy-raised border border-border transition cursor-pointer"
              title="Force Refresh Data"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-teal' : ''}`} />
            </button>
          </div>
        </div>
      </div>

      {/* Community Threat Alerts & Safety Tips Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-navy-surface border border-teal/30 space-y-1 shadow-sm">
          <div className="flex items-center gap-2 text-teal text-xs font-bold uppercase tracking-wider">
            <Shield className="w-4 h-4 text-teal" />
            <span>Rule #1: Receiving Money</span>
          </div>
          <p className="text-xs text-ink-muted leading-relaxed">
            You <strong className="text-ink">NEVER need to enter your UPI PIN</strong> or scan a QR code to receive money. PIN entry always deducts money from your account.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-navy-surface border border-gold-500/30 space-y-1 shadow-sm">
          <div className="flex items-center gap-2 text-gold-400 text-xs font-bold uppercase tracking-wider">
            <AlertTriangle className="w-4 h-4 text-gold-400" />
            <span>Electricity & KYC Phishing</span>
          </div>
          <p className="text-xs text-ink-muted leading-relaxed">
            Electricity boards and banks never threaten immediate disconnection via SMS or WhatsApp from personal 10-digit mobile numbers.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-navy-surface border border-verdict-danger/30 space-y-1 shadow-sm">
          <div className="flex items-center gap-2 text-verdict-danger text-xs font-bold uppercase tracking-wider">
            <ShieldAlert className="w-4 h-4 text-verdict-danger" />
            <span>"Digital Arrest" Extortion</span>
          </div>
          <p className="text-xs text-ink-muted leading-relaxed">
            No police officer, judge, or CBI agent will ever place you under "video arrest" or ask you to transfer funds for "clearance verification".
          </p>
        </div>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-navy-surface/90 border border-border shadow-sm space-y-1">
          <span className="text-xs font-semibold text-ink-muted uppercase tracking-wider">{t('dashboard.totalAnalyses')}</span>
          <div className="text-3xl font-extrabold text-gold-400 font-mono">
            {stats?.total_analyses || 0}
          </div>
          <span className="text-[11px] text-teal font-semibold flex items-center gap-1 font-mono">
            <Activity className="w-3 h-3" /> All Input Formats
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-navy-surface/90 border border-border shadow-sm space-y-1">
          <span className="text-xs font-semibold text-ink-muted uppercase tracking-wider">{t('dashboard.highRiskCount')}</span>
          <div className="text-3xl font-extrabold text-verdict-danger font-mono">
            {stats?.high_risk_count || 0}
          </div>
          <span className="text-[11px] text-verdict-danger font-semibold flex items-center gap-1 font-mono">
            <ShieldAlert className="w-3 h-3" /> Score &ge; 70
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-navy-surface/90 border border-border shadow-sm space-y-1">
          <span className="text-xs font-semibold text-ink-muted uppercase tracking-wider">{t('dashboard.suspiciousCount')}</span>
          <div className="text-3xl font-extrabold text-verdict-suspicious font-mono">
            {stats?.suspicious_count || 0}
          </div>
          <span className="text-[11px] text-verdict-suspicious font-semibold flex items-center gap-1 font-mono">
            <AlertTriangle className="w-3 h-3" /> Score 35–69
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-navy-surface/90 border border-border shadow-sm space-y-1">
          <span className="text-xs font-semibold text-ink-muted uppercase tracking-wider">{t('dashboard.safeCount')}</span>
          <div className="text-3xl font-extrabold text-verdict-safe font-mono">
            {stats?.safe_count || 0}
          </div>
          <span className="text-[11px] text-verdict-safe font-semibold flex items-center gap-1 font-mono">
            <ShieldCheck className="w-3 h-3" /> Score &le; 34
          </span>
        </div>
      </div>

      {/* Omnichannel Distribution Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="p-4 rounded-2xl bg-navy-surface/90 border border-border flex items-center justify-between">
          <div>
            <div className="text-[11px] font-bold text-ink-muted uppercase tracking-wider">Web Portal Scans</div>
            <div className="text-2xl font-extrabold text-ink font-mono mt-0.5">
              {stats?.channel_breakdown?.web || 0}
            </div>
            <div className="text-[10px] text-ink-faint">Desktop & Mobile Web</div>
          </div>
          <span className="text-2xl p-3 bg-navy rounded-xl border border-border">🌐</span>
        </div>

        <div className="p-4 rounded-2xl bg-navy-surface/90 border border-border flex items-center justify-between">
          <div>
            <div className="text-[11px] font-bold text-teal uppercase tracking-wider">Telegram Bot</div>
            <div className="text-2xl font-extrabold text-ink font-mono mt-0.5">
              {stats?.channel_breakdown?.telegram || 0}
            </div>
            <div className="text-[10px] text-ink-faint">Salted SHA-256 Privacy</div>
          </div>
          <span className="text-2xl p-3 bg-navy text-teal rounded-xl border border-border">✈️</span>
        </div>
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Scam Category Breakdown */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-ink uppercase tracking-wider">
            {t('dashboard.categoryDist')}
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryChartData} layout="vertical" margin={{ left: 10, right: 20 }}>
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border)', borderRadius: '12px', fontSize: '12px', color: '#F5F1E6' }}
                />
                <Bar dataKey="count" fill="#D9A441" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 7-Day Timeline Trend */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-ink uppercase tracking-wider">
            7-Day Threat Activity Trend
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.timeline_trend || []}>
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
                <YAxis tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border)', borderRadius: '12px', fontSize: '12px', color: '#F5F1E6' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Area type="monotone" dataKey="high_risk" stackId="1" stroke="#F43F5E" fill="#F43F5E" fillOpacity={0.6} name="High Risk" />
                <Area type="monotone" dataKey="suspicious" stackId="1" stroke="#FB923C" fill="#FB923C" fillOpacity={0.6} name="Suspicious" />
                <Area type="monotone" dataKey="safe" stackId="1" stroke="#34D399" fill="#34D399" fillOpacity={0.6} name="Safe" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Language Breakdown */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-ink uppercase tracking-wider">
            {t('dashboard.languageBreakdown')}
          </h3>
          <div className="h-60 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={langChartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {langChartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border)', borderRadius: '12px', fontSize: '12px', color: '#F5F1E6' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Score Bucket Distribution */}
        <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-ink uppercase tracking-wider">
            {t('dashboard.riskScoreDist')}
          </h3>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={scoreBucketData}>
                <XAxis dataKey="bucket" tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
                <YAxis tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border)', borderRadius: '12px', fontSize: '12px', color: '#F5F1E6' }}
                />
                <Bar dataKey="count" fill="#35D0C8" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Fraud Patterns / Signals Table */}
      <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-ink uppercase tracking-wider">
          Top Triggered Fraud Patterns & Signals
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-border text-ink-muted font-semibold uppercase text-[10px]">
                <th className="py-2.5 px-3">Signal Name</th>
                <th className="py-2.5 px-3">Severity</th>
                <th className="py-2.5 px-3 text-right">Detection Count</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border font-medium text-ink">
              {stats?.top_signals?.map((s, idx) => (
                <tr key={idx} className="hover:bg-navy-raised/30">
                  <td className="py-3 px-3 font-semibold text-ink">{s.signal}</td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase ${
                      s.severity === 'CRITICAL' ? 'bg-verdict-danger/15 text-verdict-danger border border-verdict-danger/40' : 'bg-verdict-suspicious/15 text-verdict-suspicious border border-verdict-suspicious/40'
                    }`}>
                      {s.severity}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold text-ink">
                    {s.count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recent Analysis History Table */}
      <div className="p-6 rounded-3xl bg-navy-surface/90 border border-border shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-ink uppercase tracking-wider">
            {t('dashboard.recentHistory')}
          </h3>
          <span className="text-xs font-semibold text-ink-muted">
            Masked PII for Consumer Privacy
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-border text-ink-muted font-semibold uppercase text-[10px]">
                <th className="py-2.5 px-3">Verdict</th>
                <th className="py-2.5 px-3">Score</th>
                <th className="py-2.5 px-3">Category</th>
                <th className="py-2.5 px-3">Masked Input</th>
                <th className="py-2.5 px-3">Type</th>
                <th className="py-2.5 px-3">Channel</th>
                <th className="py-2.5 px-3">Origin</th>
                <th className="py-2.5 px-3 text-right">Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border font-medium text-ink">
              {stats?.recent_analyses?.map((item) => (
                <tr key={item.id} className="hover:bg-navy-raised/30">
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                      item.verdict === 'HIGH RISK' ? 'bg-verdict-danger/15 text-verdict-danger border border-verdict-danger/40' : (item.verdict === 'SUSPICIOUS' ? 'bg-verdict-suspicious/15 text-verdict-suspicious border border-verdict-suspicious/40' : 'bg-verdict-safe/15 text-verdict-safe border border-verdict-safe/40')
                    }`}>
                      {item.verdict}
                    </span>
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-ink">{item.risk_score}</td>
                  <td className="py-3 px-3 text-ink-muted">{item.detected_category.replace(/_/g, ' ')}</td>
                  <td className="py-3 px-3 font-mono text-[11px] max-w-xs truncate text-ink-muted">{item.raw_input_masked}</td>
                  <td className="py-3 px-3 uppercase text-[10px] text-ink-faint font-bold">{item.input_type}</td>
                  <td className="py-3 px-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                      item.channel === 'telegram'
                        ? 'bg-teal/15 text-teal border border-teal/30'
                        : 'bg-navy-raised text-ink-muted border border-border'
                    }`}>
                      {item.channel || 'web'}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${item.is_simulated ? 'bg-navy text-ink-faint' : 'bg-gold-500/15 text-gold-400 border border-gold-500/40'}`}>
                      {item.is_simulated ? 'SIMULATED' : 'LIVE'}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right text-ink-faint font-mono text-[11px]">{item.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
