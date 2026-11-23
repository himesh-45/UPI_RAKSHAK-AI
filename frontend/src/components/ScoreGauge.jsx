import React, { useEffect, useState } from 'react';
import { ShieldCheck, AlertTriangle, ShieldAlert, Clock } from 'lucide-react';

export default function ScoreGauge({ score = null, verdict = null }) {
  const isIdle = score === null || score === undefined || verdict === 'Awaiting Input' || verdict === null || verdict === '';
  const safeScore = isIdle ? 0 : Math.max(0, Math.min(100, Math.round(score)));
  const [displayScore, setDisplayScore] = useState(0);

  // Smooth animated count-up only when active
  useEffect(() => {
    if (isIdle) {
      setDisplayScore(0);
      return;
    }
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
  }, [safeScore, isIdle]);

  // Semi-circle Speedometer calculation (Radius 58, length ~ 182.2)
  const arcLength = 182.2;
  const strokeOffset = isIdle ? arcLength : arcLength - (safeScore / 100) * arcLength;

  // Semantic verdict styles
  let gradStart = 'var(--teal-400)';
  let gradEnd = 'var(--verdict-safe)';
  let pillStyle = 'bg-verdict-safe/15 text-verdict-safe border-verdict-safe/40 shadow-xs';
  let badgeText = 'Low Risk';
  let Icon = ShieldCheck;

  if (isIdle) {
    gradStart = 'var(--border)';
    gradEnd = 'var(--border)';
    pillStyle = 'bg-navy text-ink-muted border-border';
    badgeText = 'Waiting for a message';
    Icon = Clock;
  } else if (safeScore >= 70) {
    gradStart = 'var(--verdict-suspicious)';
    gradEnd = 'var(--verdict-danger)';
    pillStyle = 'bg-verdict-danger/15 text-verdict-danger border-verdict-danger/40 shadow-xs';
    badgeText = 'High Risk';
    Icon = ShieldAlert;
  } else if (safeScore >= 35) {
    gradStart = 'var(--gold-400)';
    gradEnd = 'var(--verdict-suspicious)';
    pillStyle = 'bg-verdict-suspicious/15 text-verdict-suspicious border-verdict-suspicious/40 shadow-xs';
    badgeText = 'Suspicious';
    Icon = AlertTriangle;
  }

  return (
    <div className="flex flex-col items-center justify-center p-5 bg-navy-surface rounded-3xl border border-border shadow-[0_4px_20px_rgba(5,10,24,0.15)] shrink-0 transition-colors">
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
            stroke="currentColor"
            className="text-border/60"
            strokeWidth="11"
            strokeLinecap="round"
          />

          {/* Animated Glowing Progress Arc */}
          {!isIdle && (
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
          )}
        </svg>

        {/* Center Score with /100 */}
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-1 text-center">
          <div className="flex items-baseline gap-1">
            <span className="text-4xl font-black tracking-tight text-ink font-mono">
              {isIdle ? '--' : displayScore}
            </span>
            <span className="text-sm font-semibold text-ink-muted">/100</span>
          </div>
        </div>
      </div>

      {/* Risk Pill Badge */}
      <div className={`mt-2 px-4 py-1 rounded-full border text-xs font-bold tracking-wider flex items-center gap-1.5 uppercase transition ${pillStyle}`}>
        <Icon className="w-3.5 h-3.5 shrink-0" />
        <span>{badgeText}</span>
      </div>
    </div>
  );
}
