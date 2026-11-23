# UI Theme System: Midnight Navy + Gold + Teal Shield

## 1. Overview & Visual Identity
UPI Rakshak AI has been completely re-themed to the **"Midnight Navy + Gold + Teal Shield"** visual hierarchy. This theme blends high-security digital payment resilience with elegant typography, rich dark navy glassmorphic surfaces, golden command accents, and an active teal guardian shield.

Strict aesthetic and ethical rules are preserved:
- **Zero Detection Alterations**: No detector algorithms, weights, risk scoring math, or threshold values were altered.
- **Semantic Separation**: Brand colors (Gold `#D9A441` and Teal `#35D0C8`) are strictly separated from scam verdict indicators (`#34D399` Safe, `#FB923C` Suspicious, `#F43F5E` High Risk).
- **Multilingual Support**: All three official locales (English, Hindi, Telugu) render smoothly with dedicated Indic font stacks.
- **Contrast & Accessibility**: All interactive and reading elements satisfy or exceed WCAG AA standards (4.5:1 for normal text, 3.0:1 for large text and UI components).

---

## 2. Design Tokens & Palette Specifications

| Category | Token Name | Hex Code | RGB | Purpose & Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Background** | `--bg-deep` | `#050A18` | `rgb(5, 10, 24)` | Deepest page canvas; body background gradient start |
| **Background** | `--bg` | `#070E22` | `rgb(7, 14, 34)` | Standard canvas background; input field fills |
| **Background** | `--bg-raised` | `#0B1530` | `rgb(11, 21, 48)` | Sub-containers, nested boxes, timeline entries |
| **Surfaces** | `--surface` | `#0F1D3A` | `rgb(15, 29, 58)` | Glassmorphic cards (80-95% opacity), modals, panels |
| **Borders** | `--border` | `#1E3A5F` | `rgb(30, 58, 95)` | Subtle high-contrast card borders and dividers |
| **Brand Gold** | `--gold-300` | `#F3D58A` | `rgb(243, 213, 138)` | Light golden text accents and tags |
| **Brand Gold** | `--gold-400` | `#F5C96A` | `rgb(245, 201, 106)` | Primary button gradient stop, hero highlights |
| **Brand Gold** | `--gold-500` | `#D9A441` | `rgb(217, 164, 65)` | Primary brand CTA buttons, active card top rims |
| **Brand Gold** | `--gold-600` | `#A87B1E` | `rgb(168, 123, 30)` | Button active press border and dark gold shadow |
| **Teal Shield** | `--teal-400` | `#35D0C8` | `rgb(53, 208, 200)` | Guardian shield emblems, focus rings, active tabs |
| **Teal Shield** | `--teal-500` | `#1FB5AD` | `rgb(31, 181, 173)` | Interactive hover glow, secondary action links |
| **Text Primary** | `--text` | `#F5F1E6` | `rgb(245, 241, 230)` | Warm white high-contrast body & heading copy |
| **Text Muted** | `--text-muted`| `#A9B4CC` | `rgb(169, 180, 204)` | Secondary explanations, field labels, metadata |
| **Text Faint** | `--text-faint`| `#7C89A6` | `rgb(124, 137, 166)` | Subtle timestamps, subtotal counters |
| **Verdict Safe**| `--verdict-safe`| `#34D399` | `rgb(52, 211, 153)` | Verified legitimate communications |
| **Verdict Suspicious**| `--verdict-suspicious`| `#FB923C` | `rgb(251, 146, 60)` | Orange warning signal (distinct from gold) |
| **Verdict Danger**| `--verdict-danger`| `#F43F5E` | `rgb(244, 63, 94)` | Severe fraud, digital arrest, credential theft |

---

## 3. WCAG AA Contrast Measurement Audit

Relative luminance was computed using the standard formula `L = 0.2126*R + 0.7152*G + 0.0722*B` with gamma linearization, evaluating `(L1 + 0.05) / (L2 + 0.05)`.

