# Vanyx

A custom design system merged from four sources: **Material Design 3**, **IBM Carbon**, **GitHub Primer** and **Lumen**. It is built for product UI that should feel considered rather than generic: dashboards, admin and data tools, settings screens, and the occasional expressive moment.

Everything lives in plain files. Tokens are JSON and CSS custom properties; components are plain CSS with an `vx-` prefix. No framework is required.

## For Claude Design (read this first)

When designing with this system:

1. Link `tokens/tokens.css` then `components/components.css`. Use the CSS variables; never write a raw hex or an arbitrary px value for colour, spacing, radius or shadow.
2. Set text with the `--type-*` shorthand tokens (`font: var(--type-body-medium)`) or the `.t-*` classes.
3. Pick colour by role and by pair: a `-container` fill takes its `on-*-container` text, `accent` takes `on-accent`, a `*-emphasis` fill takes `on-emphasis` (the exception is `warning-emphasis`, which takes `on-warning-emphasis`).
4. Support light and dark. Themes switch with `data-theme="light|dark"` on `<html>`, and follow `prefers-color-scheme` when it is unset.
5. Open `index.html` to see every token and component rendered.

## What came from where

| Source | What Vanyx kept |
| --- | --- |
| **Lumen** | The brand base: warm neutrals, the single teal accent (`accent`), the Fraunces / Karla / JetBrains Mono type trio, 10px default radius, the "one accent, sparingly" rule, `ink` / `ink-muted` as the only text hierarchy. |
| **Material Design 3** | Role pairing (`on-*`), tonal `-container` fills, inverse surface for snackbars, the Display / Headline / Title / Body / Label type vocabulary, elevation levels, the larger radius steps (`radius-lg`, `radius-xl`). |
| **IBM Carbon** | Layering (`layer-01` to `layer-03`) instead of arbitrary greys, `border-subtle` vs `border-strong`, a dedicated `focus` colour, status colours reserved for state, the dense `body-compact` style, `radius-none` for tables, the 2px hairline step. |
| **GitHub Primer** | `fg` plus `emphasis` split for status colours, the `done` (purple) lifecycle state alongside `success`, `neutral-emphasis` for closed, border-over-background card separation, 6px control radius. |

Where sources disagreed, Lumen decided the look, Carbon decided density, Material decided naming and pairing, and Primer decided status semantics.

## Visual foundations

- **Colour.** Warm off-white `bg` with white `layer-01` cards in light; near-black `bg` with slightly lifted layers in dark. One teal `accent`. Never use `accent` for status; use the status colours. Use `link`, not `accent`, for accent-coloured text, because `link` is tuned to pass 4.5:1 on every surface.
- **Surfaces.** `bg` is the page. Cards are `layer-01` with a `border-subtle` outline (Primer style) or `shadow-1` when they need lift. A panel inside a card is `layer-02`; a control or well inside that is `layer-03`. Do not skip levels.
- **Type.** Fraunces (`--font-display`) only for `display-*` moments: hero numbers, page titles, posters. Karla (`--font-sans`) for everything read. JetBrains Mono (`--font-mono`) for numbers in tables, timestamps, IDs and code. Do not jump from Display to Body; bridge with a Headline or Title.
- **Spacing.** `space-0` to `space-9` (2, 4, 8, 12, 16, 24, 32, 40, 48, 64). `space-4` (16) is the default panel padding. Reuse the same five or six steps across a layout.
- **Radius.** `radius-md` for buttons and cards, `radius-sm` for inputs, `radius-xs` for tags, `radius-lg` for dialogs, `radius-none` for dense tables, `radius-full` for pills and avatars only.
- **Elevation.** Prefer borders. `shadow-1` for resting raised cards, `shadow-2` for menus and hover, `shadow-3` for dialogs.
- **Focus.** Always `outline: 2px solid var(--focus); outline-offset: 2px`. The offset keeps the ring on the surrounding surface, which is why `focus` is not measured against `accent` fills.

## Content fundamentals

- Sentence case everywhere. Buttons say what they do ("Save changes", "Delete campaign"), not "OK".
- Status text names the state and the next step: "Sync failed. Check the connection and retry."
- Numbers in tables are right-aligned in `data-large`.

## Accessibility

`build.py` checks 76 foreground/background pairs in both themes on every build. Text pairs meet 4.5:1; borders, focus rings and the accent fill meet 3:1. The build fails if any pair regresses.

## Files

```
tokens/tokens.json        Tokens in Claude Design format (colour with light+dark, type, spacing, radius, shadow)
tokens/tokens.css         Same tokens as CSS custom properties, plus .t-* type classes (generated)
components/components.css Button, input, select, checkbox, card, badge, alert, tabs, table, snackbar, avatar, dialog
index.html                Live showcase of everything, with a theme toggle
build.py                  Source of truth for tokens; regenerates the two token files and checks contrast
```

## Changing a token

Edit the tables at the top of `build.py`, run `python3 build.py`, commit `tokens/`. Do not edit the generated files by hand.

## Not included yet

No JavaScript components, icon set or font files. Fonts load from Google Fonts in `index.html`; add the same `<link>` to your own pages. Components are CSS only, so interactive behaviour (tabs switching, dialogs opening) is up to the host app.
