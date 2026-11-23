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
        // Midnight Navy + Gold + Teal Design System
        navy: {
          deep: '#050A18',
          DEFAULT: '#070E22',
          raised: '#0B1530',
          surface: '#0F1D3A',
          surfaceRaised: '#14254B',
          surfaceHover: '#192D5C',
          border: '#1E3A5F',
        },
        gold: {
          300: '#F3D58A',
          400: '#F5C96A',
          500: '#D9A441',
          600: '#A87B1E',
          DEFAULT: '#D9A441',
        },
        teal: {
          300: '#5EEAD4',
          400: '#35D0C8',
          500: '#1FB5AD',
          600: '#0E8F89',
          DEFAULT: '#35D0C8',
        },
        ink: {
          DEFAULT: '#F5F1E6',
          muted: '#A9B4CC',
          faint: '#7C89A6',
        },
        // Strict Semantic Verdict Colors (used ONLY for scam verdicts)
        verdict: {
          safe: '#34D399',
          suspicious: '#FB923C',
          danger: '#F43F5E',
        },
        // Backward-compatible semantic tokens mapped to new Midnight Navy + Teal + Gold palette
        cyber: {
          bg: '#070E22',
          surface: '#0F1D3A',
          card: '#0F1D3A',
          cardHover: '#14254B',
          border: '#1E3A5F',
          borderGlow: 'rgba(53, 208, 200, 0.45)',
          cyan: '#35D0C8',
          teal: '#1FB5AD',
          gold: '#D9A441',
          blue: '#35D0C8',
          purple: '#F5C96A',
          pink: '#F43F5E',
          red: '#F43F5E',
          amber: '#FB923C',
          green: '#34D399',
          muted: '#A9B4CC'
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
