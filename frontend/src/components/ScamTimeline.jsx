import React from 'react';
import { GitCommit, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function ScamTimeline({ story }) {
  if (!story || !story.steps || story.steps.length === 0) return null;

  return (
    <div className="bg-navy-surface/90 rounded-2xl p-5 border border-border">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <GitCommit className="w-5 h-5 text-gold-400" />
          <h4 className="text-base font-semibold text-ink">
            Attack Playbook Timeline: {story.category_name}
          </h4>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-gold-400/10 text-gold-300 border border-gold-400/30 font-medium">
          3-Stage Attack Anatomy
        </span>
      </div>

      <p className="text-xs text-ink-muted mb-5 leading-relaxed">
        {story.overview}
      </p>

      <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-gradient-to-b before:from-gold-400 before:via-verdict-suspicious before:to-verdict-danger">
        {story.steps.map((st) => (
          <div key={st.step_number} className="relative group">
            {/* Step dot */}
            <div className="absolute -left-[27px] top-1 w-6 h-6 rounded-full bg-navy border-2 border-gold-400 flex items-center justify-center text-[10px] font-bold text-gold-300 shadow-md">
              {st.step_number}
            </div>

            <div className="bg-navy/90 p-4 rounded-xl border border-border group-hover:border-teal-400/60 transition-all">
              <div className="flex items-center justify-between gap-2 mb-1.5 flex-wrap">
                <span className="text-[11px] font-bold uppercase tracking-wider text-gold-400">
                  {st.stage}
                </span>
                <span className="text-xs font-semibold text-ink">
                  {st.title}
                </span>
              </div>

              <p className="text-xs text-ink-muted leading-relaxed mb-3">
                {st.description}
              </p>

              <div className="flex items-start gap-2 bg-verdict-danger/10 border border-verdict-danger/30 p-2.5 rounded-lg text-xs text-ink">
                <AlertTriangle className="w-4 h-4 text-verdict-danger shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-verdict-danger">Warning Signal: </span>
                  <span className="text-ink-muted">{st.warning_sign}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
