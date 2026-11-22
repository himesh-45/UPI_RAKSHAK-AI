import React from 'react';
import { Shield, Sparkles, BarChart3, HelpCircle, Sun, Moon, Lock, LogOut, BookOpen, Scale, QrCode } from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import AdminAlarmBell from './AdminAlarmBell';

export default function Navbar({ activeTab, setActiveTab, darkMode, setDarkMode, token, onOpenLogin, onLogout }) {
  const { language, setLanguage, t } = useTranslation();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-cyan-500/20 bg-[#080d22]/90 backdrop-blur-xl transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo - High-Tech Glowing Shield */}
        <div
          onClick={() => setActiveTab('analyzer')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="relative p-2.5 rounded-2xl bg-gradient-to-tr from-cyan-400 via-sky-500 to-blue-600 text-slate-950 shadow-[0_0_20px_rgba(6,182,212,0.45)] group-hover:shadow-[0_0_30px_rgba(6,182,212,0.7)] group-hover:scale-105 transition transform">
            <Shield className="w-5 h-5 fill-slate-950" />
            <div className="absolute inset-0 rounded-2xl border border-cyan-300/40 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-base tracking-tight text-white group-hover:text-cyan-300 transition">
                UPI Rakshak
              </span>
              <span className="text-[10px] uppercase font-black tracking-wider px-1.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-400/40 shadow-[0_0_10px_rgba(6,182,212,0.3)]">
                AI
              </span>
            </div>
            <p className="text-[10px] text-cyan-400/80 font-semibold tracking-wide hidden sm:block">
              Secure Today. Safer Tomorrow.
            </p>
          </div>
        </div>

        {/* Navigation Tabs - Glassmorphic Pill Container */}
        <nav className="hidden md:flex items-center gap-1.5 bg-[#060919]/90 p-1.5 rounded-2xl border border-cyan-500/20 shadow-inner">
          <button
            onClick={() => setActiveTab('analyzer')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition flex items-center gap-1.5 ${
              activeTab === 'analyzer'
                ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-400/50 shadow-[0_0_15px_rgba(6,182,212,0.25)]'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
            }`}
          >
            <Shield className="w-3.5 h-3.5" />
            {t('nav.analyzer')}
          </button>

          <button
            onClick={() => setActiveTab('assistant')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition flex items-center gap-1.5 ${
              activeTab === 'assistant'
                ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-400/50 shadow-[0_0_15px_rgba(6,182,212,0.25)]'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            {t('nav.assistant')}
          </button>

          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition flex items-center gap-1.5 ${
              activeTab === 'dashboard'
                ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-400/50 shadow-[0_0_15px_rgba(6,182,212,0.25)]'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5 text-blue-400" />
            {t('nav.dashboard')}
          </button>

          <button
            onClick={() => setActiveTab('study')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition flex items-center gap-1.5 ${
              activeTab === 'study'
                ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-400/50 shadow-[0_0_15px_rgba(6,182,212,0.25)]'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
            Study
          </button>

          <button
            onClick={() => setActiveTab('arrest')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition flex items-center gap-1.5 ${
              activeTab === 'arrest'
                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/50 shadow-[0_0_15px_rgba(244,63,94,0.3)]'
                : 'text-slate-400 hover:text-rose-400 hover:bg-rose-950/30'
            }`}
          >
            <Scale className="w-3.5 h-3.5 text-rose-400" />
            <span>Digital Arrest</span>
          </button>

          <button
            onClick={() => setActiveTab('try')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition flex items-center gap-1.5 ${
              activeTab === 'try'
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/50 shadow-[0_0_15px_rgba(245,158,11,0.3)]'
                : 'text-slate-400 hover:text-amber-400 hover:bg-amber-950/30'
            }`}
          >
            <QrCode className="w-3.5 h-3.5 text-amber-400" />
            <span>Judge / Try</span>
          </button>

          <button
            onClick={() => setActiveTab('about')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition flex items-center gap-1.5 ${
              activeTab === 'about'
                ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-400/50 shadow-[0_0_15px_rgba(6,182,212,0.25)]'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
            }`}
          >
            <HelpCircle className="w-3.5 h-3.5" />
            {t('nav.about')}
          </button>
        </nav>

        {/* Right Controls: Emergency 1930, Notifications, Language, Theme, Admin */}
        <div className="flex items-center gap-2.5">
          {/* Emergency 1930 Direct Call Button */}
          <a
            href="tel:1930"
            className="px-3 py-1.5 rounded-full bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white font-black text-xs uppercase tracking-wider flex items-center gap-1 shadow-[0_0_15px_rgba(244,63,94,0.45)] transition hover:scale-105"
            title="Call National Cybercrime Helpline 1930"
          >
            <span>🚨 1930</span>
          </a>

          {/* Cyber Admin Incident & Feedback Alarm Bell */}
          <AdminAlarmBell onNavigateToDashboard={() => setActiveTab('dashboard')} />

          {/* Language Switcher */}
          <div className="flex items-center bg-[#060919] p-0.5 rounded-xl border border-cyan-500/20 text-[11px] font-bold">
            <button
              onClick={() => setLanguage('en')}
              className={`px-2 py-1 rounded-lg transition ${language === 'en' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/40 shadow-xs' : 'text-slate-400 hover:text-white'}`}
            >
              EN
            </button>
            <button
              onClick={() => setLanguage('hi')}
              className={`px-2 py-1 rounded-lg transition ${language === 'hi' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/40 shadow-xs' : 'text-slate-400 hover:text-white'}`}
            >
              हिंदी
            </button>
            <button
              onClick={() => setLanguage('te')}
              className={`px-2 py-1 rounded-lg transition ${language === 'te' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/40 shadow-xs' : 'text-slate-400 hover:text-white'}`}
            >
              తెలుగు
            </button>
          </div>

          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            aria-label="Toggle dark mode"
            className="p-2 rounded-xl bg-[#0c122b] text-cyan-300 border border-cyan-500/20 hover:border-cyan-400/50 hover:bg-slate-800 transition"
          >
            {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-cyan-400" />}
          </button>

          {/* Admin Login / Logout */}
          {token ? (
            <button
              onClick={onLogout}
              title="Admin logged in. Click to logout"
              className="px-2.5 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-bold flex items-center gap-1.5 transition shadow-[0_0_10px_rgba(16,185,129,0.3)]"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Admin</span>
            </button>
          ) : (
            <button
              onClick={onOpenLogin}
              className="px-2.5 py-1.5 rounded-xl bg-[#0c122b] hover:bg-slate-800 text-slate-300 border border-cyan-500/20 hover:border-cyan-400/40 text-xs font-bold flex items-center gap-1.5 transition"
            >
              <Lock className="w-3.5 h-3.5 text-cyan-400" />
              <span className="hidden sm:inline">Admin</span>
            </button>
          )}
        </div>
      </div>

      {/* Mobile nav pills */}
      <div className="flex md:hidden items-center justify-around border-t border-cyan-500/10 py-2 px-3 bg-[#060919]/95 backdrop-blur-md">
        <button
          onClick={() => setActiveTab('analyzer')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'analyzer' ? 'text-cyan-400' : 'text-slate-400'}`}
        >
          <Shield className="w-4 h-4" />
          <span>Analyzer</span>
        </button>
        <button
          onClick={() => setActiveTab('assistant')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'assistant' ? 'text-cyan-400' : 'text-slate-400'}`}
        >
          <Sparkles className="w-4 h-4" />
          <span>Assistant</span>
        </button>
        <button
          onClick={() => setActiveTab('dashboard')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'dashboard' ? 'text-cyan-400' : 'text-slate-400'}`}
        >
          <BarChart3 className="w-4 h-4" />
          <span>Dashboard</span>
        </button>
        <button
          onClick={() => setActiveTab('about')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'about' ? 'text-cyan-400' : 'text-slate-400'}`}
        >
          <HelpCircle className="w-4 h-4" />
          <span>About</span>
        </button>
      </div>
    </header>
  );
}
