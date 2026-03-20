---
name: premium-frontend
description: Use when building any web UI — components, pages, dashboards, or full applications — and world-class design quality is the goal. Use when avoiding generic AI aesthetics, enforcing technical precision, applying industry-appropriate visual direction, and passing a rigorous pre-delivery quality gate.
---

# Premium Frontend

## Overview

**Five elite frameworks, one skill.** Layers precise technical standards onto bold aesthetic direction. Every UI must be both unforgettable and production-grade.

**Builds on** the official `frontend-design` skill for aesthetic direction. This skill adds:
- Concrete technical standards (4pt grid, OKLCH, 8 interactive states)
- Anti-pattern hard stops (Uncodixfy's "Normal UI" standards)
- Pre-delivery quality gates (accessibility, motion, responsive)
- Industry context mapping

## Design Brief Protocol

**Before writing any code**, run this brief — it replaces 2–3 iteration rounds.

Ask the user these questions (all at once, not one by one):

> 1. **Visual reference** — Name 2–3 apps, websites, or brands whose design you love. (e.g. "Linear, Stripe, the Apple website")
> 2. **Feeling** — What should the UI make the user feel? Pick words: *focused / calm / energetic / bold / trustworthy / playful / serious / luxurious / minimal / expressive*
> 3. **Color instinct** — Any colors you love, hate, or already use in this project?
> 4. **Density** — Dense with information (like Notion, GitHub) or spacious and breathable (like Linear, Loom)?
> 5. **Context** — Who uses this and when? (e.g. "a developer at a desktop all day" vs "a customer on mobile quickly")

**Translate answers into design decisions before coding:**

| User says | Design decision |
|---|---|
| "Like Linear" | Near-black bg, tight spacing, monospace accents, minimal color |
| "Like Airbnb" | Warm neutrals, generous white space, rounded cards, photography-forward |
| "Like Stripe" | Deep navy + electric purple, dense but structured, heavy typography |
| "Calm and focused" | Low saturation, generous spacing, restrained animation, high contrast text |
| "Bold and energetic" | High contrast, strong accent, faster transitions, asymmetric layout |
| "Trustworthy" | Conservative palette, clear hierarchy, no decorative noise |
| "Dense" | 12–14px body type, tighter spacing tokens, data-table mindset |
| "Spacious" | 16px+ body type, generous padding, card-based layout |

If the user can't answer, propose two directions (e.g. "Option A: dark and focused like Linear; Option B: light and warm like Notion") and ask which resonates more.

## Design Context Protocol

**Once the brief is complete**, confirm these four technical parameters:

1. **Industry** → selects palette personality and typography register
2. **Primary action** → determines information density (sparse vs. dense)
3. **Target device** → sets interaction model (touch-first, cursor, hybrid)
4. **Existing brand** → locks palette anchors before introducing accent colors

> Then invoke `frontend-design` for aesthetic direction. Return here for technical execution.

## Technical Non-Negotiables

**Grid & Spacing** — 4pt base unit (all spacing = multiples of 4). Token names: `space-1=4px`, `space-2=8px`, `space-4=16px`. Use container queries for component-level responsiveness.

**Color** — OKLCH for all tokens (not HSL). Tinted neutrals, never pure gray. WCAG 2.2 AA minimum: 4.5:1 text, 3:1 UI components. Dark mode = separate palette, never `filter: invert()`. See [color-and-contrast.md](reference/color-and-contrast.md).

**Typography** — Avoid Inter, Roboto, Arial, Open Sans, Space Grotesk. Fluid type with `clamp()`. `font-display: swap` with fallback metrics. See [typography.md](reference/typography.md).

**Motion** — 100ms micro, 300ms standard, 500ms cinematic. Animate only `transform` and `opacity`. `prefers-reduced-motion` is mandatory. See [motion-design.md](reference/motion-design.md).

**Interaction** — 8 states required: default, hover, focus-visible, active, disabled, loading, error, success. Use `:focus-visible` not `outline: none`. See [interaction-design.md](reference/interaction-design.md).

## Anti-Pattern Hard Stops

| ❌ Banned | ✅ Instead |
|---|---|
| `border-radius: 20–32px` everywhere | Match radius to element size (4–8px small, 12px card) |
| Glassmorphism floating shells | Solid surfaces with depth through shadow |
| Purple/blue gradient on white | Project colors → curated palette → never invented |
| Metric-card grid as default layout | Earn that layout; start with list or table |
| Sticky sidebar as default nav | Contextual navigation for complex flows only |
| `transform: scale(1.05)` on hover | Subtle background-color shift instead |
| Gradient text (`background-clip: text`) | Color communicates meaning; decorative gradients are noise |
| Hero sections in dashboards | Hero = landing pages only |
| `box-shadow: 0 20px 60px rgba(0,0,0,0.4)` | Max shadow alpha: 0.12 |
| `outline: none` on focus | `:focus-visible` with visible ring |

Full list with rationale: [anti-patterns.md](reference/anti-patterns.md)

## Industry Context Map

| Context | Personality | Avoid |
|---|---|---|
| SaaS dashboard | Functional / Precise | Decorative hero, heavy animation |
| Consumer / Social | Warm / Playful | Dense tables, monochrome palette |
| Finance / Legal | Conservative / Authoritative | Saturated accents, rounded playfulness |
| Creative / Portfolio | Expressive / Distinctive | Template layouts, system fonts |
| E-commerce | Conversion-focused | Visual noise, competing CTAs |
| Dev tools | Dense / Efficient | Touch-optimized flows, oversized hit targets |

## Pre-Delivery Checklist

Before declaring any UI done:

- [ ] Keyboard-navigable end-to-end; `aria-label` on all icon buttons
- [ ] `@media (prefers-reduced-motion: reduce)` disables or slows all animations
- [ ] Color contrast verified: 4.5:1 text, 3:1 borders/icons
- [ ] Mobile tested at 375px — no horizontal overflow, touch targets ≥ 44×44px
- [ ] Dark mode uses separate token set (not inverted)
- [ ] Empty, loading, error, and success states all handled
- [ ] Typography scales fluidly; no orphaned short lines
- [ ] Only `transform`/`opacity` animated (GPU compositing verified)
- [ ] No banned anti-patterns present
- [ ] Zero console errors in DevTools

## Reference Files

- [natural-language-design.md](reference/natural-language-design.md) — Visual brands → design DNA, feeling words → choices, iteration prevention
- [typography.md](reference/typography.md) — Fluid type, modular scale, font loading, OpenType features
- [color-and-contrast.md](reference/color-and-contrast.md) — OKLCH, WCAG ratios, tinted neutrals, dark mode
- [motion-design.md](reference/motion-design.md) — Timing rules, easing curves, GPU-safe properties
- [interaction-design.md](reference/interaction-design.md) — 8 states, focus rings, keyboard navigation, forms
- [spatial-design.md](reference/spatial-design.md) — Grid system, spacing tokens, visual hierarchy
- [responsive-design.md](reference/responsive-design.md) — Mobile-first, container queries, safe areas, srcset
- [anti-patterns.md](reference/anti-patterns.md) — Full banned pattern list with context and rationale
- [accessibility.md](reference/accessibility.md) — WCAG 2.2 AA gates, ARIA patterns, focus management
