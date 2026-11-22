import React, { useState } from 'react';
import { ChevronDown, ChevronUp, CheckCircle2, ShieldCheck, Activity, Cpu, Database, AlertCircle } from 'lucide-react';

export default function ModelHonestyPanel() {
  const [isOpen, setIsOpen] = useState(false);

  const gates = [
    {
      name: 'Risk Fusion Scam Recall',
      benchmark: '>= 95.0%',
      goldV1: '99.49%',
      goldV2: '98.55%',
      status: 'PASSED',
      desc: 'Sensitivity in capturing fraudulent vector attacks'
    },
    {
      name: 'Legitimate False Alarm Rate (FPR)',
      benchmark: '<= 3.0%',
      goldV1: '0.00%',
      goldV2: '1.90%',
      status: 'PASSED',
      desc: '0.00% on Gold v1 (0/110) and 1.90% on Gold v2 (2/105) across 215 genuine communications'
    },
    {
      name: '15-Class NLP Macro-F1',
      benchmark: '>= 0.8500',
      goldV1: '0.8994',
      goldV2: '0.8624',
      status: 'PASSED',
      desc: 'Attribution accuracy across all 15 fraud taxonomy classes'
    },
    {
      name: 'Expected Calibration Error (ECE)',
      benchmark: '< 0.1000',
      goldV1: '0.0992',
      goldV2: '0.1206',
      status: 'v1: PASS / v2: FAIL',
      desc: 'Calibrated confidence alignment (over-confident on colloquial Indic slang)'
    },
    {
      name: 'Static URL Phishing Recall',
      benchmark: '>= 80.0%',
      goldV1: '82.00%',
      goldV2: '98.60%',
      status: 'PASSED',
      desc: 'Real-feed OpenPhish (82.00%) & Synthetic adversarial holdout (98.60%)'
    },
    {
      name: 'Static URL Benign FPR',
      benchmark: '<= 3.0%',
      goldV1: '1.60%',
      goldV2: '1.12%',
      status: 'PASSED',
      desc: 'Real-feed Tranco-1000 (1.60%) & Disjoint benign domains (1.12%)'
    }
  ];

  return (
    <div className="bg-slate-50 dark:bg-slate-900/60 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 sm:p-6 transition">
      
      {/* Header Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-4 text-left group"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-extrabold text-slate-900 dark:text-white group-hover:text-indigo-500 transition">
                Engine Transparency & Programmatic Benchmark
              </h3>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
                5/6 Gates Passed (ECE Honest Disclosure)
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Programmatic benchmark. Derived directly from frozen Gold Test Set benchmarks.
            </p>
          </div>
        </div>

        <div className="p-1.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-500 shrink-0">
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </button>

      {/* Collapsible Content */}
      {isOpen && (
        <div className="pt-5 mt-4 border-t border-slate-200 dark:border-slate-800 space-y-5 animate-fade-in">
          
          {/* Honest Disclosure Banner */}
          <div className="p-3.5 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/40 text-xs text-amber-900 dark:text-amber-300 flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
            <div>
              <p className="font-bold">Honest Machine Learning Disclosure:</p>
              <p className="text-amber-800 dark:text-amber-400/90 text-[11px] leading-relaxed">
                Trained on synthetic multilingual attack templates and real public SMS spam corpora.
                Evaluated against hand-curated frozen gold test sets (Gold v1 = uniform 306-sample baseline; Gold v2 = messy human phrasings with typos and WhatsApp forwards). Real-world accuracy may vary on novel attack topologies.
              </p>
            </div>
          </div>

          {/* Quality Gates Table */}
          <div className="overflow-x-auto rounded-2xl border border-slate-200 dark:border-slate-800">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-100 dark:bg-slate-800/80 text-slate-600 dark:text-slate-300 font-bold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="p-3">Metric Dimension</th>
                  <th className="p-3 text-center">Benchmark Gate</th>
                  <th className="p-3 text-center">Frozen Gold v1</th>
                  <th className="p-3 text-center">Natural Gold v2</th>
                  <th className="p-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60 font-medium text-slate-700 dark:text-slate-300">
                {gates.map((g, i) => (
                  <tr key={i} className="hover:bg-slate-100/50 dark:hover:bg-slate-800/40 transition">
                    <td className="p-3">
                      <div className="font-bold text-slate-900 dark:text-white">{g.name}</div>
                      <div className="text-[11px] text-slate-400">{g.desc}</div>
                    </td>
                    <td className="p-3 text-center font-mono text-slate-500">{g.benchmark}</td>
                    <td className="p-3 text-center font-mono font-bold text-slate-900 dark:text-white">{g.goldV1}</td>
                    <td className="p-3 text-center font-mono font-bold text-slate-900 dark:text-white">{g.goldV2}</td>
                    <td className="p-3 text-center">
                      {g.status === 'PASSED' ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
                          <CheckCircle2 className="w-3 h-3" />
                          PASSED
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
                          <AlertCircle className="w-3 h-3" />
                          {g.status}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Performance & Footprint Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs">
            <div className="p-3 rounded-2xl bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 flex items-center gap-3">
              <Cpu className="w-5 h-5 text-indigo-500 shrink-0" />
              <div>
                <p className="font-extrabold text-slate-900 dark:text-white">~32 ms (p50)</p>
                <p className="text-[11px] text-slate-400">Multi-detector CPU latency</p>
              </div>
            </div>

            <div className="p-3 rounded-2xl bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 flex items-center gap-3">
              <Database className="w-5 h-5 text-emerald-500 shrink-0" />
              <div>
                <p className="font-extrabold text-slate-900 dark:text-white">&lt; 45 MB RAM</p>
                <p className="text-[11px] text-slate-400">Lightweight offline footprint</p>
              </div>
            </div>

            <div className="p-3 rounded-2xl bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 flex items-center gap-3">
              <ShieldCheck className="w-5 h-5 text-indigo-500 shrink-0" />
              <div>
                <p className="font-extrabold text-slate-900 dark:text-white">Zero Socket Calls</p>
                <p className="text-[11px] text-slate-400">Offline static analysis (runs without internet)</p>
              </div>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
