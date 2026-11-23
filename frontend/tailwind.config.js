/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Midnight Navy + Gold + Teal Design System (Theme-Adaptive Tokens)
        navy: {
          deep: 'rgb(var(--bg-deep-rgb) / <alpha-value>)',
          DEFAULT: 'rgb(var(--bg-rgb) / <alpha-value>)',
          raised: 'rgb(var(--bg-raised-rgb) / <alpha-value>)',
          surface: 'rgb(var(--surface-rgb) / <alpha-value>)',
          surfaceRaised: 'rgb(var(--surface-raised-rgb) / <alpha-value>)',
          surfaceHover: 'rgb(var(--surface-hover-rgb) / <alpha-value>)',
          border: 'rgb(var(--border-rgb) / <alpha-value>)',
        },
        surface: {
          DEFAULT: 'rgb(var(--surface-rgb) / <alpha-value>)',
          raised: 'rgb(var(--surface-raised-rgb) / <alpha-value>)',
          hover: 'rgb(var(--surface-hover-rgb) / <alpha-value>)',
          border: 'rgb(var(--border-rgb) / <alpha-value>)',
        },
        border: {
          DEFAULT: 'rgb(var(--border-rgb) / <alpha-value>)',
          hover: 'rgb(var(--border-hover-rgb) / <alpha-value>)',
        },
        gold: {
          300: 'rgb(var(--gold-300-rgb) / <alpha-value>)',
          400: 'rgb(var(--gold-400-rgb) / <alpha-value>)',
          500: 'rgb(var(--gold-500-rgb) / <alpha-value>)',
          600: 'rgb(var(--gold-600-rgb) / <alpha-value>)',
          DEFAULT: 'rgb(var(--gold-500-rgb) / <alpha-value>)',
        },
        teal: {
          300: 'rgb(var(--teal-300-rgb) / <alpha-value>)',
          400: 'rgb(var(--teal-400-rgb) / <alpha-value>)',
          500: 'rgb(var(--teal-500-rgb) / <alpha-value>)',
          600: 'rgb(var(--teal-600-rgb) / <alpha-value>)',
          DEFAULT: 'rgb(var(--teal-400-rgb) / <alpha-value>)',
        },
        ink: {
          DEFAULT: 'rgb(var(--text-rgb) / <alpha-value>)',
          muted: 'rgb(var(--text-muted-rgb) / <alpha-value>)',
          faint: 'rgb(var(--text-faint-rgb) / <alpha-value>)',
        },
        // Strict Semantic Verdict Colors (used ONLY for scam verdicts)
        verdict: {
          safe: 'rgb(var(--verdict-safe-rgb) / <alpha-value>)',
          suspicious: 'rgb(var(--verdict-suspicious-rgb) / <alpha-value>)',
          danger: 'rgb(var(--verdict-danger-rgb) / <alpha-value>)',
        },
        // Backward-compatible semantic tokens mapped to dynamic theme palette
        cyber: {
          bg: 'rgb(var(--bg-rgb) / <alpha-value>)',
          surface: 'rgb(var(--surface-rgb) / <alpha-value>)',
          card: 'rgb(var(--surface-rgb) / <alpha-value>)',
          cardHover: 'rgb(var(--surface-raised-rgb) / <alpha-value>)',
          border: 'rgb(var(--border-rgb) / <alpha-value>)',
          borderGlow: 'rgb(var(--teal-400-rgb) / 0.45)',
          cyan: 'rgb(var(--teal-400-rgb) / <alpha-value>)',
          teal: 'rgb(var(--teal-500-rgb) / <alpha-value>)',
          gold: 'rgb(var(--gold-500-rgb) / <alpha-value>)',
          blue: 'rgb(var(--teal-400-rgb) / <alpha-value>)',
          purple: 'rgb(var(--gold-400-rgb) / <alpha-value>)',
          pink: 'rgb(var(--verdict-danger-rgb) / <alpha-value>)',
          red: 'rgb(var(--verdict-danger-rgb) / <alpha-value>)',
          amber: 'rgb(var(--verdict-suspicious-rgb) / <alpha-value>)',
          green: 'rgb(var(--verdict-safe-rgb) / <alpha-value>)',
          muted: 'rgb(var(--text-muted-rgb) / <alpha-value>)'
        },
        safe: {
          light: 'rgba(52, 211, 153, 0.12)',
          DEFAULT: '#34D399',
          dark: '#059669',
        },
        warning: {
          light: 'rgba(251, 146, 60, 0.12)',
          DEFAULT: '#FB923C',
          dark: '#EA580C',
        },
        danger: {
          light: 'rgba(244, 63, 94, 0.12)',
          DEFAULT: '#F43F5E',
          dark: '#E11D48',
        },
        brand: {
          50: '#FAF7F0',
          100: '#F3D58A',
          500: '#D9A441',
          600: '#F5C96A',
          700: '#A87B1E',
          900: '#0B1530',
        }
      },
      boxShadow: {
        'glass-card': '0 8px 32px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(30, 58, 95, 0.5)',
        'glass-hover': '0 12px 36px rgba(0, 0, 0, 0.6), 0 0 20px rgba(53, 208, 200, 0.25), 0 0 0 1px rgba(53, 208, 200, 0.4)',
        'glow-teal': '0 0 20px rgba(53, 208, 200, 0.35)',
        'glow-gold': '0 0 20px rgba(217, 164, 65, 0.35)',
        'glow-red': '0 0 20px rgba(244, 63, 94, 0.35)',
        'glow-green': '0 0 20px rgba(52, 211, 153, 0.35)',
        'shield-halo': '0 0 45px rgba(53, 208, 200, 0.3), inset 0 0 25px rgba(217, 164, 65, 0.2)',
        'cyber-card': '0 8px 32px rgba(5, 10, 24, 0.55), 0 0 0 1px #1E3A5F',
      },
      fontFamily: {
        serif: ['Playfair Display', 'Cormorant Garamond', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        devanagari: ['Noto Sans Devanagari', 'Mangal', 'sans-serif'],
        devanagariSerif: ['Noto Serif Devanagari', 'serif'],
        telugu: ['Noto Sans Telugu', 'Gautami', 'sans-serif'],
        teluguSerif: ['Noto Serif Telugu', 'serif'],
      },
      keyframes: {
        wiggle: {
          '0%, 100%': { transform: 'rotate(-12deg)' },
          '50%': { transform: 'rotate(12deg)' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(200%)' },
        },
        pulseTeal: {
          '0%, 100%': { opacity: '0.4', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.04)' },
        }
      },
      animation: {
        wiggle: 'wiggle 0.25s ease-in-out infinite',
        shimmer: 'shimmer 2.2s infinite',
        pulseTeal: 'pulseTeal 3s ease-in-out infinite',
      }
    },
  },
  plugins: [],
}
