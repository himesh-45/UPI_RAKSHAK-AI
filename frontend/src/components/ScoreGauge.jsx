import React from 'react';
import { ShieldCheck, AlertTriangle, ShieldAlert } from 'lucide-react';

export default function ScoreGauge({ score = 0, verdict = 'SAFE' }) {
  // Clamp score
  const safeScore = Math.max(0, Math.min(100, score));

  // Determine colors and verdict style
  let strokeColor = '#10b981'; // safe
  let bgColor = 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800';
  let badgeText = 'SAFE (NO STRONG THREATS)';
  let Icon = ShieldCheck;

  if (safeScore >= 70) {
    strokeColor = '#ef4444'; // danger
    bgColor = 'bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-800';
    badgeText = 'HIGH RISK (CONFIRMED SCAM)';
    Icon = ShieldAlert;
  } else if (safeScore >= 35) {
    strokeColor = '#f59e0b'; // warning
    bgColor = 'bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800';
    badgeText = 'SUSPICIOUS (PROCEED WITH CAUTION)';
    Icon = AlertTriangle;
  }

  // SVG circle calculation
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (safeScore / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 128 128">
          {/* Track circle */}
          <circle
            cx="64"
            cy="64"
            r={radius}
            className="stroke-slate-100 dark:stroke-slate-800"
            strokeWidth="10"
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx="64"
            cy="64"
            r={radius}
            stroke={strokeColor}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            style={{ transition: 'stroke-dashoffset 1s ease-in-out' }}
          />
        </svg>

        {/* Center Score & Icon */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">
            {safeScore}
          </span>
          <span className="text-xs uppercase font-semibold text-slate-500 dark:text-slate-400">
            Risk Score
          </span>
        </div>
      </div>

      {/* Verdict Pill */}
      <div className={`mt-4 px-4 py-1.5 rounded-full border text-xs font-bold tracking-wider flex items-center gap-1.5 uppercase ${bgColor}`}>
        <Icon className="w-4 h-4" />
        <span>{verdict || badgeText}</span>
      </div>
    </div>
  );
}
