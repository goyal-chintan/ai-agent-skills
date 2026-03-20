# Accessibility Reference

WCAG 2.2 AA compliance gates, ARIA patterns, and focus management. These are **minimum requirements**, not enhancements.

---

## WCAG 2.2 AA — The Non-Negotiables

| Criterion | Requirement | Quick Test |
|---|---|---|
| **1.4.3 Contrast** | 4.5:1 for text, 3:1 for UI components | Browser DevTools → Accessibility panel |
| **1.4.4 Resize Text** | No content loss at 200% zoom | Browser zoom to 200% |
| **1.4.10 Reflow** | No horizontal scroll at 320px width | Resize or DevTools mobile view |
| **1.4.11 Non-text Contrast** | 3:1 for borders, icons, focus rings | Check with contrast checker |
| **1.4.12 Text Spacing** | No loss with line-height 1.5×, letter-spacing 0.12em | Apply via bookmarklet |
| **2.1.1 Keyboard** | All functionality reachable by keyboard | Tab through entire page |
| **2.4.7 Focus Visible** | Focus indicator always visible | Never `outline: none` without replacement |
| **2.4.11 Focus Appearance** (2.2) | Focus indicator ≥ 2px, 3:1 contrast | Visual check on all interactive elements |
| **3.2.2 On Input** | No unexpected context change on input | Test all selects, checkboxes, text fields |
| **4.1.2 Name, Role, Value** | All UI components have accessible name | Run axe DevTools scan |

---

## Focus Management

### `:focus-visible` Not `outline: none`

```css
/* ❌ Destroys keyboard accessibility */
button:focus {
  outline: none;
}

/* ✅ Hides for mouse, shows for keyboard */
button:focus:not(:focus-visible) {
  outline: none;
}
button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
```

### Focus Ring Design

Visible against all backgrounds — use offset + contrasting color:

```css
:root {
  --color-focus-ring: oklch(55% 0.2 250); /* brand blue */
}

/* Consistent across all interactive elements */
:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 3px;
  border-radius: inherit; /* follows element shape */
}
```

### Modal Focus Trapping

Use the native `<dialog>` element — it handles focus trapping automatically:

```html
<!-- ✅ Native dialog — focus trapped, Escape closes, backdrop click optional -->
<dialog id="confirm-dialog" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm action</h2>
  <p>This cannot be undone.</p>
  <button autofocus>Cancel</button>
  <button>Confirm</button>
</dialog>
```

```js
// Open with showModal() — activates focus trap
document.getElementById('confirm-dialog').showModal();
```

If you must use a custom modal (not `<dialog>`), use `inert` on the background:

```js
document.getElementById('main-content').inert = true; // blocks focus + pointer events
modal.removeAttribute('inert');
modal.querySelector('[autofocus]')?.focus();
```

---

## ARIA Patterns

### Icon Buttons (Most Common Mistake)

```html
<!-- ❌ Screen readers announce "button" with no label -->
<button>
  <svg><!-- trash icon --></svg>
</button>

<!-- ✅ Visible label preferred -->
<button>
  <svg aria-hidden="true"><!-- trash icon --></svg>
  Delete
</button>

<!-- ✅ Icon-only: aria-label required -->
<button aria-label="Delete item">
  <svg aria-hidden="true"><!-- trash icon --></svg>
</button>
```

### Form Fields

Every input needs a visible `<label>` — not just `placeholder`:

```html
<!-- ❌ Placeholder disappears on input, no label announced -->
<input type="email" placeholder="Email address">

<!-- ✅ Visible label + input association -->
<label for="email">Email address</label>
<input id="email" type="email" autocomplete="email">

<!-- ✅ Visually hidden label (only when truly space-constrained) -->
<label for="search" class="sr-only">Search</label>
<input id="search" type="search" placeholder="Search...">
```

### Live Regions (Dynamic Updates)

For status messages, toasts, or async results that appear without focus movement:

```html
<!-- Status updates (polite — waits for user idle) -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- Inject success/error messages here -->
</div>

<!-- Critical alerts (assertive — interrupts immediately) -->
<div role="alert" aria-live="assertive">
  <!-- Use sparingly — session-critical errors only -->
</div>
```

### Navigation Landmarks

Every page needs these landmarks for screen reader navigation:

```html
<header role="banner">     <!-- site header -->
<nav aria-label="Main">    <!-- primary navigation -->
<main>                     <!-- primary content (one per page) -->
<aside aria-label="...">   <!-- supplementary content -->
<footer role="contentinfo"> <!-- site footer -->
```

### Loading States

```html
<!-- Button loading state -->
<button aria-busy="true" aria-disabled="true">
  <span aria-hidden="true"><!-- spinner --></span>
  <span class="sr-only">Saving…</span>
</button>

<!-- Content loading region -->
<div aria-busy="true" aria-label="Loading results">
  <!-- skeleton UI -->
</div>
```

---

## Color & Contrast Patterns

### Don't Rely on Color Alone

Information must have a non-color indicator:

```html
<!-- ❌ Red = error, green = success — color-only -->
<span style="color: red">Invalid email</span>

<!-- ✅ Color + icon + text -->
<span class="error" role="alert">
  <svg aria-hidden="true"><!-- error icon --></svg>
  Invalid email address
</span>
```

### Contrast Calculation (OKLCH)

WCAG uses relative luminance. When using OKLCH:
- L (lightness) ≥ 0.65 on dark backgrounds passes 4.5:1 for most hues
- L ≤ 0.35 on light backgrounds passes 4.5:1 for most hues
- Saturated colors (C > 0.15) may need L adjustment — always verify with a tool

**Quick tool:** [https://oklch.com](https://oklch.com) shows contrast ratios live.

---

## Screen-Reader-Only Utility Class

Every project needs this:

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Visible on focus (skip links) */
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  clip: auto;
  white-space: normal;
}
```

---

## Skip Links

Required for keyboard users on pages with navigation before main content:

```html
<!-- First element in <body> -->
<a href="#main-content" class="sr-only sr-only-focusable">
  Skip to main content
</a>

<!-- ... nav, header ... -->

<main id="main-content" tabindex="-1">
```

---

## Motion & Vestibular Safety

See [motion-design.md](motion-design.md) for full rules. Accessibility summary:

```css
/* Required on ALL animation declarations */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Do **not** simply remove animations at `prefers-reduced-motion`. Replace motion-conveyed information with an alternative (e.g., a static state change) — some animations communicate meaning.

---

## Automated Testing

Run these before shipping:

```bash
# axe-core via CLI (fastest)
npx axe-cli http://localhost:3000 --exit

# Pa11y for CI
npx pa11y http://localhost:3000 --standard WCAG2AA

# Lighthouse accessibility audit
npx lighthouse http://localhost:3000 --only-categories=accessibility
```

Target: **zero axe violations** at AA level. Lighthouse score ≥ 90.

---

## Pre-Ship Accessibility Checklist

- [ ] Tab through entire UI — every interactive element reachable and operable
- [ ] Focus rings visible on all focusable elements (never suppressed)
- [ ] All icon buttons have `aria-label`
- [ ] All form inputs have visible `<label>` elements (not just placeholder)
- [ ] Modal/dialog uses `<dialog>` or has `inert` + focus trap
- [ ] Color contrast: 4.5:1 text, 3:1 UI components (verified with tool)
- [ ] No information conveyed by color alone
- [ ] `aria-live` regions present for dynamic status/error messages
- [ ] `prefers-reduced-motion` disables/replaces all animations
- [ ] Skip link present and functional
- [ ] axe-core scan returns zero violations
