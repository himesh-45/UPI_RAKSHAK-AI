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
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 animate-fade-in text-[#F5F1E6]">
      
      {/* Prominent Simulated Demo Notice Banner */}
      <div className="p-4 rounded-2xl bg-[#0F1D3A]/90 border border-[#D9A441]/30 text-[#F5C96A] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs shadow-md">
        <div className="flex items-center gap-2.5">
          <Database className="w-5 h-5 text-[#D9A441] shrink-0" />
          <div>
            <span className="font-extrabold tracking-wide uppercase">Notice:</span>{' '}
            <span className="text-[#F5F1E6]">{t('dashboard.simulatedNotice')}</span>
          </div>
        </div>
        <div className="flex items-center gap-2 font-mono text-[11px] font-bold shrink-0">
          <span className="px-2 py-0.5 rounded bg-[#14254B] text-[#35D0C8] border border-[#35D0C8]/30">
            Live: {stats?.seeded_vs_live?.live || 0}
          </span>
          <span className="px-2 py-0.5 rounded bg-[#14254B] text-[#F5C96A] border border-[#D9A441]/30">
            Simulated: {stats?.seeded_vs_live?.simulated || 0}
          </span>
        </div>
      </div>

      {/* Header and Scope Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F1E6] font-display">
            {t('dashboard.title')}
          </h1>
          <p className="text-xs text-[#A9B4CC] mt-1">
            Aggregated threat intelligence, signal analytics, and audit logging.
          </p>
        </div>

        {/* Filter scope buttons */}
        <div className="flex items-center gap-2">
          <div className="flex items-center bg-[#0B1530] p-1 rounded-xl border border-[#1E3A5F] text-xs font-bold">
            <button
              onClick={() => setScope('all')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'all'
                  ? 'bg-gradient-to-r from-[#D9A441] to-[#F5C96A] text-[#050A18] shadow-xs'
                  : 'text-[#A9B4CC] hover:text-[#F5F1E6]'
              }`}
            >
              {t('dashboard.filterAll')}
            </button>
            <button
              onClick={() => setScope('live')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'live'
                  ? 'bg-gradient-to-r from-[#D9A441] to-[#F5C96A] text-[#050A18] shadow-xs'
                  : 'text-[#A9B4CC] hover:text-[#F5F1E6]'
              }`}
            >
              {t('dashboard.filterLive')}
            </button>
            <button
              onClick={() => setScope('simulated')}
              className={`px-3 py-1.5 rounded-lg transition ${
                scope === 'simulated'
                  ? 'bg-gradient-to-r from-[#D9A441] to-[#F5C96A] text-[#050A18] shadow-xs'
                  : 'text-[#A9B4CC] hover:text-[#F5F1E6]'
              }`}
            >
              {t('dashboard.filterSimulated')}
            </button>
          </div>

          <button
            onClick={() => fetchStats(scope)}
            className="p-2 rounded-xl bg-[#0B1530] text-[#A9B4CC] hover:text-[#35D0C8] hover:bg-[#14254B] border border-[#1E3A5F] transition"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Admin Governance & Dispute Moderation Panel (Visible when Admin signed in or login prompt) */}
      {token ? (
        <AdminModerationPanel token={token} />
      ) : (
        <div className="p-4 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs shadow-md">
          <div className="flex items-center gap-2.5">
            <Lock className="w-5 h-5 text-[#35D0C8] shrink-0" />
            <div>
              <span className="font-extrabold text-[#F5F1E6]">Admin Dispute Moderation & Research Export:</span>{' '}
              <span className="text-[#A9B4CC]">
                Sign in as Admin to review community VPA reports, adjudicate merchant false positive appeals, and export study telemetry.
              </span>
            </div>
          </div>
          <button
            onClick={onOpenLogin}
            className="btn-gold-primary px-3.5 py-1.5 rounded-xl text-xs uppercase tracking-wider shrink-0 transition"
          >
            Sign In as Admin
          </button>
        </div>
      )}

      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-1">
          <span className="text-xs font-semibold text-[#A9B4CC] uppercase tracking-wider">{t('dashboard.totalAnalyses')}</span>
          <div className="text-3xl font-extrabold text-[#F5C96A] font-mono">
            {stats?.total_analyses || 0}
          </div>
          <span className="text-[11px] text-[#35D0C8] font-semibold flex items-center gap-1 font-mono">
            <Activity className="w-3 h-3" /> All Input Formats
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-1">
          <span className="text-xs font-semibold text-[#A9B4CC] uppercase tracking-wider">{t('dashboard.highRiskCount')}</span>
          <div className="text-3xl font-extrabold text-[#F43F5E] font-mono">
            {stats?.high_risk_count || 0}
          </div>
          <span className="text-[11px] text-[#F43F5E] font-semibold flex items-center gap-1 font-mono">
            <ShieldAlert className="w-3 h-3" /> Score &ge; 70
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-1">
          <span className="text-xs font-semibold text-[#A9B4CC] uppercase tracking-wider">{t('dashboard.suspiciousCount')}</span>
          <div className="text-3xl font-extrabold text-[#FB923C] font-mono">
            {stats?.suspicious_count || 0}
          </div>
          <span className="text-[11px] text-[#FB923C] font-semibold flex items-center gap-1 font-mono">
            <AlertTriangle className="w-3 h-3" /> Score 35–69
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-1">
          <span className="text-xs font-semibold text-[#A9B4CC] uppercase tracking-wider">{t('dashboard.safeCount')}</span>
          <div className="text-3xl font-extrabold text-[#34D399] font-mono">
            {stats?.safe_count || 0}
          </div>
          <span className="text-[11px] text-[#34D399] font-semibold flex items-center gap-1 font-mono">
            <ShieldCheck className="w-3 h-3" /> Score &le; 34
          </span>
        </div>
      </div>

      {/* Omnichannel Distribution Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] flex items-center justify-between">
          <div>
            <div className="text-[11px] font-bold text-[#A9B4CC] uppercase tracking-wider">Web Portal Scans</div>
            <div className="text-2xl font-extrabold text-[#F5F1E6] font-mono mt-0.5">
              {stats?.channel_breakdown?.web || 0}
            </div>
            <div className="text-[10px] text-[#7C89A6]">Desktop & Mobile Web</div>
          </div>
          <span className="text-2xl p-3 bg-[#0B1530] rounded-xl border border-[#1E3A5F]">🌐</span>
        </div>

        <div className="p-4 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] flex items-center justify-between">
          <div>
            <div className="text-[11px] font-bold text-[#35D0C8] uppercase tracking-wider">Telegram Bot</div>
            <div className="text-2xl font-extrabold text-[#F5F1E6] font-mono mt-0.5">
              {stats?.channel_breakdown?.telegram || 0}
            </div>
            <div className="text-[10px] text-[#7C89A6]">Salted SHA-256 Privacy</div>
          </div>
          <span className="text-2xl p-3 bg-[#0B1530] text-[#35D0C8] rounded-xl border border-[#1E3A5F]">✈️</span>
        </div>

        <div className="p-4 rounded-2xl bg-[#0F1D3A]/90 border border-[#1E3A5F] flex items-center justify-between">
          <div>
            <div className="text-[11px] font-bold text-[#34D399] uppercase tracking-wider">WhatsApp Bot</div>
            <div className="text-2xl font-extrabold text-[#F5F1E6] font-mono mt-0.5">
              {stats?.channel_breakdown?.whatsapp || 0}
            </div>
            <div className="text-[10px] text-[#7C89A6]">Twilio Sandbox & Meta Cloud API</div>
          </div>
          <span className="text-2xl p-3 bg-[#0B1530] text-[#34D399] rounded-xl border border-[#1E3A5F]">💬</span>
        </div>
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Scam Category Breakdown */}
        <div className="p-6 rounded-3xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-[#F5F1E6] uppercase tracking-wider">
            {t('dashboard.categoryDist')}
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryChartData} layout="vertical" margin={{ left: 10, right: 20 }}>
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 11, fill: '#A9B4CC' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0B1530', borderColor: '#1E3A5F', borderRadius: '12px', fontSize: '12px', color: '#F5F1E6' }}
                />
                <Bar dataKey="count" fill="#D9A441" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 7-Day Timeline Trend */}
        <div className="p-6 rounded-3xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-[#F5F1E6] uppercase tracking-wider">
            7-Day Threat Activity Trend
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.timeline_trend || []}>
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#A9B4CC' }} />
                <YAxis tick={{ fontSize: 11, fill: '#A9B4CC' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0B1530', borderColor: '#1E3A5F', borderRadius: '12px', fontSize: '12px', color: '#F5F1E6' }}
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
        <div className="p-6 rounded-3xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-[#F5F1E6] uppercase tracking-wider">
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
                  contentStyle={{ backgroundColor: '#0B1530', borderColor: '#1E3A5F', borderRadius: '12px', fontSize: '12px', color: '#F5F1E6' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Score Bucket Distribution */}
        <div className="p-6 rounded-3xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-[#F5F1E6] uppercase tracking-wider">
            {t('dashboard.riskScoreDist')}
          </h3>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={scoreBucketData}>
                <XAxis dataKey="bucket" tick={{ fontSize: 11, fill: '#A9B4CC' }} />
                <YAxis tick={{ fontSize: 11, fill: '#A9B4CC' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0B1530', borderColor: '#1E3A5F', borderRadius: '12px', fontSize: '12px', color: '#F5F1E6' }}
                />
                <Bar dataKey="count" fill="#35D0C8" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Fraud Patterns / Signals Table */}
      <div className="p-6 rounded-3xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-[#F5F1E6] uppercase tracking-wider">
          Top Triggered Fraud Patterns & Signals
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-[#1E3A5F] text-[#A9B4CC] font-semibold uppercase text-[10px]">
                <th className="py-2.5 px-3">Signal Name</th>
                <th className="py-2.5 px-3">Severity</th>
                <th className="py-2.5 px-3 text-right">Detection Count</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E3A5F]/60 font-medium text-[#F5F1E6]">
              {stats?.top_signals?.map((s, idx) => (
                <tr key={idx} className="hover:bg-[#14254B]/30">
                  <td className="py-3 px-3 font-semibold text-[#F5F1E6]">{s.signal}</td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase ${
                      s.severity === 'CRITICAL' ? 'bg-[#F43F5E]/15 text-[#F43F5E] border border-[#F43F5E]/40' : 'bg-[#FB923C]/15 text-[#FB923C] border border-[#FB923C]/40'
                    }`}>
                      {s.severity}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold text-[#F5F1E6]">
                    {s.count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recent Analysis History Table */}
      <div className="p-6 rounded-3xl bg-[#0F1D3A]/90 border border-[#1E3A5F] shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-[#F5F1E6] uppercase tracking-wider">
            {t('dashboard.recentHistory')}
          </h3>
          <span className="text-xs font-semibold text-[#A9B4CC]">
            Masked PII for Consumer Privacy
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-[#1E3A5F] text-[#A9B4CC] font-semibold uppercase text-[10px]">
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
            <tbody className="divide-y divide-[#1E3A5F]/60 font-medium text-[#F5F1E6]">
              {stats?.recent_analyses?.map((item) => (
                <tr key={item.id} className="hover:bg-[#14254B]/30">
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                      item.verdict === 'HIGH RISK' ? 'bg-[#F43F5E]/15 text-[#F43F5E] border border-[#F43F5E]/40' : (item.verdict === 'SUSPICIOUS' ? 'bg-[#FB923C]/15 text-[#FB923C] border border-[#FB923C]/40' : 'bg-[#34D399]/15 text-[#34D399] border border-[#34D399]/40')
                    }`}>
                      {item.verdict}
                    </span>
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-[#F5F1E6]">{item.risk_score}</td>
                  <td className="py-3 px-3 text-[#A9B4CC]">{item.detected_category.replace(/_/g, ' ')}</td>
                  <td className="py-3 px-3 font-mono text-[11px] max-w-xs truncate text-[#A9B4CC]">{item.raw_input_masked}</td>
                  <td className="py-3 px-3 uppercase text-[10px] text-[#7C89A6] font-bold">{item.input_type}</td>
                  <td className="py-3 px-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                      item.channel === 'telegram'
                        ? 'bg-[#35D0C8]/15 text-[#35D0C8] border border-[#35D0C8]/30'
                        : (item.channel === 'whatsapp'
                            ? 'bg-[#34D399]/15 text-[#34D399] border border-[#34D399]/30'
                            : 'bg-[#14254B] text-[#A9B4CC] border border-[#1E3A5F]')
                    }`}>
                      {item.channel || 'web'}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${item.is_simulated ? 'bg-[#0B1530] text-[#7C89A6]' : 'bg-[#D9A441]/15 text-[#F5C96A] border border-[#D9A441]/40'}`}>
                      {item.is_simulated ? 'SIMULATED' : 'LIVE'}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right text-[#7C89A6] font-mono text-[11px]">{item.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
