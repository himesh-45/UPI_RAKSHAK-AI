import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown, Check, X, AlertCircle } from 'lucide-react';
import { submitFeedback } from '../api/client';

const CATEGORY_OPTIONS = [
  { value: 'legitimate', label: 'Legitimate / Genuine Message' },
  { value: 'fake_bank_kyc', label: 'Fake Bank KYC Phishing' },
  { value: 'electricity_disconnection', label: 'Electricity Disconnection Threat' },
  { value: 'fake_upi_refund_cashback', label: 'Fake UPI Refund / Cashback' },
  { value: 'collect_request_fraud', label: 'UPI Collect Request PIN Fraud' },
  { value: 'lottery_prize', label: 'KBC Lottery & Advance-Fee Scam' },
  { value: 'fake_customer_support', label: 'Fake Customer Care Helpline' },
  { value: 'remote_access_scam', label: 'Remote Access App (AnyDesk)' },
  { value: 'otp_pin_theft', label: 'Credential & OTP/PIN Theft' },
  { value: 'fake_govt_scheme', label: 'Fake Govt Scheme / Subsidy' },
  { value: 'job_investment_scam', label: 'Part-Time Task & Crypto Investment' },
  { value: 'loan_app_extortion', label: 'Predatory Loan App Extortion' },
  { value: 'courier_customs_scam', label: 'Courier / Digital Arrest Scam' },
  { value: 'marketplace_qr_scam', label: 'OLX / Marketplace QR Scam' },
  { value: 'wrong_number_transfer', label: 'Accidental Money Sent Trap' },
];

export default function FeedbackModal({ isOpen, onClose, report, rawInput }) {
  const [step, setStep] = useState('initial'); // 'initial' | 'correction' | 'success'
  const [correctCategory, setCorrectCategory] = useState('legitimate');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen || !report) return null;

  const handlePositive = async () => {
    setLoading(true);
    setError('');
    try {
      await submitFeedback({
        analysis_id: report.id || null,
        input_text: rawInput || report.masked_input || '',
        reported_verdict: report.verdict,
        is_correct: true,
        correct_category: report.detected_category,
        feedback_notes: 'User verified verdict as correct.'
      });
      setStep('success');
      setTimeout(() => {
        onClose();
        setStep('initial');
      }, 1800);
    } catch (err) {
      setError(err.message || 'Failed to submit feedback');
    } finally {
      setLoading(false);
    }
  };

  const handleNegativeSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await submitFeedback({
        analysis_id: report.id || null,
        input_text: rawInput || report.masked_input || '',
        reported_verdict: report.verdict,
        is_correct: false,
        correct_category: correctCategory,
        feedback_notes: notes.trim()
      });
      setStep('success');
      setTimeout(() => {
        onClose();
        setStep('initial');
      }, 1800);
    } catch (err) {
      setError(err.message || 'Failed to submit feedback');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-deep/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-navy-surface border border-border border-t-2 border-t-gold-500 w-full max-w-md rounded-2xl shadow-2xl overflow-hidden p-6 text-sm text-ink">
        <div className="flex items-center justify-between mb-4 pb-2 border-b border-border">
          <h3 className="text-base font-bold text-ink flex items-center gap-2">
            Model Evaluation Feedback
          </h3>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-ink-muted hover:text-ink hover:bg-navy-raised"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-verdict-danger/15 border border-verdict-danger/30 text-rose-600 dark:text-rose-300 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-verdict-danger" />
            <span>{error}</span>
          </div>
        )}

        {step === 'initial' && (
          <div className="space-y-4">
            <p className="text-ink-muted text-xs leading-relaxed">
              Help make UPI Rakshak AI more accurate for millions of Indian digital payment users. Was our verdict (<strong className="text-ink">{report.verdict}</strong>) correct for this sample?
            </p>

            <div className="grid grid-cols-2 gap-3 pt-2">
              <button
                onClick={handlePositive}
                disabled={loading}
                className="flex items-center justify-center gap-2 p-3 rounded-xl bg-verdict-safe/15 hover:bg-verdict-safe/25 text-verdict-safe border border-verdict-safe/30 font-semibold text-xs transition-all"
              >
                <ThumbsUp className="w-4 h-4 text-verdict-safe" />
                Yes, Accurate
              </button>
              <button
                onClick={() => setStep('correction')}
                disabled={loading}
                className="flex items-center justify-center gap-2 p-3 rounded-xl bg-verdict-danger/15 hover:bg-verdict-danger/25 text-verdict-danger border border-verdict-danger/30 font-semibold text-xs transition-all"
              >
                <ThumbsDown className="w-4 h-4 text-verdict-danger" />
                Report Error
              </button>
            </div>
          </div>
        )}

        {step === 'correction' && (
          <form onSubmit={handleNegativeSubmit} className="space-y-4">
            <p className="text-ink-muted text-xs">
              What was the actual nature of this message?
            </p>

            <div>
              <label className="text-[11px] text-ink-muted block mb-1 font-medium">
                Correct Category:
              </label>
              <select
                value={correctCategory}
                onChange={(e) => setCorrectCategory(e.target.value)}
                className="w-full bg-navy border border-border rounded-xl px-3 py-2 text-xs text-ink focus:outline-none focus:border-teal"
              >
                {CATEGORY_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value} className="bg-navy text-ink">
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-[11px] text-ink-muted block mb-1 font-medium">
                Notes (Optional):
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
                placeholder="Why do you consider this verdict incorrect?"
                className="w-full bg-navy border border-border rounded-xl p-3 text-xs text-ink focus:outline-none focus:border-teal resize-none placeholder-[#7C89A6]"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setStep('initial')}
                className="px-3 py-1.5 rounded-lg bg-navy-raised hover:bg-border text-ink border border-border text-xs"
              >
                Back
              </button>
              <button
                type="submit"
                disabled={loading}
                className="btn-gold-primary px-4 py-1.5 rounded-lg font-bold text-xs transition-colors"
              >
                {loading ? 'Submitting...' : 'Submit Correction'}
              </button>
            </div>
          </form>
        )}

        {step === 'success' && (
          <div className="py-6 text-center space-y-2">
            <div className="w-12 h-12 rounded-full bg-verdict-safe/20 text-verdict-safe border border-verdict-safe/30 mx-auto flex items-center justify-center">
              <Check className="w-6 h-6" />
            </div>
            <h4 className="font-bold text-ink text-sm">Feedback Recorded!</h4>
            <p className="text-xs text-ink-muted">
              Your feedback has been logged to the retraining queue.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
