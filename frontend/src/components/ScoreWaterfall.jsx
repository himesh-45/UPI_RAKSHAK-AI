import React from 'react';
import { ArrowUpRight, ArrowDownRight, Layers, HelpCircle } from 'lucide-react';

export default function ScoreWaterfall({ waterfall = [] }) {
  if (!waterfall || waterfall.length === 0) return null;

  return (
    <div className="bg-[#0F1D3A]/90 rounded-2xl p-5 border border-[#1E3A5F]">
      <div className="flex items-center gap-2 mb-4">
        <Layers className="w-5 h-5 text-teal-400" />
        <h4 className="text-base font-semibold text-ink">Score Waterfall & Evidence Decomposition</h4>
      </div>

      <div className="space-y-3">
        {waterfall.map((step, idx) => {
          const isPositive = step.points > 0;
          const isZero = step.points === 0;
          const isNegative = step.points < 0;

          return (
            <div
              key={idx}
              className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-[#070E22]/90 border border-[#1E3A5F] hover:border-teal-400/60 transition-all text-xs sm:text-sm"
            >
              <div className="flex-1 pr-3">
                <div className="flex items-center gap-2 font-medium text-ink">
                  <span>{step.component}</span>
                  {step.explanation && (
                    <span className="text-[11px] text-ink-muted hidden md:inline font-normal">
                      — {step.explanation}
                    </span>
                  )}
                </div>
                {step.explanation && (
                  <p className="text-[11px] text-ink-muted mt-0.5 md:hidden font-normal">
                    {step.explanation}
                  </p>
                )}
              </div>

              <div className="flex items-center gap-3 mt-2 sm:mt-0 shrink-0">
                <span
                  className={`inline-flex items-center font-bold px-2 py-0.5 rounded text-xs ${
                    isPositive
                      ? 'bg-verdict-danger/20 text-verdict-danger border border-verdict-danger/30'
                      : isNegative
                      ? 'bg-verdict-safe/20 text-verdict-safe border border-verdict-safe/30'
                      : 'bg-[#0B1530] text-ink-muted border border-[#1E3A5F]'
                  }`}
                >
                  {isPositive && <ArrowUpRight className="w-3.5 h-3.5 mr-0.5 inline" />}
                  {isNegative && <ArrowDownRight className="w-3.5 h-3.5 mr-0.5 inline" />}
                  {isPositive ? `+${step.points}` : step.points} pts
                </span>

                <div className="w-20 text-right font-mono font-semibold text-ink">
                  <span className="text-[10px] text-ink-muted block uppercase">Subtotal</span>
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
