import React, { useEffect, useState } from 'react';
import { ShieldCheck, AlertTriangle, ShieldAlert } from 'lucide-react';

export default function ScoreGauge({ score = 0, verdict = 'SAFE' }) {
  const safeScore = Math.max(0, Math.min(100, Math.round(score)));
  const [displayScore, setDisplayScore] = useState(0);

  // Smooth animated count-up
  useEffect(() => {
    let start = 0;
    const duration = 800; // ms
    const startTime = performance.now();

    const animate = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const currentVal = Math.round(eased * safeScore);
      setDisplayScore(currentVal);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }, [safeScore]);

  // WCAG AA Compliant color palette (minimum 4.5:1 contrast against dark background)
  let strokeColor = '#10b981'; // emerald-500
  let bgColor = 'bg-emerald-950/60 text-emerald-300 border-emerald-500/40';
  let badgeText = 'SAFE (NO STRONG THREATS)';
  let Icon = ShieldCheck;

  if (safeScore >= 70) {
    strokeColor = '#f43f5e'; // rose-500
    bgColor = 'bg-rose-950/60 text-rose-300 border-rose-500/40';
    badgeText = 'HIGH RISK (CONFIRMED SCAM)';
    Icon = ShieldAlert;
  } else if (safeScore >= 35) {
    strokeColor = '#f59e0b'; // amber-500
    bgColor = 'bg-amber-950/60 text-amber-300 border-amber-500/40';
    badgeText = 'SUSPICIOUS (PROCEED WITH CAUTION)';
    Icon = AlertTriangle;
  }

  // SVG circle calculation
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (safeScore / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-slate-900/90 rounded-2xl border border-slate-800 shadow-xl shrink-0">
      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 128 128">
          {/* Background track circle */}
          <circle
            cx="64"
            cy="64"
            r={radius}
            className="stroke-slate-800"
            strokeWidth="10"
            fill="transparent"
          />
          {/* Animated progress circle */}
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
            style={{ transition: 'stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1)' }}
          />
        </svg>

        {/* Center Score & Label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-black tracking-tight text-white font-mono">
            {displayScore}
          </span>
          <span className="text-[11px] uppercase font-bold tracking-wider text-slate-400 mt-0.5">
            Risk Score
          </span>
        </div>
      </div>

      {/* Verdict Pill (WCAG AA Compliant contrast) */}
      <div className={`mt-4 px-4 py-1.5 rounded-full border text-xs font-black tracking-wider flex items-center gap-1.5 uppercase shadow-sm ${bgColor}`}>
        <Icon className="w-4 h-4 shrink-0" />
        <span>{verdict || badgeText}</span>
      </div>
    </div>
  );
}
