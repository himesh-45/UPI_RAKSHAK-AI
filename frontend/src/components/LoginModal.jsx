import React, { useState } from 'react';
import { X, Lock, CheckCircle, KeyRound } from 'lucide-react';
import { loginAdmin } from '../api/client';
import { useTranslation } from '../i18n/useTranslation';

export default function LoginModal({ isOpen, onClose, onLoginSuccess }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await loginAdmin(email, password);
      onLoginSuccess(data.access_token);
      onClose();
    } catch (err) {
      setError(err.message || 'Login failed. Please check credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-deep/80 backdrop-blur-md animate-fade-in">
      <div className="w-full max-w-sm bg-[#0F1D3A]/95 rounded-3xl border border-[#1E3A5F] border-t-2 border-t-gold-400 shadow-2xl p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-ink-muted hover:text-ink transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-4">
          <div className="p-2.5 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-300">
            <Lock className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-extrabold text-ink text-base">
              {t('auth.adminLogin')}
            </h3>
            <p className="text-xs text-ink-muted">Secure JWT Authentication</p>
          </div>
        </div>

        {error && (
          <div className="p-2.5 mb-3 text-xs rounded-xl bg-verdict-danger/10 text-verdict-danger border border-verdict-danger/30">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3.5">
          <div>
            <label className="block text-xs font-semibold text-ink-muted mb-1">
              {t('auth.email')}
            </label>
            <input
              type="email"
              required
              placeholder="admin@upirakshak.ai"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 text-xs rounded-xl bg-[#070E22] border border-[#1E3A5F] text-ink focus:border-teal-400 focus:ring-1 focus:ring-teal-400 focus:outline-hidden"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-ink-muted mb-1">
              {t('auth.password')}
            </label>
            <input
              type="password"
              required
              placeholder="Enter admin password from .env or console"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 text-xs rounded-xl bg-[#070E22] border border-[#1E3A5F] text-ink focus:border-teal-400 focus:ring-1 focus:ring-teal-400 focus:outline-hidden"
            />
          </div>

          <div className="p-2.5 rounded-xl bg-[#0B1530] border border-[#1E3A5F] text-[11px] text-ink-muted">
            <p className="font-medium text-ink-muted">
              Admin password is in backend/data/.admin_secret (generated on first run)
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-xl btn-gold-primary font-bold text-xs uppercase tracking-wider transition disabled:opacity-50"
          >
            {loading ? 'Authenticating...' : t('auth.loginBtn')}
          </button>
        </form>
      </div>
    </div>
  );
}
