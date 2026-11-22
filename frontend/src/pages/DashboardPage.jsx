import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, AreaChart, Area, Legend
} from 'recharts';
import {
  ShieldAlert, ShieldCheck, AlertTriangle, Activity,
  Database, RefreshCw, Lock, Sparkles, Filter
} from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import { getDashboardStats } from '../api/client';
import AdminModerationPanel from '../components/AdminModerationPanel';

export default function DashboardPage({ token, onOpenLogin }) {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [scope, setScope] = useState('all'); // 'all', 'live', 'simulated'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchStats = async (selectedScope) => {
    setLoading(true);
    setError('');
    try {
      const data = await getDashboardStats(selectedScope);
      setStats(data);
    } catch (err) {
      setError(err.message || 'Failed to load intelligence metrics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats(scope);
  }, [scope]);

  const COLORS = ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ef4444', '#14b8a6'];

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
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 animate-fade-in">
      
      {/* Prominent Simulated Demo Notice Banner */}
      <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-800 dark:text-amber-300 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2.5">
          <Database className="w-5 h-5 text-amber-500 shrink-0" />
          <div>
            <span className="font-extrabold tracking-wide uppercase">Notice:</span>{' '}
            <span>{t('dashboard.simulatedNotice')}</span>
          </div>
        </div>
        <div className="flex items-center gap-2 font-mono text-[11px] font-bold shrink-0">
          <span className="px-2 py-0.5 rounded bg-amber-500/20">
            Live: {stats?.seeded_vs_live?.live || 0}
          </span>
          <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-700 dark:text-indigo-300">
            Simulated: {stats?.seeded_vs_live?.simulated || 0}
          </span>
        </div>
      </div>

      {/* Header and Scope Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            {t('dashboard.title')}
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Aggregated threat intelligence, signal analytics, and audit logging.
          </p>
        </div>

        {/* Filter scope buttons */}
        <div className="flex items-center gap-2">
          <div className="flex items-center bg-slate-100 dark:bg-slate-900 p-1 rounded-xl border border-slate-200 dark:border-slate-800 text-xs font-bold">
            <button
              onClick={() => setScope('all')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'all'
                  ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-xs'
                  : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              {t('dashboard.filterAll')}
            </button>
            <button
              onClick={() => setScope('live')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'live'
                  ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-xs'
                  : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              {t('dashboard.filterLive')}
            </button>
            <button
              onClick={() => setScope('simulated')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'simulated'
                  ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-xs'
                  : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              {t('dashboard.filterSimulated')}
            </button>
          </div>

          <button
            onClick={() => fetchStats(scope)}
            className="p-2 rounded-xl bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 transition"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Admin Governance & Dispute Moderation Panel (Visible when Admin signed in or login prompt) */}
      {token ? (
        <AdminModerationPanel token={token} />
      ) : (
        <div className="p-4 rounded-2xl bg-indigo-50/70 dark:bg-indigo-950/30 border border-indigo-200 dark:border-indigo-900/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2.5">
            <Lock className="w-5 h-5 text-indigo-500 shrink-0" />
            <div>
              <span className="font-extrabold text-slate-900 dark:text-white">Admin Dispute Moderation & Research Export:</span>{' '}
              <span className="text-slate-600 dark:text-slate-300">
                Sign in as Admin to review community VPA reports, adjudicate merchant false positive appeals, and export study telemetry.
              </span>
            </div>
          </div>
          <button
            onClick={onOpenLogin}
            className="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs uppercase tracking-wider shrink-0 transition shadow-xs"
          >
            Sign In as Admin
          </button>
        </div>
      )}

      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{t('dashboard.totalAnalyses')}</span>
          <div className="text-3xl font-extrabold text-slate-900 dark:text-white">
            {stats?.total_analyses || 0}
          </div>
          <span className="text-[11px] text-indigo-500 font-semibold flex items-center gap-1">
            <Activity className="w-3 h-3" /> All Input Formats
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{t('dashboard.highRiskCount')}</span>
          <div className="text-3xl font-extrabold text-rose-600 dark:text-rose-400">
            {stats?.high_risk_count || 0}
          </div>
          <span className="text-[11px] text-rose-500 font-semibold flex items-center gap-1">
            <ShieldAlert className="w-3 h-3" /> Score &ge; 70
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{t('dashboard.suspiciousCount')}</span>
          <div className="text-3xl font-extrabold text-amber-500">
            {stats?.suspicious_count || 0}
          </div>
          <span className="text-[11px] text-amber-500 font-semibold flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" /> Score 35–69
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{t('dashboard.safeCount')}</span>
          <div className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400">
            {stats?.safe_count || 0}
          </div>
          <span className="text-[11px] text-emerald-500 font-semibold flex items-center gap-1">
            <ShieldCheck className="w-3 h-3" /> Score &le; 34
          </span>
        </div>
      </div>

      {/* Omnichannel Distribution Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div>
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Web Portal Scans</div>
            <div className="text-2xl font-extrabold text-slate-900 dark:text-white mt-0.5">
              {stats?.channel_breakdown?.web || 0}
            </div>
            <div className="text-[10px] text-slate-400">Desktop & Mobile Web</div>
          </div>
          <span className="text-2xl p-3 bg-white dark:bg-slate-800 rounded-xl shadow-xs border border-slate-200 dark:border-slate-700">🌐</span>
        </div>

        <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div>
            <div className="text-[11px] font-bold text-sky-600 dark:text-sky-400 uppercase tracking-wider">Telegram Bot</div>
            <div className="text-2xl font-extrabold text-slate-900 dark:text-white mt-0.5">
              {stats?.channel_breakdown?.telegram || 0}
            </div>
            <div className="text-[10px] text-slate-400">Salted SHA-256 Privacy</div>
          </div>
          <span className="text-2xl p-3 bg-sky-50 dark:bg-sky-950/60 text-sky-500 rounded-xl shadow-xs border border-sky-200 dark:border-sky-800">✈️</span>
        </div>

        <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div>
            <div className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">WhatsApp Bot</div>
            <div className="text-2xl font-extrabold text-slate-900 dark:text-white mt-0.5">
              {stats?.channel_breakdown?.whatsapp || 0}
            </div>
            <div className="text-[10px] text-slate-400">Twilio Sandbox & Meta Cloud API</div>
          </div>
          <span className="text-2xl p-3 bg-emerald-50 dark:bg-emerald-950/60 text-emerald-500 rounded-xl shadow-xs border border-emerald-200 dark:border-emerald-800">💬</span>
        </div>
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Scam Category Breakdown */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
            {t('dashboard.categoryDist')}
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryChartData} layout="vertical" margin={{ left: 10, right: 20 }}>
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px', color: '#fff' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 7-Day Timeline Trend */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
            7-Day Threat Activity Trend
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.timeline_trend || []}>
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px', color: '#fff' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Area type="monotone" dataKey="high_risk" stackId="1" stroke="#ef4444" fill="#ef4444" fillOpacity={0.6} name="High Risk" />
                <Area type="monotone" dataKey="suspicious" stackId="1" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.6} name="Suspicious" />
                <Area type="monotone" dataKey="safe" stackId="1" stroke="#10b981" fill="#10b981" fillOpacity={0.6} name="Safe" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Language Breakdown */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
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
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px', color: '#fff' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Score Bucket Distribution */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
            {t('dashboard.riskScoreDist')}
          </h3>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={scoreBucketData}>
                <XAxis dataKey="bucket" tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px', color: '#fff' }}
                />
                <Bar dataKey="count" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Fraud Patterns / Signals Table */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
          Top Triggered Fraud Patterns & Signals
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-100 dark:border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                <th className="py-2.5 px-3">Signal Name</th>
                <th className="py-2.5 px-3">Severity</th>
                <th className="py-2.5 px-3 text-right">Detection Count</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-medium text-slate-700 dark:text-slate-300">
              {stats?.top_signals?.map((s, idx) => (
                <tr key={idx} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                  <td className="py-3 px-3 font-semibold text-slate-900 dark:text-white">{s.signal}</td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase ${
                      s.severity === 'CRITICAL' ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300' : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
                    }`}>
                      {s.severity}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold text-slate-900 dark:text-white">
                    {s.count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recent Analysis History Table */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
            {t('dashboard.recentHistory')}
          </h3>
          <span className="text-xs font-semibold text-slate-400">
            Masked PII for Consumer Privacy
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-100 dark:border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
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
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-medium text-slate-700 dark:text-slate-300">
              {stats?.recent_analyses?.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                      item.verdict === 'HIGH RISK' ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300' : (item.verdict === 'SUSPICIOUS' ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' : 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300')
                    }`}>
                      {item.verdict}
                    </span>
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-slate-900 dark:text-white">{item.risk_score}</td>
                  <td className="py-3 px-3 text-slate-600 dark:text-slate-400">{item.detected_category.replace(/_/g, ' ')}</td>
                  <td className="py-3 px-3 font-mono text-[11px] max-w-xs truncate">{item.raw_input_masked}</td>
                  <td className="py-3 px-3 uppercase text-[10px] text-slate-500 font-bold">{item.input_type}</td>
                  <td className="py-3 px-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                      item.channel === 'telegram'
                        ? 'bg-sky-100 dark:bg-sky-950 text-sky-700 dark:text-sky-300'
                        : (item.channel === 'whatsapp'
                            ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300'
                            : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300')
                    }`}>
                      {item.channel || 'web'}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${item.is_simulated ? 'bg-slate-100 dark:bg-slate-800 text-slate-500' : 'bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300'}`}>
                      {item.is_simulated ? 'SIMULATED' : 'LIVE'}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right text-slate-400 font-mono text-[11px]">{item.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
