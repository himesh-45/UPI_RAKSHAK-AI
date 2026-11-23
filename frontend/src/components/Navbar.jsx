import React, { useState, useRef, useEffect } from 'react';
import { Shield, Sparkles, BarChart3, HelpCircle, Lock, LogOut, BookOpen, Scale, QrCode, MoreHorizontal, ChevronDown, Zap } from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import AdminAlarmBell from './AdminAlarmBell';

export default function Navbar({
  activeTab,
  setActiveTab,
  token,
  onOpenLogin,
  onLogout,
  onOpenLlmModal
}) {
  const { language, setLanguage, t } = useTranslation();
  const [moreOpen, setMoreOpen] = useState(false);
  const moreRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (moreRef.current && !moreRef.current.contains(event.target)) {
        setMoreOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const isMoreActive = ['study', 'try', 'about'].includes(activeTab);

  const handleSelectTab = (tab) => {
    setActiveTab(tab);
    setMoreOpen(false);
  };

  return (
    <>
      <header className="sticky top-0 z-40 w-full border-b border-border bg-navy-deep/90 backdrop-blur-xl transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          
          {/* Brand Logo - Single row, no wrapped tagline */}
          <div
            onClick={() => handleSelectTab('analyzer')}
            className="flex items-center gap-3 cursor-pointer group"
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === 'Enter' && handleSelectTab('analyzer')}
            aria-label="UPI Rakshak AI Home"
          >
            <div className="relative p-2 rounded-2xl bg-gradient-to-b from-navy-surface to-navy border-2 border-gold-500 shadow-[0_0_20px_rgba(var(--teal-400-rgb),0.35)] group-hover:scale-105 transition transform">
              <svg className="w-5 h-5 text-teal drop-shadow-[0_0_8px_rgba(var(--teal-400-rgb),0.7)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="rgba(var(--teal-500-rgb),0.18)" />
                <path d="m9 12 2 2 4-4" stroke="currentColor" className="text-gold-500" strokeWidth="2.5" />
              </svg>
            </div>
            <div className="flex items-center gap-1.5 whitespace-nowrap">
              <span className="font-extrabold text-base tracking-tight text-ink group-hover:text-gold-400 transition">
                UPI Rakshak
              </span>
              <span className="text-[10px] uppercase font-black tracking-wider px-1.5 py-0.5 rounded-full bg-teal/20 text-teal border border-teal/40">
                AI
              </span>
            </div>
          </div>

          {/* Navigation Tabs - Primary 4 items only + More Dropdown */}
          <nav className="hidden md:flex items-center gap-1 bg-navy/80 p-1 rounded-2xl border border-border">
            <button
              onClick={() => handleSelectTab('analyzer')}
              className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 rounded-xl ${
                activeTab === 'analyzer'
                  ? 'text-gold-400 bg-navy-surface border-b-2 border-gold-500 shadow-xs'
                  : 'text-ink-muted hover:text-ink hover:bg-navy-surface/60'
              }`}
            >
              <Shield className="w-3.5 h-3.5 text-teal" />
              <span>{t('nav.analyzer')}</span>
            </button>

            <button
              onClick={() => handleSelectTab('assistant')}
              className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 rounded-xl ${
                activeTab === 'assistant'
                  ? 'text-gold-400 bg-navy-surface border-b-2 border-gold-500 shadow-xs'
                  : 'text-ink-muted hover:text-ink hover:bg-navy-surface/60'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-teal" />
              <span>{t('nav.assistant')}</span>
            </button>

            <button
              onClick={() => handleSelectTab('arrest')}
              className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 rounded-xl ${
                activeTab === 'arrest'
                  ? 'text-gold-400 bg-navy-surface border-b-2 border-gold-500 shadow-xs'
                  : 'text-ink-muted hover:text-ink hover:bg-navy-surface/60'
              }`}
            >
              <Scale className="w-3.5 h-3.5 text-amber-500" />
              <span>Digital Arrest</span>
            </button>

            <button
              onClick={() => handleSelectTab('dashboard')}
              className={`px-3.5 py-1.5 text-xs font-bold transition flex items-center gap-1.5 rounded-xl ${
                activeTab === 'dashboard'
                  ? 'text-gold-400 bg-navy-surface border-b-2 border-gold-500 shadow-xs'
                  : 'text-ink-muted hover:text-ink hover:bg-navy-surface/60'
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5 text-teal" />
              <span>{t('nav.dashboard')}</span>
            </button>

            {/* "More" Dropdown Menu */}
            <div className="relative" ref={moreRef}>
              <button
                onClick={() => setMoreOpen(!moreOpen)}
                aria-expanded={moreOpen}
                aria-haspopup="true"
                className={`px-3 py-1.5 text-xs font-bold transition flex items-center gap-1.5 rounded-xl ${
                  isMoreActive || moreOpen
                    ? 'text-gold-400 bg-navy-surface border-b-2 border-gold-500'
                    : 'text-ink-muted hover:text-ink hover:bg-navy-surface/60'
                }`}
              >
                <MoreHorizontal className="w-3.5 h-3.5 text-teal" />
                <span>More</span>
                <ChevronDown className={`w-3 h-3 transition-transform ${moreOpen ? 'rotate-180' : ''}`} />
              </button>

              {moreOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-2xl bg-navy-surface border border-border shadow-2xl py-2 z-50 text-left animate-fade-in backdrop-blur-xl">
                  <button
                    onClick={() => handleSelectTab('study')}
                    className={`w-full px-4 py-2 text-xs font-semibold flex items-center gap-2.5 transition ${
                      activeTab === 'study' ? 'text-gold-400 bg-navy-raised' : 'text-ink-muted hover:text-ink hover:bg-navy-raised'
                    }`}
                  >
                    <BookOpen className="w-4 h-4 text-teal" />
                    <span>Study / Benchmark</span>
                  </button>

                  <button
                    onClick={() => handleSelectTab('try')}
                    className={`w-full px-4 py-2 text-xs font-semibold flex items-center gap-2.5 transition ${
                      activeTab === 'try' ? 'text-gold-400 bg-navy-raised' : 'text-ink-muted hover:text-ink hover:bg-navy-raised'
                    }`}
                  >
                    <QrCode className="w-4 h-4 text-gold-400" />
                    <span>Judge / Try Mode</span>
                  </button>

                  <button
                    onClick={() => handleSelectTab('about')}
                    className={`w-full px-4 py-2 text-xs font-semibold flex items-center gap-2.5 transition ${
                      activeTab === 'about' ? 'text-gold-400 bg-navy-raised' : 'text-ink-muted hover:text-ink hover:bg-navy-raised'
                    }`}
                  >
                    <HelpCircle className="w-4 h-4 text-teal" />
                    <span>{t('nav.about')}</span>
                  </button>

                  {onOpenLlmModal && (
                    <button
                      onClick={() => {
                        setMoreOpen(false);
                        onOpenLlmModal();
                      }}
                      className="w-full px-4 py-2 text-xs font-semibold text-ink-muted hover:text-ink hover:bg-navy-raised flex items-center gap-2.5 transition"
                    >
                      <Zap className="w-4 h-4 text-gold-400" />
                      <span>How we compare to a chatbot</span>
                    </button>
                  )}

                  <div className="my-1 border-t border-border" />

                  {token ? (
                    <button
                      onClick={() => {
                        setMoreOpen(false);
                        onLogout();
                      }}
                      className="w-full px-4 py-2 text-xs font-semibold text-verdict-danger hover:bg-navy-raised flex items-center gap-2.5 transition"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Admin Logout</span>
                    </button>
                  ) : (
                    <button
                      onClick={() => {
                        setMoreOpen(false);
                        onOpenLogin();
                      }}
                      className="w-full px-4 py-2 text-xs font-semibold text-teal hover:bg-navy-raised flex items-center gap-2.5 transition"
                    >
                      <Lock className="w-4 h-4" />
                      <span>Admin Login</span>
                    </button>
                  )}
                </div>
              )}
            </div>
          </nav>

          {/* Right Controls: 1930 Emergency, Alarm Bell, Language, Theme */}
          <div className="flex items-center gap-2 sm:gap-2.5">
            {/* Emergency 1930 Direct Call Button */}
            <a
              href="tel:1930"
              className="px-3 py-1.5 rounded-full bg-gradient-to-r from-gold-500 to-gold-400 hover:from-gold-400 hover:to-gold-300 text-navy-deep font-black text-xs uppercase tracking-wider flex items-center gap-1.5 shadow-[0_0_15px_rgba(var(--gold-500-rgb),0.35)] transition hover:scale-105 active:scale-95"
              title="Call National Cybercrime Helpline 1930"
              aria-label="Call National Cybercrime Helpline 1930"
            >
              <span className="text-sm">🚨</span>
              <span>1930</span>
            </a>

            {/* Admin Incident & Feedback Alarm Bell (Real unread counts only) */}
            <AdminAlarmBell onNavigateToDashboard={() => handleSelectTab('dashboard')} />

            {/* Language Switcher */}
            <div className="flex items-center bg-navy p-0.5 rounded-xl border border-border text-[11px] font-bold">
              <button
                onClick={() => setLanguage('en')}
                className={`px-2 py-1 rounded-lg transition ${
                  language === 'en'
                    ? 'bg-teal/20 text-teal border border-teal/40 shadow-xs'
                    : 'text-ink-muted hover:text-ink'
                }`}
                aria-label="Switch to English"
              >
                EN
              </button>
              <button
                onClick={() => setLanguage('hi')}
                className={`px-2 py-1 rounded-lg transition ${
                  language === 'hi'
                    ? 'bg-teal/20 text-teal border border-teal/40 shadow-xs'
                    : 'text-ink-muted hover:text-ink'
                }`}
                aria-label="Switch to Hindi"
              >
                हिंदी
              </button>
              <button
                onClick={() => setLanguage('te')}
                className={`px-2 py-1 rounded-lg transition ${
                  language === 'te'
                    ? 'bg-teal/20 text-teal border border-teal/40 shadow-xs'
                    : 'text-ink-muted hover:text-ink'
                }`}
                aria-label="Switch to Telugu"
              >
                తెలుగు
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Bottom Tab Bar with minimum 44x44px touch targets */}
      <nav aria-label="Mobile Navigation" className="fixed bottom-0 left-0 right-0 z-40 bg-navy-surface/95 backdrop-blur-xl border-t border-border flex md:hidden items-center justify-around py-1 px-1 shadow-2xl">
        <button
          onClick={() => handleSelectTab('analyzer')}
          className={`min-h-[44px] min-w-[44px] flex-1 flex flex-col items-center justify-center gap-0.5 text-[10px] font-bold transition rounded-xl ${
            activeTab === 'analyzer' ? 'text-gold-400' : 'text-ink-muted hover:text-ink'
          }`}
        >
          <Shield className="w-4 h-4 text-teal" />
          <span>Check</span>
        </button>

        <button
          onClick={() => handleSelectTab('assistant')}
          className={`min-h-[44px] min-w-[44px] flex-1 flex flex-col items-center justify-center gap-0.5 text-[10px] font-bold transition rounded-xl ${
            activeTab === 'assistant' ? 'text-gold-400' : 'text-ink-muted hover:text-ink'
          }`}
        >
          <Sparkles className="w-4 h-4 text-teal" />
          <span>Assistant</span>
        </button>

        <button
          onClick={() => handleSelectTab('arrest')}
          className={`min-h-[44px] min-w-[44px] flex-1 flex flex-col items-center justify-center gap-0.5 text-[10px] font-bold transition rounded-xl ${
            activeTab === 'arrest' ? 'text-gold-400' : 'text-ink-muted hover:text-ink'
          }`}
        >
          <Scale className="w-4 h-4 text-amber-500" />
          <span>Arrest</span>
        </button>

        <button
          onClick={() => handleSelectTab('dashboard')}
          className={`min-h-[44px] min-w-[44px] flex-1 flex flex-col items-center justify-center gap-0.5 text-[10px] font-bold transition rounded-xl ${
            activeTab === 'dashboard' ? 'text-gold-400' : 'text-ink-muted hover:text-ink'
          }`}
        >
          <BarChart3 className="w-4 h-4 text-teal" />
          <span>Dashboard</span>
        </button>

        <button
          onClick={() => setMoreOpen(!moreOpen)}
          className={`min-h-[44px] min-w-[44px] flex-1 flex flex-col items-center justify-center gap-0.5 text-[10px] font-bold transition rounded-xl ${
            isMoreActive || moreOpen ? 'text-gold-400' : 'text-ink-muted hover:text-ink'
          }`}
        >
          <MoreHorizontal className="w-4 h-4 text-teal" />
          <span>More</span>
        </button>
      </nav>

      {/* Mobile "More" Drawer Backdrop & Menu */}
      {moreOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-navy-deep/80 backdrop-blur-sm flex flex-col justify-end" onClick={() => setMoreOpen(false)}>
          <div className="bg-navy-surface border-t border-border rounded-t-3xl p-5 space-y-2 mb-14 animate-fade-in shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="w-12 h-1 bg-border rounded-full mx-auto mb-3" />
            <div className="text-xs font-bold uppercase tracking-wider text-ink-muted px-2 pb-1">Navigation & Tools</div>

            <button
              onClick={() => handleSelectTab('study')}
              className={`w-full min-h-[44px] px-3 py-2 rounded-xl text-xs font-semibold flex items-center gap-3 transition ${
                activeTab === 'study' ? 'text-gold-400 bg-navy-raised' : 'text-ink-muted hover:text-ink hover:bg-navy-raised'
              }`}
            >
              <BookOpen className="w-4 h-4 text-teal" />
              <span>Study / Benchmark</span>
            </button>

            <button
              onClick={() => handleSelectTab('try')}
              className={`w-full min-h-[44px] px-3 py-2 rounded-xl text-xs font-semibold flex items-center gap-3 transition ${
                activeTab === 'try' ? 'text-gold-400 bg-navy-raised' : 'text-ink-muted hover:text-ink hover:bg-navy-raised'
              }`}
            >
              <QrCode className="w-4 h-4 text-gold-400" />
              <span>Judge / Try Mode</span>
            </button>

            <button
              onClick={() => handleSelectTab('about')}
              className={`w-full min-h-[44px] px-3 py-2 rounded-xl text-xs font-semibold flex items-center gap-3 transition ${
                activeTab === 'about' ? 'text-gold-400 bg-navy-raised' : 'text-ink-muted hover:text-ink hover:bg-navy-raised'
              }`}
            >
              <HelpCircle className="w-4 h-4 text-teal" />
              <span>{t('nav.about')}</span>
            </button>

            {onOpenLlmModal && (
              <button
                onClick={() => {
                  setMoreOpen(false);
                  onOpenLlmModal();
                }}
                className="w-full min-h-[44px] px-3 py-2 rounded-xl text-xs font-semibold text-ink-muted hover:text-ink hover:bg-navy-raised flex items-center gap-3 transition"
              >
                <Zap className="w-4 h-4 text-gold-400" />
                <span>How we compare to a chatbot</span>
              </button>
            )}

            <div className="my-2 border-t border-border" />

            {token ? (
              <button
                onClick={() => {
                  setMoreOpen(false);
                  onLogout();
                }}
                className="w-full min-h-[44px] px-3 py-2 rounded-xl text-xs font-semibold text-verdict-danger hover:bg-navy-raised flex items-center gap-3 transition"
              >
                <LogOut className="w-4 h-4" />
                <span>Admin Logout</span>
              </button>
            ) : (
              <button
                onClick={() => {
                  setMoreOpen(false);
                  onOpenLogin();
                }}
                className="w-full min-h-[44px] px-3 py-2 rounded-xl text-xs font-semibold text-teal hover:bg-navy-raised flex items-center gap-3 transition"
              >
                <Lock className="w-4 h-4" />
                <span>Admin Login</span>
              </button>
            )}
          </div>
        </div>
      )}
    </>
  );
}
