import React, { useState, useEffect } from 'react';
import { CheckCircle2, Circle, ExternalLink, PhoneCall } from 'lucide-react';

export default function CheckableStepsCard({ steps = [], language = 'en', messageId = 'default' }) {
  const storageKey = `rakshak_steps_${messageId}`;
  
  const [completed, setCompleted] = useState(() => {
    try {
      const saved = sessionStorage.getItem(storageKey);
      return saved ? JSON.parse(saved) : {};
    } catch {
      return {};
    }
  });

  const toggleStep = (idx) => {
    setCompleted((prev) => {
      const next = { ...prev, [idx]: !prev[idx] };
      try {
        sessionStorage.setItem(storageKey, JSON.stringify(next));
      } catch {}
      return next;
    });
  };

  const doneCount = Object.values(completed).filter(Boolean).length;
  const allDone = steps.length > 0 && doneCount === steps.length;

  const labels = {
    en: { header: "What To Do Now (Action Checklist)", progress: `${doneCount} of ${steps.length} completed`, allDone: "All steps complete! Keep evidence secure." },
    hi: { header: "अब क्या करें (कार्य सूची)", progress: `${steps.length} में से ${doneCount} पूरे हुए`, allDone: "सभी चरण पूरे हुए! साक्ष्य सुरक्षित रखें।" },
    te: { header: "ఇప్పుడు ఏమి చేయాలి (చర్యల జాబితా)", progress: `${steps.length} లో ${doneCount} పూర్తయ్యాయి`, allDone: "అన్ని చర్యలు పూర్తయ్యాయి! ఆధారాలను భద్రపరచండి." }
  };

  const l = labels[language] || labels.en;

  if (!steps || steps.length === 0) return null;

  return (
    <div className="mt-3 p-3.5 bg-slate-900/90 border border-cyan-500/25 rounded-xl shadow-lg text-slate-100">
      <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800">
        <span className="text-xs font-bold text-cyan-400 font-sans tracking-wide uppercase">
          {l.header}
        </span>
        <span className="text-[11px] font-mono text-slate-400">
          {l.progress}
        </span>
      </div>

      <div className="space-y-2">
        {steps.map((step, idx) => {
          const isDone = !!completed[idx];
          const isPhoneStep = step.includes("1930");
          const isWebStep = step.includes("cybercrime.gov.in");

          return (
            <div
              key={idx}
              onClick={() => toggleStep(idx)}
              className={`flex items-start gap-2.5 p-2 rounded-lg cursor-pointer transition-all border ${
                isDone
                  ? 'bg-emerald-950/20 border-emerald-500/30 text-slate-300'
                  : 'bg-slate-800/50 hover:bg-slate-800 border-slate-700/60 text-slate-100'
              }`}
            >
              <button
                type="button"
                className="mt-0.5 shrink-0 text-slate-400 hover:text-cyan-400 transition-colors"
                aria-label={isDone ? "Mark incomplete" : "Mark complete"}
              >
                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <Circle className="w-4 h-4 text-slate-500" />
                )}
              </button>

              <div className="flex-1 text-xs leading-relaxed">
                <span className={isDone ? 'line-through text-slate-400' : 'text-slate-200'}>
                  {step}
                </span>

                {/* Inline Action Pills */}
                <div className="mt-1 flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                  {isPhoneStep && (
                    <a
                      href="tel:1930"
                      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-red-500/20 text-red-300 hover:bg-red-500/30 border border-red-500/30 transition-colors"
                    >
                      <PhoneCall className="w-3 h-3" /> Dial 1930
                    </a>
                  )}
                  {isWebStep && (
                    <a
                      href="https://cybercrime.gov.in"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-cyan-500/20 text-cyan-300 hover:bg-cyan-500/30 border border-cyan-500/30 transition-colors"
                    >
                      <ExternalLink className="w-3 h-3" /> cybercrime.gov.in
                    </a>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {allDone && (
        <div className="mt-2.5 p-2 bg-emerald-950/30 border border-emerald-500/40 rounded-lg text-center text-xs text-emerald-300 font-medium animate-fadeIn">
          {l.allDone}
        </div>
      )}
    </div>
  );
}
