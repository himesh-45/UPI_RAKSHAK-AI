import React from 'react';
import { ArrowUpRight, ArrowDownRight, Layers, HelpCircle } from 'lucide-react';

export default function ScoreWaterfall({ waterfall = [] }) {
  if (!waterfall || waterfall.length === 0) return null;

  return (
    <div className="bg-slate-900/60 rounded-xl p-5 border border-slate-800">
      <div className="flex items-center gap-2 mb-4">
        <Layers className="w-5 h-5 text-indigo-400" />
        <h4 className="text-base font-semibold text-white">Score Waterfall & Evidence Decomposition</h4>
      </div>

      <div className="space-y-3">
        {waterfall.map((step, idx) => {
          const isPositive = step.points > 0;
          const isZero = step.points === 0;
          const isNegative = step.points < 0;

          return (
            <div
              key={idx}
              className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-lg bg-slate-950/50 border border-slate-800/80 hover:border-slate-700/80 transition-all text-xs sm:text-sm"
            >
              <div className="flex-1 pr-3">
                <div className="flex items-center gap-2 font-medium text-slate-200">
                  <span>{step.component}</span>
                  {step.explanation && (
                    <span className="text-[11px] text-slate-400 hidden md:inline font-normal">
                      — {step.explanation}
                    </span>
                  )}
                </div>
                {step.explanation && (
                  <p className="text-[11px] text-slate-400 mt-0.5 md:hidden font-normal">
                    {step.explanation}
                  </p>
                )}
              </div>

              <div className="flex items-center gap-3 mt-2 sm:mt-0 shrink-0">
                <span
                  className={`inline-flex items-center font-bold px-2 py-0.5 rounded text-xs ${
                    isPositive
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                      : isNegative
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                      : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {isPositive && <ArrowUpRight className="w-3.5 h-3.5 mr-0.5 inline" />}
                  {isNegative && <ArrowDownRight className="w-3.5 h-3.5 mr-0.5 inline" />}
                  {isPositive ? `+${step.points}` : step.points} pts
                </span>

                <div className="w-20 text-right font-mono font-semibold text-slate-300">
                  <span className="text-[10px] text-slate-500 block uppercase">Subtotal</span>
                  <span>{step.running_total} / 100</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
