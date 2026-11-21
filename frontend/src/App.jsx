import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import AnalyzerPage from './pages/AnalyzerPage';
import AssistantPage from './pages/AssistantPage';
import DashboardPage from './pages/DashboardPage';
import AboutPage from './pages/AboutPage';
import LoginModal from './components/LoginModal';
import { TranslationProvider } from './i18n/useTranslation';

function AppContent() {
  const [activeTab, setActiveTab] = useState('analyzer'); // 'analyzer', 'assistant', 'dashboard', 'about'
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark';
  });
  const [token, setToken] = useState(() => localStorage.getItem('upi_rakshak_token') || null);
  const [loginModalOpen, setLoginModalOpen] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  const handleLoginSuccess = (newToken) => {
    setToken(newToken);
    localStorage.setItem('upi_rakshak_token', newToken);
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('upi_rakshak_token');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        token={token}
        onOpenLogin={() => setLoginModalOpen(true)}
        onLogout={handleLogout}
      />

      <main className="flex-1">
        {activeTab === 'analyzer' && <AnalyzerPage />}
        {activeTab === 'assistant' && <AssistantPage />}
        {activeTab === 'dashboard' && (
          <DashboardPage token={token} onOpenLogin={() => setLoginModalOpen(true)} />
        )}
        {activeTab === 'about' && <AboutPage />}
      </main>

      <footer className="border-t border-slate-200 dark:border-slate-800 py-6 px-4 bg-white dark:bg-slate-950 text-center text-xs text-slate-500">
        <p className="max-w-3xl mx-auto leading-relaxed">
          <strong>UPI Rakshak AI</strong> is an offline-first, evidence-based digital payment scam detection system.
          Prototype for consumer protection. Always confirm suspicious transactions with your bank.
          National Cyber Crime Reporting Helpline: <strong>1930</strong> • <strong>cybercrime.gov.in</strong>
        </p>
      </footer>

      <LoginModal
        isOpen={loginModalOpen}
        onClose={() => setLoginModalOpen(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
}

export default function App() {
  return (
    <TranslationProvider>
      <AppContent />
    </TranslationProvider>
  );
}
