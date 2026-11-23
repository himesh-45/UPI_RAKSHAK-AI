import React, { useState } from 'react';
import { X, Send, ShieldAlert, CheckCircle } from 'lucide-react';
import { submitThreatReport } from '../api/client';

export default function ReportModal({ isOpen, onClose, analysisId, inputType, defaultContent, defaultCategory }) {
  const [comments, setComments] = useState('');
  const [contact, setContact] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await submitThreatReport({
        analysis_id: analysisId || null,
        input_type: inputType || 'text',
        suspicious_content: defaultContent || '',
        scam_category: defaultCategory || 'general_fraud',
        comments,
        contact
      });
      setSuccess(true);
      setTimeout(() => {
        setSuccess(false);
        onClose();
      }, 1800);
    } catch (err) {
      setError(err.message || 'Failed to submit report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-deep/80 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-md bg-navy-surface rounded-2xl border border-border border-t-2 border-t-gold-500 shadow-2xl p-6 relative text-ink">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-ink-muted hover:text-ink hover:bg-navy-raised"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-4 pb-2 border-b border-border">
          <div className="p-2 rounded-lg bg-navy text-verdict-danger border border-verdict-danger/30">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-ink text-base">Report Threat Incident</h3>
            <p className="text-xs text-ink-muted">Helps protect other citizens across India.</p>
          </div>
        </div>

        {success ? (
          <div className="py-8 text-center text-verdict-safe">
            <CheckCircle className="w-12 h-12 mx-auto mb-2 animate-bounce" />
            <p className="font-bold">Threat Report Recorded!</p>
            <p className="text-xs text-ink-muted mt-1">Thank you for helping safeguard digital payments.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-2.5 text-xs rounded-lg bg-verdict-danger/15 text-rose-600 dark:text-rose-300 border border-verdict-danger/30">
                {error}
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-ink-muted mb-1">
                Category
              </label>
              <input
                type="text"
                disabled
                value={defaultCategory}
                className="w-full px-3 py-2 text-xs rounded-lg bg-navy border border-border text-ink"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-ink-muted mb-1">
                Additional Observations / Comments (Optional)
              </label>
              <textarea
                rows="3"
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                placeholder="E.g., received via WhatsApp from unknown number asking to verify SBI card..."
                className="w-full px-3 py-2 text-xs rounded-lg bg-navy border border-border text-ink focus:border-teal placeholder-[#7C89A6]"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-ink-muted mb-1">
                Your Contact / Phone (Optional, will be masked)
              </label>
              <input
                type="text"
                value={contact}
                onChange={(e) => setContact(e.target.value)}
                placeholder="+91-98XXXXXXXX"
                className="w-full px-3 py-2 text-xs rounded-lg bg-navy border border-border text-ink focus:border-teal placeholder-[#7C89A6]"
              />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-navy-raised hover:bg-border text-ink border border-border"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="btn-gold-primary px-4 py-2 text-xs font-bold rounded-lg flex items-center gap-1.5"
              >
                <Send className="w-3.5 h-3.5" />
                {loading ? 'Submitting...' : 'Submit Report'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
