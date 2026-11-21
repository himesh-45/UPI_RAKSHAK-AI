import React from 'react';
import { PhoneCall, CheckCircle, XCircle, AlertOctagon } from 'lucide-react';

export default function ActionBox({ actions = [], verdict = 'SAFE' }) {
  const isHighRisk = verdict === 'HIGH RISK';

  return (
    <div className="space-y-4">
      {/* 1930 Emergency Helpline Banner */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-indigo-900 to-slate-900 text-white shadow-md border border-indigo-700/50 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-indigo-600/30 border border-indigo-500/40 text-amber-300">
            <PhoneCall className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider text-indigo-300 font-bold">
              National Cyber Crime Reporting Helpline
            </div>
            <div className="text-xl font-extrabold tracking-tight flex items-center gap-2">
              <span>Dial 1930</span>
              <span className="text-xs font-normal text-slate-300">| 24x7 Toll-Free</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <a
            href="tel:1930"
            className="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs uppercase tracking-wider shadow transition"
          >
            Call 1930
          </a>
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs transition"
          >
            cybercrime.gov.in
          </a>
        </div>
      </div>

      {/* Action items list */}
      <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3 flex items-center gap-1.5">
          <AlertOctagon className="w-4 h-4 text-indigo-500" />
          Recommended Immediate Action Steps
        </h4>

        <div className="space-y-2.5">
          {actions.map((act, idx) => {
            const isNegative = act.toLowerCase().includes('not') || act.toLowerCase().includes('न करें') || act.toLowerCase().includes('వద్దు');
            return (
              <div key={idx} className="flex items-start gap-2.5 text-sm text-slate-700 dark:text-slate-300">
                {isNegative ? (
                  <XCircle className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
                ) : (
                  <CheckCircle className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                )}
                <span>{act}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
