import React from 'react';
import { Shield, Sparkles, BarChart3, HelpCircle, Sun, Moon, Lock, LogOut, BookOpen, Scale } from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';

export default function Navbar({ activeTab, setActiveTab, darkMode, setDarkMode, token, onOpenLogin, onLogout }) {
  const { language, setLanguage, t } = useTranslation();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 dark:border-slate-800 bg-white/90 dark:bg-slate-950/90 backdrop-blur-md transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <div
          onClick={() => setActiveTab('analyzer')}
          className="flex items-center gap-2.5 cursor-pointer group"
        >
          <div className="p-2 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-700 to-violet-600 text-white shadow-md shadow-indigo-500/20 group-hover:scale-105 transition transform">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-base tracking-tight text-slate-900 dark:text-white">
                UPI Rakshak
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/60 text-indigo-700 dark:text-indigo-300">
                AI
              </span>
            </div>
            <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium hidden sm:block">
              Multilingual Scam Detection
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-100/80 dark:bg-slate-900/80 p-1 rounded-xl border border-slate-200 dark:border-slate-800">
          <button
            onClick={() => setActiveTab('analyzer')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'analyzer'
                ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Shield className="w-3.5 h-3.5" />
            {t('nav.analyzer')}
          </button>

          <button
            onClick={() => setActiveTab('assistant')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'assistant'
                ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            {t('nav.assistant')}
          </button>

          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'dashboard'
                ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5" />
            {t('nav.dashboard')}
          </button>

          <button
            onClick={() => setActiveTab('study')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'study'
                ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            Study
          </button>

          <button
            onClick={() => setActiveTab('arrest')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'arrest'
                ? 'bg-rose-50 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 shadow-sm border border-rose-200 dark:border-rose-900/60'
                : 'text-slate-600 dark:text-slate-400 hover:text-rose-600 dark:hover:text-rose-400'
            }`}
          >
            <Scale className="w-3.5 h-3.5 text-rose-500" />
            <span>Digital Arrest</span>
          </button>

          <button
            onClick={() => setActiveTab('about')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'about'
                ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <HelpCircle className="w-3.5 h-3.5" />
            {t('nav.about')}
          </button>
        </nav>

        {/* Right Controls: Language Selector, Theme Toggle, Admin Button */}
        <div className="flex items-center gap-2">
          {/* Emergency 1930 Direct Call Button */}
          <a
            href="tel:1930"
            className="px-2.5 py-1 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-black text-xs uppercase tracking-wider flex items-center gap-1 shadow transition animate-pulse"
            title="Call National Cybercrime Helpline 1930"
          >
            <span>1930</span>
          </a>

          {/* Language Switcher */}
          <div className="flex items-center bg-slate-100 dark:bg-slate-900 p-0.5 rounded-lg border border-slate-200 dark:border-slate-800 text-[11px] font-bold">
            <button
              onClick={() => setLanguage('en')}
              className={`px-2 py-1 rounded transition ${language === 'en' ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-xs' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'}`}
            >
              EN
            </button>
            <button
              onClick={() => setLanguage('hi')}
              className={`px-2 py-1 rounded transition ${language === 'hi' ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-xs' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'}`}
            >
              हिंदी
            </button>
            <button
              onClick={() => setLanguage('te')}
              className={`px-2 py-1 rounded transition ${language === 'te' ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-xs' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'}`}
            >
              తెలుగు
            </button>
          </div>

          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            aria-label="Toggle dark mode"
            className="p-2 rounded-xl bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition"
          >
            {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* Admin Login / Logout */}
          {token ? (
            <button
              onClick={onLogout}
              title="Admin logged in. Click to logout"
              className="px-2.5 py-1.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-800 text-xs font-bold flex items-center gap-1.5 transition"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Admin</span>
            </button>
          ) : (
            <button
              onClick={onOpenLogin}
              className="px-2.5 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-900 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-300 dark:border-slate-800 text-xs font-bold flex items-center gap-1.5 transition"
            >
              <Lock className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Admin</span>
            </button>
          )}
        </div>
      </div>

      {/* Mobile nav pills */}
      <div className="flex md:hidden items-center justify-around border-t border-slate-200 dark:border-slate-800 py-2 px-3 bg-slate-50 dark:bg-slate-900/60">
        <button
          onClick={() => setActiveTab('analyzer')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'analyzer' ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-500'}`}
        >
          <Shield className="w-4 h-4" />
          <span>Analyzer</span>
        </button>
        <button
          onClick={() => setActiveTab('assistant')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'assistant' ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-500'}`}
        >
          <Sparkles className="w-4 h-4" />
          <span>Assistant</span>
        </button>
        <button
          onClick={() => setActiveTab('dashboard')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'dashboard' ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-500'}`}
        >
          <BarChart3 className="w-4 h-4" />
          <span>Dashboard</span>
        </button>
        <button
          onClick={() => setActiveTab('arrest')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'arrest' ? 'text-rose-600 dark:text-rose-400' : 'text-slate-500'}`}
        >
          <Scale className="w-4 h-4" />
          <span>Arrest</span>
        </button>
        <button
          onClick={() => setActiveTab('about')}
          className={`text-xs font-bold flex flex-col items-center gap-1 ${activeTab === 'about' ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-500'}`}
        >
          <HelpCircle className="w-4 h-4" />
          <span>About</span>
        </button>
      </div>
    </header>
  );
}
