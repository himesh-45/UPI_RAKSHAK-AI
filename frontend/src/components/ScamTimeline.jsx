import React from 'react';
import { GitCommit, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function ScamTimeline({ story }) {
  if (!story || !story.steps || story.steps.length === 0) return null;

  return (
    <div className="bg-slate-900/60 rounded-xl p-5 border border-slate-800">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <GitCommit className="w-5 h-5 text-amber-400" />
          <h4 className="text-base font-semibold text-white">
            Attack Playbook Timeline: {story.category_name}
          </h4>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/20 font-medium">
          3-Stage Attack Anatomy
        </span>
      </div>

      <p className="text-xs text-slate-400 mb-5 leading-relaxed">
        {story.overview}
      </p>

      <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-gradient-to-b before:from-amber-500 before:via-orange-500 before:to-rose-500">
        {story.steps.map((st) => (
          <div key={st.step_number} className="relative group">
            {/* Step dot */}
            <div className="absolute -left-[27px] top-1 w-6 h-6 rounded-full bg-slate-900 border-2 border-amber-400 flex items-center justify-center text-[10px] font-bold text-amber-300 shadow-md">
              {st.step_number}
            </div>

            <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800/80 group-hover:border-slate-700 transition-all">
              <div className="flex items-center justify-between gap-2 mb-1.5 flex-wrap">
                <span className="text-[11px] font-bold uppercase tracking-wider text-amber-400">
                  {st.stage}
                </span>
                <span className="text-xs font-semibold text-slate-100">
                  {st.title}
                </span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed mb-3">
                {st.description}
              </p>

              <div className="flex items-start gap-2 bg-rose-950/30 border border-rose-900/50 p-2.5 rounded-lg text-xs text-rose-200">
                <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-rose-300">Warning Signal: </span>
                  <span>{st.warning_sign}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
