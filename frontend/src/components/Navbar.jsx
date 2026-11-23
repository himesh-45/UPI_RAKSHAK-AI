import React from 'react';
import { Shield, Sparkles, BarChart3, HelpCircle, Sun, Moon, Lock, LogOut, BookOpen, Scale, QrCode } from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import AdminAlarmBell from './AdminAlarmBell';

export default function Navbar({ activeTab, setActiveTab, darkMode, setDarkMode, token, onOpenLogin, onLogout }) {
  const { language, setLanguage, t } = useTranslation();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-[#1E3A5F] bg-[#050A18]/90 dark:bg-[#050A18]/90 backdrop-blur-xl transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo - Original High-Tech Shield Emblem with Teal Glow & Gold Rim */}
        <div
          onClick={() => setActiveTab('analyzer')}
          className="flex items-center gap-3 cursor-pointer group"
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && setActiveTab('analyzer')}
          aria-label="UPI Rakshak AI Home"
        >
          <div className="relative p-2 rounded-2xl bg-gradient-to-b from-[#0F1D3A] to-[#070E22] border-2 border-[#D9A441] shadow-[0_0_20px_rgba(53,208,200,0.35)] group-hover:shadow-[0_0_28px_rgba(53,208,200,0.6)] group-hover:scale-105 transition transform">
            <svg className="w-5 h-5 text-[#35D0C8] drop-shadow-[0_0_8px_rgba(53,208,200,0.8)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="rgba(31,181,173,0.18)" />
              <path d="m9 12 2 2 4-4" stroke="#D9A441" strokeWidth="2.5" />
            </svg>
            <div className="absolute inset-0 rounded-2xl border border-[#35D0C8]/40 animate-pulse pointer-events-none" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-base tracking-tight text-[#F5F1E6] group-hover:text-[#F5C96A] transition">
                UPI Rakshak
              </span>
              <span className="text-[10px] uppercase font-black tracking-wider px-1.5 py-0.5 rounded-full bg-[#1FB5AD]/20 text-[#35D0C8] border border-[#35D0C8]/40 shadow-[0_0_10px_rgba(53,208,200,0.25)]">
                AI
              </span>
            </div>
            <p className="text-[10px] text-[#A9B4CC] font-semibold tracking-wide hidden sm:block">
              Secure Today. Safer Tomorrow.
            </p>
          </div>
        </div>

        {/* Navigation Tabs - Transparent-to-Solid Navy Bar with Gold Underline on Active Item */}
        <nav className="hidden md:flex items-center gap-1 bg-[#070E22]/80 p-1 rounded-2xl border border-[#1E3A5F]">
          <button
            onClick={() => setActiveTab('analyzer')}
            className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 relative ${
              activeTab === 'analyzer'
                ? 'text-[#F5C96A] border-b-2 border-[#D9A441] pb-1'
                : 'text-[#A9B4CC] hover:text-[#F5F1E6] hover:bg-[#0F1D3A]/60 rounded-xl'
            }`}
          >
            <Shield className="w-3.5 h-3.5 text-[#35D0C8]" />
            <span>{t('nav.analyzer')}</span>
          </button>

          <button
            onClick={() => setActiveTab('assistant')}
            className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 relative ${
              activeTab === 'assistant'
                ? 'text-[#F5C96A] border-b-2 border-[#D9A441] pb-1'
                : 'text-[#A9B4CC] hover:text-[#F5F1E6] hover:bg-[#0F1D3A]/60 rounded-xl'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-[#35D0C8]" />
            <span>{t('nav.assistant')}</span>
          </button>

          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 relative ${
              activeTab === 'dashboard'
                ? 'text-[#F5C96A] border-b-2 border-[#D9A441] pb-1'
                : 'text-[#A9B4CC] hover:text-[#F5F1E6] hover:bg-[#0F1D3A]/60 rounded-xl'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5 text-[#35D0C8]" />
            <span>{t('nav.dashboard')}</span>
          </button>

          <button
            onClick={() => setActiveTab('study')}
            className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 relative ${
              activeTab === 'study'
                ? 'text-[#F5C96A] border-b-2 border-[#D9A441] pb-1'
                : 'text-[#A9B4CC] hover:text-[#F5F1E6] hover:bg-[#0F1D3A]/60 rounded-xl'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-[#35D0C8]" />
            <span>Study</span>
          </button>

          <button
            onClick={() => setActiveTab('arrest')}
            className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 relative ${
              activeTab === 'arrest'
                ? 'text-[#F5C96A] border-b-2 border-[#D9A441] pb-1'
                : 'text-[#A9B4CC] hover:text-[#F5F1E6] hover:bg-[#0F1D3A]/60 rounded-xl'
            }`}
          >
            <Scale className="w-3.5 h-3.5 text-[#FB923C]" />
            <span>Digital Arrest</span>
          </button>

          <button
            onClick={() => setActiveTab('try')}
            className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 relative ${
              activeTab === 'try'
                ? 'text-[#F5C96A] border-b-2 border-[#D9A441] pb-1'
                : 'text-[#A9B4CC] hover:text-[#F5F1E6] hover:bg-[#0F1D3A]/60 rounded-xl'
            }`}
          >
            <QrCode className="w-3.5 h-3.5 text-[#F5C96A]" />
            <span>Judge / Try</span>
          </button>

          <button
            onClick={() => setActiveTab('about')}
            className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 relative ${
              activeTab === 'about'
                ? 'text-[#F5C96A] border-b-2 border-[#D9A441] pb-1'
                : 'text-[#A9B4CC] hover:text-[#F5F1E6] hover:bg-[#0F1D3A]/60 rounded-xl'
            }`}
          >
            <HelpCircle className="w-3.5 h-3.5 text-[#35D0C8]" />
            <span>{t('nav.about')}</span>
          </button>
        </nav>

        {/* Right Controls: Emergency 1930, Notifications, Language, Theme, Admin */}
        <div className="flex items-center gap-2.5">
          {/* Emergency 1930 Direct Call Button with High Visibility Gold Styling */}
          <a
            href="tel:1930"
            className="px-3 py-1.5 rounded-full bg-gradient-to-r from-[#D9A441] to-[#F5C96A] hover:from-[#F5C96A] hover:to-[#F3D58A] text-[#050A18] font-black text-xs uppercase tracking-wider flex items-center gap-1.5 shadow-[0_0_15px_rgba(217,164,65,0.4)] transition hover:scale-105 active:scale-95"
            title="Call National Cybercrime Helpline 1930"
            aria-label="Call National Cybercrime Helpline 1930"
          >
            <span className="text-sm">🚨</span>
            <span>1930</span>
          </a>

          {/* Admin Incident & Feedback Alarm Bell */}
          <AdminAlarmBell onNavigateToDashboard={() => setActiveTab('dashboard')} />

          {/* Language Switcher */}
          <div className="flex items-center bg-[#070E22] p-0.5 rounded-xl border border-[#1E3A5F] text-[11px] font-bold">
            <button
              onClick={() => setLanguage('en')}
              className={`px-2 py-1 rounded-lg transition ${
                language === 'en'
                  ? 'bg-[#35D0C8]/20 text-[#35D0C8] border border-[#35D0C8]/40 shadow-xs'
                  : 'text-[#A9B4CC] hover:text-[#F5F1E6]'
              }`}
              aria-label="Switch to English"
            >
              EN
            </button>
            <button
              onClick={() => setLanguage('hi')}
              className={`px-2 py-1 rounded-lg transition ${
                language === 'hi'
                  ? 'bg-[#35D0C8]/20 text-[#35D0C8] border border-[#35D0C8]/40 shadow-xs'
                  : 'text-[#A9B4CC] hover:text-[#F5F1E6]'
              }`}
              aria-label="Switch to Hindi"
            >
              हिंदी
            </button>
            <button
              onClick={() => setLanguage('te')}
              className={`px-2 py-1 rounded-lg transition ${
                language === 'te'
                  ? 'bg-[#35D0C8]/20 text-[#35D0C8] border border-[#35D0C8]/40 shadow-xs'
                  : 'text-[#A9B4CC] hover:text-[#F5F1E6]'
              }`}
              aria-label="Switch to Telugu"
            >
              తెలుగు
            </button>
          </div>

          {/* Dark / Light Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            aria-label="Toggle dark / light mode"
            className="p-2 rounded-xl bg-[#0F1D3A] text-[#35D0C8] border border-[#1E3A5F] hover:border-[#35D0C8]/50 hover:bg-[#14254B] transition"
          >
            {darkMode ? <Sun className="w-4 h-4 text-[#F5C96A]" /> : <Moon className="w-4 h-4 text-[#35D0C8]" />}
          </button>

          {/* Admin Login / Logout */}
          {token ? (
            <button
              onClick={onLogout}
              title="Admin logged in. Click to logout"
              className="px-2.5 py-1.5 rounded-xl bg-[#0F1D3A] text-[#35D0C8] border border-[#35D0C8]/40 text-xs font-bold flex items-center gap-1.5 transition shadow-[0_0_10px_rgba(53,208,200,0.2)]"
            >
              <LogOut className="w-3.5 h-3.5 text-[#35D0C8]" />
              <span className="hidden sm:inline">Admin</span>
            </button>
          ) : (
            <button
              onClick={onOpenLogin}
              className="px-2.5 py-1.5 rounded-xl bg-[#0F1D3A] hover:bg-[#14254B] text-[#A9B4CC] hover:text-[#F5F1E6] border border-[#1E3A5F] hover:border-[#35D0C8]/40 text-xs font-bold flex items-center gap-1.5 transition"
            >
              <Lock className="w-3.5 h-3.5 text-[#35D0C8]" />
              <span className="hidden sm:inline">Admin</span>
            </button>
          )}
        </div>
      </div>

      {/* Mobile nav pills */}
      <div className="flex md:hidden items-center justify-around border-t border-[#1E3A5F]/60 py-2 px-3 bg-[#050A18]/95 backdrop-blur-md">
        <button
          onClick={() => setActiveTab('analyzer')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'analyzer' ? 'text-[#F5C96A]' : 'text-[#A9B4CC]'}`}
        >
          <Shield className="w-4 h-4 text-[#35D0C8]" />
          <span>Analyzer</span>
        </button>
        <button
          onClick={() => setActiveTab('assistant')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'assistant' ? 'text-[#F5C96A]' : 'text-[#A9B4CC]'}`}
        >
          <Sparkles className="w-4 h-4 text-[#35D0C8]" />
          <span>Assistant</span>
        </button>
        <button
          onClick={() => setActiveTab('dashboard')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'dashboard' ? 'text-[#F5C96A]' : 'text-[#A9B4CC]'}`}
        >
          <BarChart3 className="w-4 h-4 text-[#35D0C8]" />
          <span>Dashboard</span>
        </button>
        <button
          onClick={() => setActiveTab('about')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'about' ? 'text-[#F5C96A]' : 'text-[#A9B4CC]'}`}
        >
          <HelpCircle className="w-4 h-4 text-[#35D0C8]" />
          <span>About</span>
        </button>
      </div>
    </header>
  );
}
