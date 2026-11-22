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

  // Cyber theme glowing palette & badges
  let gradStart = '#06b6d4';
  let gradEnd = '#10b981';
  let pillStyle = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 shadow-[0_0_12px_rgba(16,185,129,0.3)]';
  let badgeText = 'Low Risk';
  let Icon = ShieldCheck;

  if (safeScore >= 70) {
    gradStart = '#f59e0b';
    gradEnd = '#ef4444';
    pillStyle = 'bg-rose-500/20 text-rose-300 border-rose-500/50 shadow-[0_0_15px_rgba(239,68,68,0.4)]';
    badgeText = 'High Risk';
    Icon = ShieldAlert;
  } else if (safeScore >= 35) {
    gradStart = '#facc15';
    gradEnd = '#f59e0b';
    pillStyle = 'bg-amber-500/20 text-amber-300 border-amber-500/50 shadow-[0_0_12px_rgba(245,158,11,0.35)]';
    badgeText = 'Suspicious';
    Icon = AlertTriangle;
  }

  // Semi-circle Speedometer calculation (Radius 58, length ~ 182.2)
  const arcLength = 182.2;
  const strokeOffset = arcLength - (safeScore / 100) * arcLength;

  return (
    <div className="flex flex-col items-center justify-center p-5 bg-[#0a0f26]/90 rounded-3xl border border-cyan-500/20 shadow-[0_0_20px_rgba(6,182,212,0.1)] shrink-0">
      <div className="relative w-44 h-28 flex items-center justify-center">
        <svg className="w-full h-full overflow-visible" viewBox="0 0 160 100">
          <defs>
            <linearGradient id="cyberGaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor={gradStart} />
              <stop offset="100%" stopColor={gradEnd} />
            </linearGradient>
            <filter id="gaugeGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Background Track Arc */}
          <path
            d="M 22 88 A 58 58 0 0 1 138 88"
            fill="none"
            stroke="#161f3d"
            strokeWidth="11"
            strokeLinecap="round"
          />

          {/* Animated Glowing Progress Arc */}
          <path
            d="M 22 88 A 58 58 0 0 1 138 88"
            fill="none"
            stroke="url(#cyberGaugeGradient)"
            strokeWidth="11"
            strokeLinecap="round"
            strokeDasharray={arcLength}
            strokeDashoffset={strokeOffset}
            filter="url(#gaugeGlow)"
            style={{ transition: 'stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1)' }}
          />
        </svg>

        {/* Center Score with /100 */}
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-1 text-center">
          <div className="flex items-baseline gap-1">
            <span className="text-4xl font-black tracking-tight text-white font-mono drop-shadow-[0_0_10px_rgba(255,255,255,0.4)]">
              {displayScore}
            </span>
            <span className="text-sm font-semibold text-slate-400">/100</span>
          </div>
        </div>
      </div>

      {/* High-Tech Risk Pill Badge */}
      <div className={`mt-2 px-4 py-1 rounded-full border text-xs font-black tracking-wider flex items-center gap-1.5 uppercase transition ${pillStyle}`}>
        <Icon className="w-3.5 h-3.5 shrink-0" />
        <span>{badgeText}</span>
      </div>
    </div>
  );
}
