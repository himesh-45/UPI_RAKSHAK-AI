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
        cyber: {
          bg: '#060919',
          surface: '#0a0f26',
          card: '#0c122b',
          cardHover: '#10183b',
          border: 'rgba(6, 182, 212, 0.22)',
          borderGlow: 'rgba(6, 182, 212, 0.45)',
          cyan: '#00f2fe',
          teal: '#06b6d4',
          blue: '#0ea5e9',
          purple: '#a855f7',
          pink: '#ec4899',
          red: '#ef4444',
          amber: '#f59e0b',
          green: '#10b981',
          muted: '#94a3b8'
        },
        safe: {
          light: '#ecfdf5',
          DEFAULT: '#10b981',
          dark: '#047857',
        },
        warning: {
          light: '#fffbeb',
          DEFAULT: '#f59e0b',
          dark: '#b45309',
        },
        danger: {
          light: '#fef2f2',
          DEFAULT: '#ef4444',
          dark: '#b91c1c',
        },
        brand: {
          50: '#eef2ff',
          100: '#e0e7ff',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          900: '#312e81',
        }
      },
      boxShadow: {
        'neon-cyan': '0 0 20px rgba(6, 182, 212, 0.35)',
        'neon-blue': '0 0 25px rgba(14, 165, 233, 0.35)',
        'neon-red': '0 0 20px rgba(239, 68, 68, 0.35)',
        'neon-purple': '0 0 20px rgba(168, 85, 247, 0.35)',
        'neon-green': '0 0 20px rgba(16, 185, 129, 0.35)',
        'cyber-card': '0 8px 32px rgba(0, 0, 0, 0.45), 0 0 20px rgba(6, 182, 212, 0.08)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
