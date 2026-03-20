# Natural Language → Design Decisions

A translation layer between how users describe what they want and the actual design choices that produce it. Use this when the user describes UI in emotional, visual, or reference-based terms rather than technical specs.

---

## Visual Reference Brands → Design DNA

### Linear
- Near-black background (`oklch(12% 0.01 250)`)
- Tight spacing (4–8px gaps, dense information)
- Monospace or geometric sans (Geist, Inter Mono for code)
- Restrained color (single accent, muted everywhere else)
- Micro-animations: fast (100–150ms), easing-out
- No gradients, no decoration, zero noise

### Stripe
- Deep navy + electric indigo/purple (`oklch(35% 0.12 280)` + `oklch(65% 0.25 275)`)
- Dense but meticulously structured — every element earns its place
- Heavy typographic hierarchy (900 weight headlines)
- Rich gradient meshes in hero/marketing only
- High-trust, premium engineering aesthetic

### Airbnb / Warm Consumer
- Warm neutrals (slight red-orange tint in background)
- Coral/rose accent (`oklch(65% 0.18 30)`)
- Photography-forward — images do visual work
- Rounded cards (12–16px radius)
- Generous white space, unhurried layout

### Notion / GitHub
- Dense information architecture
- Neutral palette — color is semantic only (status, tags)
- Monospace for data/code, sans for prose
- Flat UI with minimal shadow
- Keyboard-first design language

### Apple
- Ultra-minimal — maximum restraint
- Light mode: near-white with warm undertones
- Dark mode: layered dark surfaces (not flat black)
- SF Pro or equivalent humanist sans
- Animation: fluid, physics-based, intentional
- No icons without labels in core UI

### Vercel / Dev Tools
- True black (`oklch(5% 0.005 250)`)
- Monospace type as a design element
- High contrast: white text on black
- Minimal navigation chrome
- Code and terminal aesthetics as inspiration

---

## Feeling Words → Design Choices

### "Clean" / "Minimal"
- Reduce color: 1 accent max, neutrals everywhere else
- Increase whitespace: double your default padding
- Remove decorative elements: no gradients, no shadows above level 1
- Typography does the work: strong hierarchy without color

### "Premium" / "Luxury"
- Dark background with tinted neutrals (not pure black)
- Narrow, high-tracking display font for headlines
- Gold or warm bronze accent (`oklch(70% 0.12 80)`)
- Generous spacing + precise alignment
- Subtle texture or noise overlay (2–4% opacity)
- Animations: slow (400–500ms), ease-in-out-quart

### "Friendly" / "Approachable" / "Warm"
- Warmer neutrals (red/orange tint in grays)
- Rounded corners (12–16px on cards, 8px on inputs)
- Slightly heavier body weight (500 instead of 400)
- Saturated but soft accent (high chroma, high lightness)
- Avoid sharp contrast — softer gray/white split

### "Trustworthy" / "Professional" / "Enterprise"
- Conservative palette: navy, slate, or forest green anchor
- No decorative gradients
- Compact spacing — dense layouts signal seriousness
- Table-heavy information design
- Tabular numbers for all data
- Clear status indicators (color + icon + text, never color alone)

### "Bold" / "Energetic" / "Exciting"
- High contrast: near-black on near-white, or reverse
- Saturated accent pushed to maximum viable chroma
- Asymmetric layouts — break the grid intentionally
- Fast animations (100–200ms) with snap easing
- Large, heavy typographic moments
- Full-bleed sections

### "Calm" / "Focused" / "Meditative"
- Desaturated palette (chroma < 0.06 for neutrals)
- Maximum whitespace — generous margins
- Single typographic scale (no dramatic size jumps)
- No hover animations beyond color shifts
- Muted success/error states

### "Playful" / "Fun" / "Creative"
- Multiple accent colors (2–3, intentionally chosen)
- Unexpected font pairing (display + handwritten, or geometric + serif)
- Asymmetric or diagonal elements
- Spring/bounce easing (only here — normally banned)
- Generous border radius (pill buttons acceptable)
- Illustrations or custom iconography over system icons

---

## Density Words → Spacing Decisions

| User says | Spacing multiplier | Base padding | Body size |
|---|---|---|---|
| "Dense" / "compact" / "lots of info" | 0.75× | 8–12px | 12–13px |
| "Normal" / "standard" | 1× | 16px | 14–15px |
| "Spacious" / "breathable" / "airy" | 1.5× | 24–32px | 16px |
| "Very minimal" / "zen" | 2× | 40–48px | 16–18px |

---

## Iteration Prevention: What to Show Before Full Build

When the user's request is ambiguous, **show a design decision summary before writing component code**:

```
Before I start, here's what I've decided based on your description:

Aesthetic: Dark, focused (Linear-inspired)
  - Background: near-black with cool tint
  - Accent: electric blue (oklch 65% 0.22 250)
  - Font: Geist Sans / Geist Mono for data

Density: Standard — 16px base padding, 14px body text

Personality: Professional + focused (not playful)
  - Animations: fast (150ms), no bounce
  - Shadows: level 1 only (very subtle)
  - Radius: 6px cards, 4px inputs

Does this match what you had in mind, or should I adjust direction?
```

This takes 30 seconds and prevents a full rebuild if you got the direction wrong.

---

## When the User Says "Make It Better"

This phrase means one of five things. Ask which:

1. **More visual impact** → Increase contrast, add a strong typographic moment
2. **More professional** → Remove decoration, tighten spacing, add structure
3. **More modern** → Update to current patterns (container queries, OKLCH, fluid type)
4. **More accessible** → Fix contrast, add focus rings, check motion
5. **More consistent** → Align spacing tokens, unify border radii, match type scale

Never guess — one question eliminates a full iteration.

---

## When the User Says "Something Like X but Y"

Parse the modifier:

| Pattern | What to keep from X | What to change for Y |
|---|---|---|
| "Like Linear but warmer" | Dark bg, tight spacing, minimal | Warm tint in neutrals, replace blue accent with amber |
| "Like Stripe but lighter" | Dense structure, strong typography | Light mode, replace navy with slate, soften shadows |
| "Like Airbnb but more serious" | Warm palette, spacious layout | Remove rounded playfulness, reduce accent saturation |
| "Like GitHub but cleaner" | Neutral palette, information density | Remove noise, increase whitespace, reduce border frequency |
