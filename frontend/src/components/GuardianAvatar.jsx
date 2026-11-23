import React from 'react';

/**
 * GuardianAvatar ("Rakshak")
 * Pure SVG cyber guardian avatar with 5 reactive states:
 * - idle: calm circuit shield with gentle cyan glow
 * - listening: pulsing cyan outer ring with audio waveform bars
 * - scanning: rotating radar beam and glowing scanner lines
 * - safe: verified green shield with checkmark lock (detector verified safe)
 * - alert: pulse amber/red shield with warning beacon (detector flagged threat)
 */
export default function GuardianAvatar({
  state = 'idle',
  size = 48,
  className = '',
  onClick = null,
  showLabel = false,
  label = 'Rakshak'
}) {
  const isInteractive = typeof onClick === 'function';

  // State-specific styling & colors
  const stateConfig = {
    idle: {
      primary: '#00e5ff',
      secondary: '#06b6d4',
      glow: 'rgba(0, 229, 255, 0.35)',
      ringColor: '#0891b2',
      badgeColor: '#00e5ff',
      badgeText: 'ONLINE'
    },
    listening: {
      primary: '#38bdf8',
      secondary: '#0284c7',
      glow: 'rgba(56, 189, 248, 0.55)',
      ringColor: '#38bdf8',
      badgeColor: '#38bdf8',
      badgeText: 'LISTENING'
    },
    scanning: {
      primary: '#22d3ee',
      secondary: '#0891b2',
      glow: 'rgba(34, 211, 238, 0.65)',
      ringColor: '#06b6d4',
      badgeColor: '#22d3ee',
      badgeText: 'SCANNING'
    },
    safe: {
      primary: '#10b981',
      secondary: '#059669',
      glow: 'rgba(16, 185, 129, 0.45)',
      ringColor: '#10b981',
      badgeColor: '#10b981',
      badgeText: 'VERIFIED SAFE'
    },
    alert: {
      primary: '#ef4444',
      secondary: '#dc2626',
      glow: 'rgba(239, 68, 68, 0.55)',
      ringColor: '#ef4444',
      badgeColor: '#ef4444',
      badgeText: 'THREAT ALERT'
    }
  };

  const config = stateConfig[state] || stateConfig.idle;

  return (
    <div
      className={`inline-flex flex-col items-center select-none ${isInteractive ? 'cursor-pointer group' : ''} ${className}`}
      onClick={onClick}
      role={isInteractive ? 'button' : 'img'}
      aria-label={`Rakshak Guardian Avatar (${state} state)`}
      tabIndex={isInteractive ? 0 : -1}
      onKeyDown={(e) => {
        if (isInteractive && (e.key === 'Enter' || e.key === ' ')) {
          e.preventDefault();
          onClick();
        }
      }}
    >
      <div
        className="relative flex items-center justify-center transition-all duration-300"
        style={{
          width: `${size}px`,
          height: `${size}px`,
          filter: `drop-shadow(0 0 ${Math.max(4, size * 0.15)}px ${config.glow})`
        }}
      >
        <svg
          viewBox="0 0 100 100"
          className="w-full h-full overflow-visible"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Definitions for Gradients and Filters */}
          <defs>
            <linearGradient id={`shieldGrad-${state}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#0c162d" />
              <stop offset="50%" stopColor="#0a0f1d" />
              <stop offset="100%" stopColor="#050811" />
            </linearGradient>

            <linearGradient id={`accentGrad-${state}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={config.primary} />
              <stop offset="100%" stopColor={config.secondary} />
            </linearGradient>

            {/* Rotating scanner beam */}
            {state === 'scanning' && (
              <linearGradient id="scanBeam" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="rgba(34, 211, 238, 0)" />
                <stop offset="100%" stopColor="rgba(34, 211, 238, 0.45)" />
              </linearGradient>
            )}
          </defs>

          {/* Outer Breathing/Scanning Halo Ring */}
          <circle
            cx="50"
            cy="50"
            r="46"
            stroke={config.ringColor}
            strokeWidth={size >= 48 ? '1.5' : '1'}
            strokeDasharray={state === 'listening' ? '4 3' : (state === 'scanning' ? '8 4' : 'none')}
            className={`transition-all duration-500 opacity-60 ${
              state === 'listening' ? 'animate-pulse' : (state === 'scanning' ? 'animate-spin' : '')
            }`}
            style={{ transformOrigin: '50% 50%' }}
          />

          {/* Hexagonal Guardian Chassis Base */}
          <polygon
            points="50,6 88,28 88,72 50,94 12,72 12,28"
            fill={`url(#shieldGrad-${state})`}
            stroke={`url(#accentGrad-${state})`}
            strokeWidth={size >= 48 ? '2' : '1.5'}
            className="transition-colors duration-300"
          />

          {/* Circuit / Tech Traces */}
          {size >= 32 && (
            <g stroke={config.primary} strokeWidth="1" opacity="0.35" strokeLinecap="round">
              <line x1="28" y1="24" x2="40" y2="24" />
              <line x1="40" y1="24" x2="48" y2="32" />
              <line x1="72" y1="24" x2="60" y2="24" />
              <line x1="60" y1="24" x2="52" y2="32" />
              <line x1="24" y1="50" x2="34" y2="50" />
              <line x1="76" y1="50" x2="66" y2="50" />
              <circle cx="28" cy="24" r="1.5" fill={config.primary} />
              <circle cx="72" cy="24" r="1.5" fill={config.primary} />
            </g>
          )}

          {/* Center Dynamic Shield Emblem */}
          <path
            d="M50 22 C64 22 72 26 72 40 C72 62 50 78 50 78 C50 78 28 62 28 40 C28 26 36 22 50 22 Z"
            fill="rgba(6, 182, 212, 0.08)"
            stroke={config.primary}
            strokeWidth={size >= 48 ? '2' : '1.5'}
            className="transition-all duration-300"
          />

          {/* STATE-SPECIFIC INTERIOR GRAPHICS */}

          {/* 1. IDLE: Calm Central Core Eye & Keyhole Circuit */}
          {state === 'idle' && (
            <g>
              <circle cx="50" cy="44" r="7" fill={config.primary} opacity="0.8" />
              <circle cx="50" cy="44" r="3.5" fill="#0a0f1d" />
              <path d="M46 54 L54 54 L56 64 L44 64 Z" fill={config.primary} opacity="0.8" />
            </g>
          )}

          {/* 2. LISTENING: Dynamic Acoustic Waveform */}
          {state === 'listening' && (
            <g fill={config.primary}>
              <rect x="36" y="42" width="3.5" height="12" rx="1.5" className="animate-pulse" style={{ animationDelay: '0.1s' }} />
              <rect x="43" y="36" width="3.5" height="24" rx="1.5" className="animate-pulse" style={{ animationDelay: '0.3s' }} />
              <rect x="50" y="32" width="3.5" height="32" rx="1.5" className="animate-pulse" style={{ animationDelay: '0.0s' }} />
              <rect x="57" y="36" width="3.5" height="24" rx="1.5" className="animate-pulse" style={{ animationDelay: '0.4s' }} />
              <rect x="64" y="42" width="3.5" height="12" rx="1.5" className="animate-pulse" style={{ animationDelay: '0.2s' }} />
            </g>
          )}

          {/* 3. SCANNING: Active Radar Sweep Line */}
          {state === 'scanning' && (
            <g>
              <line x1="50" y1="50" x2="72" y2="30" stroke={config.primary} strokeWidth="2.5" strokeLinecap="round" />
              <circle cx="50" cy="50" r="16" stroke={config.primary} strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />
              <circle cx="50" cy="50" r="5" fill={config.primary} />
            </g>
          )}

          {/* 4. SAFE: Verified Checkmark Lock */}
          {state === 'safe' && (
            <g>
              <circle cx="50" cy="48" r="14" fill="rgba(16, 185, 129, 0.2)" />
              <path
                d="M42 48 L48 54 L60 40"
                stroke="#10b981"
                strokeWidth="3.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </g>
          )}

          {/* 5. ALERT: Red Warning Shield Hazard Triangle */}
          {state === 'alert' && (
            <g className="animate-pulse">
              <path
                d="M50 36 L62 58 L38 58 Z"
                fill="rgba(239, 68, 68, 0.25)"
                stroke="#ef4444"
                strokeWidth="2"
                strokeLinejoin="round"
              />
              <line x1="50" y1="43" x2="50" y2="50" stroke="#ef4444" strokeWidth="2.5" strokeLinecap="round" />
              <circle cx="50" cy="54" r="1.5" fill="#ef4444" />
            </g>
          )}
        </svg>

        {/* Small Active Pulse Pip (Corner Indicator) */}
        {size >= 40 && (
          <span
            className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full ring-2 ring-slate-950"
            style={{ backgroundColor: config.badgeColor }}
          />
        )}
      </div>

      {showLabel && (
        <span className="mt-1 text-xs font-mono tracking-wider font-semibold text-slate-300">
          {label}
        </span>
      )}
    </div>
  );
}
