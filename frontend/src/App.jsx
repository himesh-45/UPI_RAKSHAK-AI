import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import AnalyzerPage from './pages/AnalyzerPage';
import AssistantPage from './pages/AssistantPage';
import DashboardPage from './pages/DashboardPage';
import AboutPage from './pages/AboutPage';
import StudyPage from './pages/StudyPage';
import DigitalArrestPage from './pages/DigitalArrestPage';
import JudgeTryPage from './pages/JudgeTryPage';
import LoginModal from './components/LoginModal';
import { TranslationProvider } from './i18n/useTranslation';

function AppContent() {
  const [activeTab, setActiveTab] = useState(() => {
    if (typeof window !== 'undefined') {
      if (window.location.pathname === '/study') return 'study';
      if (window.location.pathname === '/arrest') return 'arrest';
      if (window.location.pathname === '/try') return 'try';
    }
    return 'analyzer';
  });
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('theme');
    if (saved) return saved === 'dark';
    return true; // Default to Cyber Dark Theme
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
    <div className="min-h-screen flex flex-col bg-navy-deep text-ink transition-colors duration-200">
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
        {activeTab === 'study' && <StudyPage />}
        {activeTab === 'arrest' && <DigitalArrestPage />}
        {activeTab === 'try' && <JudgeTryPage />}
        {activeTab === 'about' && <AboutPage />}
      </main>

      <footer className="border-t border-cyan-500/10 py-6 px-4 bg-[#080d22]/90 backdrop-blur-md text-center text-xs text-slate-400">
        <p className="max-w-3xl mx-auto leading-relaxed">
          <strong className="text-cyan-400">UPI Rakshak AI</strong> is an offline-first, evidence-based digital payment scam detection system.
          Prototype for consumer protection. Always confirm suspicious transactions with your bank.
          National Cyber Crime Reporting Helpline: <strong className="text-white">1930</strong> • <strong className="text-cyan-400">cybercrime.gov.in</strong>
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
