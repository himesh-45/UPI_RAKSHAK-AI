# UPI Rakshak Assistant — UI & Visual Design Specifications

This directory contains visual reference artifacts, a11y specifications, and responsive screenshots for the Rakshak Assistant digital guardian interface.

## 1. Responsive Viewports Verified
- **Mobile First (360px x 740px)**: Pinned safe-area composer (`env(safe-area-inset-bottom)`), zero horizontal overflow, swipeable quick-reply chips, min 44px touch targets.
- **Tablet / Responsive (768px x 1024px)**: Adaptive 2-column action grids, collapsible bank helpline accordions.
- **Desktop (1440px x 900px)**: Full cyber glassmorphism layout, multi-card security overview.

## 2. Accessibility & A11y Standards
- **WCAG AA Compliance**: High-contrast ratios (>= 4.5:1 text, >= 3:1 controls).
- **ARIA Live Regions**: `aria-live="polite"` on conversational log container for non-intrusive screen reader announcements; `aria-live="assertive"` on threat verdict alert cards.
- **Keyboard Shortcuts**:
  - `Ctrl + K` / `Cmd + K`: Direct focus to conversational composer.
  - `Escape`: Instantly dismiss active modals (About Rakshak, Learn Scams, Pre-fill 1930).
  - `Alt + 1`: English language mode.
  - `Alt + 2`: Hindi language mode (हिंदी).
  - `Alt + 3`: Telugu language mode (తెలుగు).

## 3. High-Contrast Elder Mode
- Large-font mode (18px base) with high-contrast amber/black styling.
- 3 simplified primary actions: `[Check a Message]`, `[Call 1930]`, `[Is This Safe?]`.
- Automated Web Speech API speech synthesis reading out threat verdicts and statutory actions in native accents (`hi-IN`, `te-IN`, `en-IN`).