| Foreground Element | Background Surface | Measured Contrast | WCAG AA Requirement | Status |
| :--- | :--- | :--- | :--- | :--- |
| Warm White Text (`#F5F1E6`) | Deep Navy Canvas (`#050A18`) | **17.50 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Warm White Text (`#F5F1E6`) | Surface Card (`#0F1D3A`) | **14.80 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Warm White Text (`#F5F1E6`) | Raised Box (`#0B1530`) | **15.98 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Muted Text (`#A9B4CC`) | Deep Navy Canvas (`#050A18`) | **9.49 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Muted Text (`#A9B4CC`) | Surface Card (`#0F1D3A`) | **8.02 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Dark Navy Button Text (`#050A18`) | Primary Gold Fill (`#F5C96A`) | **12.65 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Dark Navy Button Text (`#050A18`) | Brand Gold Fill (`#D9A441`) | **8.78 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Teal Shield Text (`#35D0C8`) | Deep Navy Canvas (`#050A18`) | **10.35 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Teal Shield Text (`#35D0C8`) | Surface Card (`#0F1D3A`) | **8.76 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| High Risk Pill (`#F43F5E`) | Deep Navy Canvas (`#050A18`) | **5.38 : 1** | &ge; 4.5:1 (Normal) | **PASS (AA)** |
| Safe Pill (`#34D399`) | Deep Navy Canvas (`#050A18`) | **10.28 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Suspicious Pill (`#FB923C`) | Deep Navy Canvas (`#050A18`) | **8.73 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Light Theme: Navy Text (`#0B1530`) | Ivory Background (`#FAF7F0`) | **16.86 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Light Theme: Navy Text (`#0B1530`) | Card White (`#FFFFFF`) | **18.04 : 1** | &ge; 4.5:1 (Normal) | **PASS (AAA)** |
| Light Theme: Dark Gold (`#8A6410`) | Card White (`#FFFFFF`) | **5.37 : 1** | &ge; 4.5:1 (Normal) | **PASS (AA)** |

---

## 4. Typography Hierarchy

1. **Display Headings (English Only)**:
   - Primary: `Playfair Display`, `Cormorant Garamond`, serif.
   - Used selectively for hero headlines, major section headers, and modal titles.
2. **Body and UI Copy**:
   - `Inter`, system-ui, -apple-system, sans-serif.
   - Clean, highly legible sans-serif for reading dense evidence lists and navigation items.
3. **Indic Multilingual Script Support**:
   - Hindi: `Noto Serif Devanagari`, `Noto Sans Devanagari`.
   - Telugu: `Noto Serif Telugu`, `Noto Sans Telugu`.
   - Line-height rules (`line-height: 1.6`) ensure that complex conjunct glyphs, matras, and diacritics are never clipped or crowded.
4. **Code, Hashes & Financial Identifiers**:
   - `JetBrains Mono`, `Fira Code`, monospace.
   - Used for UPI VPAs, phone numbers, transaction IDs, UTR numbers, and URLs.

---

## 5. Component Transformation Catalog

| Component / Page | Prior Style | Re-themed Style |
| :--- | :--- | :--- |
| **Navbar** | Flat dark slate bar with purple button | Transparent-to-solid navy (`#050A18`), gold active underline, gold 1930 CTA |
| **Analyzer Hero** | Generic sans-serif title with gray inputs | Display serif heading, gold keyword highlight, `#070E22` input with teal focus ring |
| **Score Gauge** | Blue speedometer arc | Midnight Navy track (`#101F3D`), semantic gradients, `#F5F1E6` score numerals |
| **Evidence List** | Slate card containers | Surface Navy (`#0F1D3A`) glassmorphic cards, semantic severity tags |
| **Guardian Avatar** | Purple robot avatar | 5 live states in Midnight Navy gradient, gold trim, and glowing teal core |
| **Assistant Chat** | Slate bubbles with blue send button | Navy-gold gradient bubbles, teal accent assistant responses, gold send action |
| **Emergency Playbook** | Monolithic red container | Golden Hour banner (`#F43F5E/15`), action tiles (`#0B1530`), bank hotline grid |
| **Admin Alarm Bell** | Cyan bell without audio feedback | Dual audio-visual alarm chime, live red notification badge, Midnight Navy drawer |
| **Dashboard Charts** | Default Recharts color palette | Brand gold category bars, semantic risk timeline, dark navy tooltips |
| **Share Card Generator** | 1200x630 slate canvas | High-res 1200x630 Midnight Navy canvas, gold borders, teal shield badge |
| **Favicon & Manifest** | Legacy Vite lightning bolt | Gold-rimmed navy circle with glowing teal vector shield SVG |

---

## 6. Light Theme Support
The application provides full support for light theme viewing while respecting system color scheme preferences:
- Background switches to Ivory `#FAF7F0` with crisp white card containers `#FFFFFF`.
- Typography shifts to dark navy `#0B1530` for extreme clarity.
- Brand gold and teal are calibrated darker (`#8A6410` for gold and `#0E8F89` for teal) to maintain high contrast compliance on white surfaces.
- Scam verdict hues (Green, Orange, Red) remain semantically intact with high-contrast text and border treatments.
