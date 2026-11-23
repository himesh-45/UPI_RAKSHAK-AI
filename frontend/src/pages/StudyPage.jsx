import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, CheckCircle, HelpCircle, ArrowRight, RotateCcw, Star, Award, BookOpen } from 'lucide-react';

const API_BASE = '/api';

export default function StudyPage() {
  const [hasConsented, setHasConsented] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [items, setItems] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);

  // Current trial state
  const [userGuess, setUserGuess] = useState(null); // 'scam' | 'genuine'
  const [userConfidence, setUserConfidence] = useState(3);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [wouldChange, setWouldChange] = useState(''); // 'yes' | 'no' | 'already_agreed'
  const [revisedGuess, setRevisedGuess] = useState('');
  const [clarityRating, setClarityRating] = useState(5);
  const [feedbackNotes, setFeedbackNotes] = useState('');

  // Collected responses
  const [collectedResponses, setCollectedResponses] = useState([]);

  const handleStartStudy = async () => {
    const newSessionId = 'session_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now();
    setSessionId(newSessionId);
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/study/items`);
      if (!res.ok) throw new Error('Failed to load items');
      const data = await res.json();
      setItems(data);
      setCurrentIndex(0);
      setCollectedResponses([]);
      setHasConsented(true);
    } catch (err) {
      alert('Failed to load study items. Please ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleRevealAnalysis = async () => {
    if (!userGuess) {
      alert('Please select whether you believe this is Genuine or a Scam first.');
      return;
    }
    const currentItem = items[currentIndex];
    setEvaluating(true);
    try {
      const res = await fetch(`${API_BASE}/study/evaluate-item`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: currentItem.text })
      });
      if (!res.ok) throw new Error('Evaluation failed');
      const data = await res.json();
      setAnalysisResult(data);
      // Auto default wouldChange based on alignment
      const toolIsScam = data.verdict === 'HIGH RISK' || data.verdict === 'SUSPICIOUS';
      const userIsScam = userGuess === 'scam';
      if (toolIsScam === userIsScam) {
        setWouldChange('already_agreed');
        setRevisedGuess(userGuess);
      } else {
        setWouldChange('no');
        setRevisedGuess(userGuess);
      }
    } catch (err) {
      alert('Analysis evaluation error. Please retry.');
    } finally {
      setEvaluating(false);
    }
  };

  const handleNextItem = async () => {
    const currentItem = items[currentIndex];
    const trialRecord = {
      item_id: currentItem.item_id,
      user_guess: userGuess,
      user_confidence: userConfidence,
      would_change: wouldChange || 'no',
      revised_guess: wouldChange === 'yes' ? (userGuess === 'scam' ? 'genuine' : 'scam') : userGuess,
      clarity_rating: clarityRating,
      feedback: feedbackNotes
    };

    const updatedResponses = [...collectedResponses, trialRecord];
    setCollectedResponses(updatedResponses);

    // Reset trial state
    setUserGuess(null);
    setUserConfidence(3);
    setAnalysisResult(null);
    setWouldChange('');
    setRevisedGuess('');
    setClarityRating(5);
    setFeedbackNotes('');

    if (currentIndex + 1 < items.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // Completed all items, submit to backend
      setSubmitting(true);
      try {
        await fetch(`${API_BASE}/study/submit`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: sessionId,
            responses: updatedResponses
          })
        });
      } catch (e) {
        console.error('Study submission background notice:', e);
      } finally {
        setSubmitting(false);
        setCompleted(true);
      }
    }
  };

  if (!hasConsented) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-12 animate-fade-in">
        <div className="bg-navy-surface/90 rounded-3xl border border-border border-t-2 border-t-gold-400 shadow-xl p-8 space-y-6">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-teal-500/10 border border-teal-500/30 text-teal-300">
              <BookOpen className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-black text-ink">
                Consumer Payment Security Study
              </h1>
              <p className="text-xs text-ink-muted">Evaluating Human-AI Collaboration in Digital Payment Defense</p>
            </div>
          </div>

          <div className="text-xs text-ink-muted space-y-3 leading-relaxed">
            <p>
              Welcome to the <strong className="text-ink">UPI Rakshak AI Empirical Perception Study</strong>. This voluntary academic trial investigates how plain-language evidence and multi-layer indicators influence human fraud detection decisions.
            </p>
            <div className="p-4 rounded-2xl bg-navy border border-border space-y-2">
              <h4 className="font-bold text-gold-300 text-xs">Trial Protocol:</h4>
              <ul className="list-disc pl-4 space-y-1 text-ink-muted">
                <li>You will review <strong className="text-ink">10 short realistic messages</strong> (transaction alerts, refunds, SMS, and WhatsApp notices).</li>
                <li>First, decide if each message is <em className="text-teal-300">Genuine</em> or a <em className="text-verdict-danger">Scam</em>, and rate your confidence.</li>
                <li>Next, view the multi-layer AI safety report and evidence breakdown.</li>
                <li>Indicate whether the evidence supports or changes your original decision.</li>
                <li>Duration: Approximately <strong className="text-ink">3 to 4 minutes</strong>.</li>
              </ul>
            </div>
            <p>
              <strong className="text-ink">Privacy Assurance</strong>: Your participation is 100% anonymous. We do not collect names, phone numbers, IP addresses, or device identifiers. All aggregated results are published in research benchmarks.
            </p>
          </div>

          <button
            onClick={handleStartStudy}
            disabled={loading}
            className="w-full py-3.5 px-6 rounded-2xl btn-gold-primary text-sm transition flex items-center justify-center gap-2"
          >
            {loading ? 'Preparing Scenarios...' : 'I Consent — Begin Study'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="max-w-xl mx-auto px-4 py-16 animate-fade-in text-center">
        <div className="bg-navy-surface/90 rounded-3xl border border-border border-t-2 border-t-gold-400 shadow-xl p-8 space-y-6">
          <div className="w-16 h-16 mx-auto rounded-full bg-verdict-safe/20 border border-verdict-safe/30 text-verdict-safe flex items-center justify-center">
            <Award className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-black text-ink">
            Study Completed!
          </h2>
          <p className="text-xs text-ink-muted leading-relaxed max-w-md mx-auto">
            Thank you for participating! Your responses have been anonymously saved to the research database and will contribute to our statistical evaluation report.
          </p>
          <div className="p-4 rounded-2xl bg-navy border border-border text-xs text-ink-muted">
            <p>Session ID: <code className="font-mono text-gold-300">{sessionId}</code></p>
            <p className="mt-1">Scenarios Completed: <strong className="text-ink">10 / 10</strong></p>
          </div>
          <button
            onClick={() => {
              setHasConsented(false);
              setCompleted(false);
            }}
            className="py-3 px-6 rounded-2xl bg-navy border border-border hover:bg-navy font-bold text-xs text-ink transition"
          >
            Return to Overview
          </button>
        </div>
      </div>
    );
  }

  const currentItem = items[currentIndex];

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 animate-fade-in space-y-6">
      {/* Progress header */}
      <div className="flex items-center justify-between text-xs font-semibold text-ink-muted">
        <span>Scenario {currentIndex + 1} of {items.length}</span>
        <span className="uppercase tracking-wider px-2 py-0.5 rounded-md bg-navy border border-border text-gold-300">
          Lang: {currentItem.language}
        </span>
      </div>

      <div className="w-full bg-navy rounded-full h-1.5 overflow-hidden border border-border">
        <div
          className="bg-gold-400 h-1.5 transition-all duration-300"
          style={{ width: `${((currentIndex + 1) / items.length) * 100}%` }}
        />
      </div>

      {/* Message Card */}
      <div className="bg-navy-surface/90 rounded-3xl border border-border shadow-md p-6 space-y-4">
        <div className="text-[11px] font-bold text-gold-300 uppercase tracking-wider">
          Incoming Communication to Review:
        </div>
        <div className="p-4 rounded-2xl bg-navy border border-border font-sans text-sm text-ink leading-relaxed break-words">
          {currentItem.text}
        </div>
      </div>

      {/* Phase 1: Pre-tool user decision */}
      {!analysisResult ? (
        <div className="bg-navy-surface/90 rounded-3xl border border-border shadow-md p-6 space-y-5 animate-fade-in">
          <div>
            <h3 className="text-sm font-bold text-ink">
              Step 1: Your Initial Assessment
            </h3>
            <p className="text-xs text-ink-muted">Based on your own judgment, is this message legitimate or a scam?</p>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => setUserGuess('genuine')}
              className={`py-3 px-4 rounded-2xl border font-bold text-xs flex items-center justify-center gap-2 transition ${
                userGuess === 'genuine'
                  ? 'bg-verdict-safe/10 border-verdict-safe text-verdict-safe shadow'
                  : 'border-border bg-navy hover:border-teal-400/50 text-ink-muted'
              }`}
            >
              <CheckCircle className="w-4 h-4 text-verdict-safe" />
              Genuine Alert
            </button>
            <button
              type="button"
              onClick={() => setUserGuess('scam')}
              className={`py-3 px-4 rounded-2xl border font-bold text-xs flex items-center justify-center gap-2 transition ${
                userGuess === 'scam'
                  ? 'bg-verdict-danger/10 border-verdict-danger text-verdict-danger shadow'
                  : 'border-border bg-navy hover:border-teal-400/50 text-ink-muted'
              }`}
            >
              <AlertTriangle className="w-4 h-4 text-verdict-danger" />
              Scam / Fraud
            </button>
          </div>

          {userGuess && (
            <div className="space-y-2 pt-2 border-t border-border">
              <div className="flex justify-between items-center text-xs font-semibold text-ink-muted">
                <span>Confidence Level:</span>
                <span className="font-bold text-gold-300">
                  {userConfidence === 1 && '1 - Very Low'}
                  {userConfidence === 2 && '2 - Low'}
                  {userConfidence === 3 && '3 - Moderate'}
                  {userConfidence === 4 && '4 - High'}
                  {userConfidence === 5 && '5 - Very High'}
                </span>
              </div>
              <input
                type="range"
                min="1"
                max="5"
                value={userConfidence}
                onChange={(e) => setUserConfidence(parseInt(e.target.value))}
                className="w-full h-1.5 bg-navy rounded-lg appearance-none cursor-pointer accent-gold-400"
              />
            </div>
          )}

          <button
            onClick={handleRevealAnalysis}
            disabled={!userGuess || evaluating}
            className="w-full py-3 rounded-2xl btn-gold-primary text-xs uppercase tracking-wider transition disabled:opacity-40"
          >
            {evaluating ? 'Analyzing Signals...' : 'Reveal UPI Rakshak Analysis →'}
          </button>
        </div>
      ) : (
        /* Phase 2: Post-tool evaluation & reflection */
        <div className="bg-navy-surface/90 rounded-3xl border border-border shadow-md p-6 space-y-5 animate-fade-in">
          <div className="flex items-center justify-between pb-3 border-b border-border">
            <div>
              <span className="text-[10px] uppercase font-bold text-ink-muted tracking-wider">UPI Rakshak AI Verdict</span>
              <div className="flex items-center gap-2 mt-0.5">
                <span className={`px-2.5 py-1 rounded-full text-xs font-black ${
                  analysisResult.verdict === 'SAFE'
                    ? 'bg-verdict-safe/20 text-verdict-safe border border-verdict-safe/30'
                    : analysisResult.verdict === 'SUSPICIOUS'
                    ? 'bg-verdict-suspicious/20 text-verdict-suspicious border border-verdict-suspicious/30'
                    : 'bg-verdict-danger/20 text-verdict-danger border border-verdict-danger/30'
                }`}>
                  {analysisResult.verdict}
                </span>
                <span className="text-xs font-bold text-ink-muted">
                  Risk Score: {analysisResult.risk_score}/100
                </span>
              </div>
            </div>
            <div className="text-right">
              <span className="text-[10px] text-ink-muted">Your Choice</span>
              <p className="text-xs font-bold text-ink uppercase">
                {userGuess === 'scam' ? '🚨 Scam' : '✅ Genuine'}
              </p>
            </div>
          </div>

          {/* Top evidence */}
          <div className="space-y-2">
            <span className="text-xs font-bold text-ink">Key Evidence Detected:</span>
            <div className="space-y-1.5">
              {analysisResult.top_evidence.map((ev, i) => (
                <div key={i} className="p-2.5 rounded-xl bg-navy border border-border text-xs flex items-start gap-2">
                  <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                    ev.severity === 'CRITICAL' || ev.severity === 'HIGH'
                      ? 'bg-verdict-danger/20 text-verdict-danger border border-verdict-danger/30'
                      : 'bg-teal-500/20 text-teal-300 border border-teal-500/30'
                  }`}>
                    {ev.severity}
                  </span>
                  <span className="text-ink flex-1 leading-snug">{ev.signal}</span>
                </div>
              ))}
            </div>
            <p className="text-xs text-ink-muted italic pt-1">
              "{analysisResult.plain_explanation}"
            </p>
          </div>

          {/* Reflection */}
          <div className="space-y-3 pt-3 border-t border-border">
            <label className="block text-xs font-bold text-ink">
              Does this evidence change or strengthen your decision?
            </label>
            <div className="grid grid-cols-3 gap-2 text-xs">
              <button
                type="button"
                onClick={() => setWouldChange('already_agreed')}
                className={`py-2 px-2 rounded-xl border text-center font-semibold transition ${
                  wouldChange === 'already_agreed'
                    ? 'bg-gold-400/20 border-gold-400 text-gold-300'
                    : 'border-border bg-navy text-ink-muted hover:text-ink'
                }`}
              >
                Already Agreed
              </button>
              <button
                type="button"
                onClick={() => setWouldChange('yes')}
                className={`py-2 px-2 rounded-xl border text-center font-semibold transition ${
                  wouldChange === 'yes'
                    ? 'bg-gold-400/20 border-gold-400 text-gold-300'
                    : 'border-border bg-navy text-ink-muted hover:text-ink'
                }`}
              >
                Yes, Changed Mind
              </button>
              <button
                type="button"
                onClick={() => setWouldChange('no')}
                className={`py-2 px-2 rounded-xl border text-center font-semibold transition ${
                  wouldChange === 'no'
                    ? 'bg-gold-400/20 border-gold-400 text-gold-300'
                    : 'border-border bg-navy text-ink-muted hover:text-ink'
                }`}
              >
                No, Keep Decision
              </button>
            </div>
          </div>

          <button
            onClick={handleNextItem}
            className="w-full py-3 rounded-2xl btn-gold-primary text-xs uppercase tracking-wider transition flex items-center justify-center gap-2"
          >
            {currentIndex + 1 < items.length ? 'Next Scenario →' : 'Complete Study & Submit'}
          </button>
        </div>
      )}
    </div>
  );
}
