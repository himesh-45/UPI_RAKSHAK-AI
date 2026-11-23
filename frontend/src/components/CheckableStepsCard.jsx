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
    <div className="mt-3 p-3.5 bg-[#0F1D3A]/95 border border-[#1E3A5F] rounded-xl shadow-lg text-[#F5F1E6]">
      <div className="flex items-center justify-between pb-2 mb-2 border-b border-[#1E3A5F]">
        <span className="text-xs font-bold text-[#35D0C8] font-sans tracking-wide uppercase">
          {l.header}
        </span>
        <span className="text-[11px] font-mono text-[#A9B4CC]">
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
                  ? 'bg-[#34D399]/10 border-[#34D399]/30 text-[#A9B4CC]'
                  : 'bg-[#0B1530] hover:bg-[#14254B] border-[#1E3A5F] text-[#F5F1E6]'
              }`}
            >
              <button
                type="button"
                className="mt-0.5 shrink-0 text-[#7C89A6] hover:text-[#35D0C8] transition-colors"
                aria-label={isDone ? "Mark incomplete" : "Mark complete"}
              >
                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-[#34D399]" />
                ) : (
                  <Circle className="w-4 h-4 text-[#7C89A6]" />
                )}
              </button>

              <div className="flex-1 text-xs leading-relaxed">
                <span className={isDone ? 'line-through text-[#A9B4CC]' : 'text-[#F5F1E6]'}>
                  {step}
                </span>

                {/* Inline Action Pills */}
                <div className="mt-1 flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                  {isPhoneStep && (
                    <a
                      href="tel:1930"
                      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-[#F43F5E]/15 text-[#F43F5E] hover:bg-[#F43F5E]/25 border border-[#F43F5E]/30 transition-colors"
                    >
                      <PhoneCall className="w-3 h-3" /> Dial 1930
                    </a>
                  )}
                  {isWebStep && (
                    <a
                      href="https://cybercrime.gov.in"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-[#35D0C8]/15 text-[#35D0C8] hover:bg-[#35D0C8]/25 border border-[#35D0C8]/30 transition-colors"
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
        <div className="mt-2.5 p-2 bg-[#34D399]/15 border border-[#34D399]/40 rounded-lg text-center text-xs text-[#A7F3D0] font-medium animate-fadeIn">
          {l.allDone}
        </div>
      )}
    </div>
  );
}
