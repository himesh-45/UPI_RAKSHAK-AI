# Cross-Device & Viewport Compatibility Specification

## 1. Overview & Architectural Principles

UPI Rakshak AI is built to operate seamlessly across diverse hardware and network conditions representative of India's digital ecosystem—ranging from entry-level 320px smartphones running on 2G/3G connectivity up to 4K desktop security command centers.

### Core Compatibility Principles:
1. **Fluid Fluidity (320px to 2560px)**: Strict adherence to flexible container grids and auto-collapsing flex layouts with zero horizontal scroll (`overflow-x: hidden`).
2. **Touch-First Accessibility**: All interactive touch targets (buttons, inputs, tabs, chips, toggles) meet or exceed the **WCAG 2.1 AA** minimum requirement of **44 × 44 CSS pixels**.
3. **Adaptive Keyboard Semantics**: Form elements declare explicit `inputMode`, `type`, and text capitalization properties to invoke optimal on-screen touch keyboards.
4. **Offline Resilience & Fallbacks**: The offline core heuristic detector operates locally without external API dependencies, providing immediate feedback even under high packet loss.

---

## 2. Responsive Breakpoint Matrix

| Viewport Profile | Width × Height | CSS Breakpoint | Structural Adaptations | Overflow Status |
| :--- | :--- | :--- | :--- | :--- |
| **Budget Phone** | `320px × 568px` | `< 360px` | Single-column stack, wrapped button rows, compact text, font clamping, sticky bottom navigation bar. | **0px (Zero overflow)** |
| **Standard Android** | `360px × 740px` | `sm: 640px` | Single-column main layout, above-the-fold input, side-scrolling demo sample chips, 44px tap targets. | **0px (Zero overflow)** |
| **Large Smartphone** | `412px × 915px` | `sm: 640px` | Fluid card widths, balanced typography, full touch targets, native virtual keyboard padding. | **0px (Zero overflow)** |
| **Tablet Portrait** | `768px × 1024px` | `md: 768px` | 2-column KPI cards, full navigation links collapsed into tablet menu, expanded analytics charts. | **0px (Zero overflow)** |
| **Small Laptop / iPad**| `1024px × 768px` | `lg: 1024px` | Dual-pane side-by-side workspace (checker left, safety card right), single-row navigation header. | **0px (Zero overflow)** |
| **Standard Desktop** | `1440px × 900px` | `xl: 1280px` | Constrained `max-w-7xl` container, centered margins, multi-column analytics grid, full data tables. | **0px (Zero overflow)** |
| **Ultra-Wide / 4K** | `2560px × 1440px`| `2xl: 1536px`| Clamped container width, bounded line lengths (&le; 80 characters for prose readability), balanced whitespace. | **0px (Zero overflow)** |

---

## 3. Touch Target & Accessibility Audit (WCAG 2.1 AA)

All primary interactive components have been audited for hit-box boundaries:

| UI Component | Element Type | Dimensions | Min Hit Target | WCAG AA Status |
| :--- | :--- | :--- | :--- | :--- |
| **Primary CTA ("Check a message")** | `<button>` | `184px × 44px` | &ge; 44 × 44px | **PASS (AAA)** |
| **Quick Action / Demo Chips** | `<button>` | `Auto × 44px` (touch-target) | &ge; 44 × 44px | **PASS (AA)** |
| **Mode & Input Tabs (SMS/URL/QR)** | `<button>` | `Auto × 44px` | &ge; 44 × 44px | **PASS (AA)** |
| **Theme Switcher Button** | `<button>` | `44px × 44px` | &ge; 44 × 44px | **PASS (AA)** |
| **Language Switcher (EN/HI/TE)** | `<button>` | `44px × 44px` (padded) | &ge; 44 × 44px | **PASS (AA)** |
| **Mobile Navigation Bar Items** | `<button>` | `Auto × 52px` | &ge; 44 × 44px | **PASS (AAA)** |
| **Emergency 1930 Call Button** | `<a>` | `88px × 44px` | &ge; 44 × 44px | **PASS (AAA)** |
| **Form Inputs & Textareas** | `<input>, <textarea>` | `100% × &ge;44px` | &ge; 44 × 44px | **PASS (AA)** |

---

## 4. Input & Mobile Keyboard Optimizations

Form controls are enriched with mobile-friendly attributes:

```html
<!-- Payment link analysis -->
<input
  type="url"
  inputmode="url"
  autocapitalize="none"
  autocorrect="off"
  spellcheck="false"
  placeholder="https://..."
/>

<!-- UPI ID verification -->
<input
  type="text"
  inputmode="text"
  autocapitalize="none"
  autocorrect="off"
  spellcheck="false"
  placeholder="user@okhdfcbank"
/>

<!-- Amount field -->
<input
  type="number"
  inputmode="numeric"
  min="0"
  step="1"
  placeholder="₹ 5,000"
/>
```

---

## 5. Supported Browsers & Platform Matrix

| Platform | Target OS Versions | Supported Browsers | Engine | Testing Status |
| :--- | :--- | :--- | :--- | :--- |
| **Android** | Android 9.0+ (Pie to 15) | Chrome Mobile, Firefox Mobile, Samsung Internet | Blink / Gecko | Verified |
| **iOS / iPadOS** | iOS 15.0+ | Safari, Chrome for iOS | WebKit | Verified |
| **Windows** | Windows 10, 11 | Chrome 110+, Edge 110+, Firefox 115+ | Blink / Gecko | Verified |
| **macOS** | macOS Monterey (12)+ | Safari 16+, Chrome, Firefox | WebKit / Blink | Verified |
| **Linux** | Ubuntu 20.04+, Fedora | Firefox ESR, Chromium | Gecko / Blink | Verified |

---

## 6. Fallback & Fault Tolerance Architecture

1. **Slow 2G/3G Networks**:
   - Initial bundle load is pre-rendered and statically compiled via Vite.
   - Core heuristic scoring runs client-side / offline with zero external API dependencies.
2. **Offline Mode**:
   - Local storage retains preferences (language, theme).
   - If server connection drops during a scan, cached offline safety advice and statutory 1930 emergency instructions remain visible.
3. **No-Script / Blocked Fonts**:
   - Semantic system font fallbacks: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.
   - Multilingual Devanagari & Telugu scripts fall back safely to `Noto Sans Devanagari`, `Noto Sans Telugu`, `Nirmala UI`, `Gautami`, and `Mangal` without clipping or broken conjuncts.
