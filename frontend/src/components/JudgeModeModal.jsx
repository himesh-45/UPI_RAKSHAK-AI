import React from 'react';
import { X, Award, ArrowRight, ShieldAlert, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

export const JUDGE_SCENARIOS = [
  {
    id: 'telugu_otp',
    title: '1. Telugu OTP Phishing Scam',
    lang: 'Telugu (te-IN)',
    expectedVerdict: 'HIGH RISK',
    badgeColor: 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300',
    description: 'Tests Indic NLP comprehension, SOV word order, and credential theft rules in Telugu.',
    type: 'text',
    input: 'మీ బ్యాంక్ అకౌంట్ నిలిపివేయబడింది. వెంటనే మీ రహస్య ఓటీపీ (OTP) మరియు పిన్ నంబర్ చెప్పండి లేదా ఈ లింక్ ఓపెన్ చేయండి: http://sbi-kyc-verify.top'
  },
  {
    id: 'hindi_electricity',
    title: '2. Hindi Power Disconnection Scam',
    lang: 'Hindi (hi-IN)',
    expectedVerdict: 'HIGH RISK',
    badgeColor: 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300',
    description: 'Tests artificial urgency, utility threat, and unauthorized personal supervisor phone contact.',
    type: 'text',
    input: 'बिजली विभाग सूचना: आज रात 9:30 बजे आपके घर की बिजली काट दी जाएगी क्योंकि पिछला बिल अपडेट नहीं हुआ है। तुरंत बिजली अधिकारी 8920194820 पर कॉल करें और बिल का भुगतान करें।'
  },
  {
    id: 'collect_request',
    title: '3. UPI Collect Request Trick',
    lang: 'English (en-IN)',
    expectedVerdict: 'HIGH RISK',
    badgeColor: 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300',
    description: 'Tests detection of the classic "enter PIN to receive cashback" deception.',
    type: 'text',
    input: 'Paytm Diwali Cashback: You won Rs. 1,500 scratch reward. Accept payment request sent to your UPI VPA to claim balance instantly into your bank.'
  },
  {
    id: 'remote_access',
    title: '4. AnyDesk Remote Desktop Takeover',
    lang: 'English (en-IN)',
    expectedVerdict: 'HIGH RISK',
    badgeColor: 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300',
    description: 'Tests rule interception of remote assistance apps (AnyDesk/TeamViewer/QuickSupport).',
    type: 'text',
    input: 'HDFC Card Helpline: Your international payment failed. Immediately install AnyDesk app from play store and share your 9-digit code with support agent.'
  },
  {
    id: 'marketplace_qr',
    title: '5. OLX Army Buyer Fake QR Scam',
    lang: 'English / Hinglish',
    expectedVerdict: 'HIGH RISK',
    badgeColor: 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300',
    description: 'Tests impersonation of defense personnel and "scan QR to receive payment" trick.',
    type: 'text',
    input: 'I am an Indian Army soldier interested in your OLX sofa. Scan this UPI QR code to receive Rs. 15,000 advance payment directly into your bank.'
  },
  {
    id: 'adversarial_obfuscation',
    title: '6. Adversarial Obfuscation (Leetspeak & Spaced)',
    lang: 'English / Adversarial',
    expectedVerdict: 'HIGH RISK',
    badgeColor: 'bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300',
    description: 'Tests text normalizer: spaced "O  T  P", leetspeak "bl0cked", zero-width space de-obfuscation.',
    type: 'text',
    input: 'URGENT: Your account will be bl0cked t0night. Share the O  T  P and P - I - N with bank manager to unfreeze.'
  },
  {
    id: 'typosquat_url',
    title: '7. Subdomain Typosquatting Phishing URL',
    lang: 'Static URL Analysis',
    expectedVerdict: 'HIGH RISK',
    badgeColor: 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300',
    description: 'Tests tldextract registered domain isolation: not fooled by "sbi.co.in" in the subdomain prefix.',
    type: 'url',
    input: 'http://onlinesbi.sbi.co.in.kyc-verification.top/login.php?ref=sms'
  },
  {
    id: 'genuine_bank_alert',
    title: '8. Genuine Bank Alert (Benign Negative)',
    lang: 'English / Hard Negative',
    expectedVerdict: 'SAFE',
    badgeColor: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300',
    description: 'Tests warning context suppression: "NEVER share OTP" ensures legitimate notifications score SAFE.',
    type: 'text',
    input: 'HDFC Bank: Rs. 1,450.00 debited from a/c **4821 for Swiggy order. Avail Bal: Rs 34,200. NEVER share your OTP or UPI PIN with anyone.'
  }
];

export default function JudgeModeModal({ isOpen, onClose, onSelectScenario }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-sm animate-fade-in">
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl max-w-3xl w-full max-h-[90vh] flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-gradient-to-r from-amber-500/10 via-indigo-500/10 to-transparent">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-500/30">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-extrabold text-slate-900 dark:text-white">
                  Judge Mode — Guided Verification Scenarios
                </h3>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-amber-500 text-slate-950">
                  Live Demo
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Click any challenge scenario below to load it into the engine and verify detection.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scenarios Grid */}
        <div className="p-6 overflow-y-auto space-y-3 divide-y divide-slate-100 dark:divide-slate-800/60">
          {JUDGE_SCENARIOS.map((s) => (
            <div
              key={s.id}
              className="pt-3 first:pt-0 flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-3 rounded-2xl hover:bg-slate-50 dark:hover:bg-slate-800/40 transition group"
            >
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-indigo-500 transition">
                    {s.title}
                  </span>
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${s.badgeColor}`}>
                    Expected: {s.expectedVerdict}
                  </span>
                  <span className="text-[10px] text-slate-400 font-mono">
                    [{s.lang}]
                  </span>
                </div>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  {s.description}
                </p>
                <p className="text-[11px] font-mono text-slate-500 dark:text-slate-500 line-clamp-1 italic bg-slate-100 dark:bg-slate-950/70 p-1.5 rounded-lg border border-slate-200 dark:border-slate-800">
                  "{s.input}"
                </p>
              </div>

              <button
                onClick={() => {
                  onSelectScenario(s);
                  onClose();
                }}
                className="px-4 py-2 rounded-xl text-xs font-extrabold bg-indigo-600 hover:bg-indigo-500 text-white shrink-0 flex items-center justify-center gap-1.5 transition shadow-sm"
              >
                <span>Load & Test</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/50 flex items-center justify-between text-xs text-slate-500">
          <span>All 8 test scenarios are verified against our programmatic test suite.</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl text-xs font-bold bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
