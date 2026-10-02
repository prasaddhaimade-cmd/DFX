#!/usr/bin/env python3
"""Builds tokens/tokens.json and tokens/tokens.css for Vanyx, and checks contrast.

Run: python3 build.py
Edit the tables below, re-run, commit the generated files.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).parent

# name, light, dark, usage
COLOR = [
 # --- Surfaces (Carbon layering, Lumen warm neutrals) ---
 ("bg", "#FAFAF8", "#121414", "Page canvas behind everything. Never a card surface."),
 ("layer-01", "#FFFFFF", "#1A1C1D", "First stacked surface: cards, panels, dialogs (Carbon layer-01)."),
 ("layer-02", "#F1F0ED", "#222525", "Second stacked surface: a panel nested inside a layer-01 card, sidebars, inset boxes."),
 ("layer-03", "#E8E6E1", "#2B2E2F", "Third stacked surface: a control or well inside a layer-02 panel. Hovered rows."),
 ("inverse-layer", "#1B1D1F", "#ECEDEA", "Surface that flips against the theme: snackbars, tooltips (Material inverse-surface)."),
 ("on-inverse-layer", "#F4F3F0", "#1B1D1F", "Text and icons on inverse-layer."),
 ("scrim", "#000000", "#000000", "Modal backdrop. Apply at about 40% opacity."),
 # --- Text ---
 ("ink", "#1B1D1F", "#ECEDEA", "Default text and icons on bg and layers."),
 ("ink-muted", "#5B5F63", "#9A9E9F", "The one secondary text level: captions, timestamps, helper text. Do not add a third grey; change weight or size instead."),
 # --- Borders ---
 ("border-subtle", "#DEDDD8", "#34373A", "Quiet dividers: table rules, section separators (Carbon border-subtle)."),
 ("border-strong", "#8A8D8F", "#6A6E70", "Input outlines and any border that must read as interactive. 3:1 on bg."),
 # --- Accent: one teal, Material role pairing ---
 ("accent", "#0E7C7B", "#28B8B3", "The single most important action or data point on a screen. Fills for primary buttons, selected indicators."),
 ("on-accent", "#FFFFFF", "#06201F", "Text and icons on accent."),
 ("accent-container", "#D3EEEC", "#0F3F3E", "Tonal fill for selected items, chips, active nav (Material primary-container)."),
 ("on-accent-container", "#06302F", "#C4EFEC", "Text and icons on accent-container."),
 ("link", "#0A6B6A", "#5ED0CB", "Inline text links and icon-only primary actions (Primer accent-fg). Use this, not accent, for accent-coloured text."),
 ("link-visited", "#7442C4", "#B79BEF", "Visited inline links."),
 ("focus", "#0B5FA5", "#FFFFFF", "Keyboard focus ring. Deliberately not the accent so it stays visible on accent fills (Carbon focus)."),
 # --- Secondary and tertiary roles (Material) ---
 ("secondary-container", "#E4EBEA", "#2A3837", "Quiet tonal fill for secondary buttons and filter chips."),
 ("on-secondary-container", "#1F2F2E", "#D5E3E1", "Text and icons on secondary-container."),
 ("tertiary-container", "#F6E3D8", "#4A2E20", "Warm clay tonal fill for callouts and decorative emphasis. Use rarely."),
 ("on-tertiary-container", "#3B1F10", "#F6E3D8", "Text and icons on tertiary-container."),
 # --- Status: fg / emphasis / container triplets (Primer fg+emphasis, Carbon support, Material container) ---
 ("on-emphasis", "#FFFFFF", "#FFFFFF", "Text and icons on any filled -emphasis colour except warning-emphasis."),
 ("success-fg", "#1A7F37", "#4FBE7B", "Success text and icons: passing checks, confirmations."),
 ("success-emphasis", "#1A7F37", "#238636", "Filled success button or badge. Text on it is on-emphasis."),
 ("success-container", "#DDF3E4", "#12301D", "Success banner and tag background. Text on it is ink."),
 ("warning-fg", "#8A5F00", "#D8A33B", "Warning text and icons."),
 ("warning-emphasis", "#F1C21B", "#D8A33B", "Filled warning badge. Text on it is on-warning-emphasis (dark), never white."),
 ("on-warning-emphasis", "#1B1D1F", "#121414", "Text and icons on warning-emphasis."),
 ("warning-container", "#FBEFC8", "#3A2D0B", "Warning banner and tag background. Text on it is ink."),
 ("danger-fg", "#B8322F", "#F07673", "Error text, destructive icons, field validation messages."),
 ("danger-emphasis", "#C23B3B", "#C9302C", "Filled destructive button. Text on it is on-emphasis."),
 ("danger-container", "#F9DEDC", "#4A1614", "Error banner and field-error background. Text on it is ink."),
 ("info-fg", "#2E6F9E", "#5B9FD1", "Informational text and icons."),
 ("info-emphasis", "#2E6F9E", "#2F6FA8", "Filled info badge. Text on it is on-emphasis."),
 ("info-container", "#DCEAF5", "#14283A", "Info banner and tag background. Text on it is ink."),
 ("done-fg", "#7442C4", "#AB7DF8", "Completed or merged lifecycle state (Primer done). Distinct from success: use for things that have finished a lifecycle."),
 ("done-emphasis", "#7442C4", "#7C4DD6", "Filled done or merged badge. Text on it is on-emphasis."),
 ("done-container", "#EBDFFB", "#2D1F4D", "Done banner and tag background. Text on it is ink."),
 ("neutral-emphasis", "#5B5F63", "#6E7274", "Closed, archived or neutral lifecycle badge. Text on it is on-emphasis."),
]

SPACING = [
 ("space-0", "2px", "Hairline gap: icon-to-text inside a dense tag (Carbon spacing-01)."),
 ("space-1", "4px", "Tightest gap: icon-to-label."),
 ("space-2", "8px", "Gap between closely related inline elements and between related form fields."),
 ("space-3", "12px", "Compact component padding."),
 ("space-4", "16px", "Standard card and panel padding. The most common step."),
 ("space-5", "24px", "Gap between sibling cards and between form sections."),
 ("space-6", "32px", "Gap between distinct content groups."),
 ("space-7", "40px", "Page header to page content."),
 ("space-8", "48px", "Page-level section spacing."),
 ("space-9", "64px", "Hero and top-level section breaks, wide-layout page margins."),
]

RADIUS = [
 ("radius-none", "0px", "Full-bleed images, dense data tables, Carbon-style productive screens."),
 ("radius-xs", "4px", "Tags and small chips."),
 ("radius-sm", "6px", "Controls: inputs, selects, badges (Primer default control radius)."),
 ("radius-md", "10px", "Default for buttons and cards."),
 ("radius-lg", "16px", "Dialogs, bottom sheets, prominent cards."),
 ("radius-xl", "28px", "Expressive hero containers. Marketing and editorial only."),
 ("radius-full", "9999px", "Pills, avatars, switches. Not every rectangle."),
]

SHADOW = [
 ("shadow-1", "0 1px 2px rgba(27,29,31,0.10), 0 1px 3px rgba(27,29,31,0.08)", "Resting raised surface: cards that need lift."),
 ("shadow-2", "0 2px 6px rgba(27,29,31,0.12), 0 1px 2px rgba(27,29,31,0.08)", "Hovered cards, menus, popovers."),
 ("shadow-3", "0 8px 24px rgba(27,29,31,0.16), 0 2px 6px rgba(27,29,31,0.10)", "Dialogs and sheets."),
]

FAMILIES = {
 "display": "'Fraunces', 'Iowan Old Style', Georgia, serif",
 "sans": "'Karla', system-ui, -apple-system, 'Segoe UI', sans-serif",
 "mono": "'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace",
}

# group, family, [(name, size, line, weight)]
TYPE = [
 ("Display", "display", [("display-large", 56, 60, 600), ("display-medium", 40, 46, 600), ("display-small", 32, 40, 600)]),
 ("Headline", "sans", [("headline-large", 28, 34, 700), ("headline-medium", 24, 32, 700), ("headline-small", 20, 28, 700)]),
 ("Title", "sans", [("title-large", 18, 26, 700), ("title-medium", 16, 22, 700), ("title-small", 14, 20, 700)]),
 ("Body", "sans", [("body-large", 16, 24, 400), ("body-medium", 14, 20, 400), ("body-small", 13, 20, 400), ("body-compact", 14, 18, 400)]),
 ("Label", "sans", [("label-large", 14, 20, 600), ("label-medium", 12, 16, 600), ("label-small", 11, 16, 600)]),
 ("Data", "mono", [("data-large", 14, 20, 500), ("data-small", 12, 16, 400)]),
]

# (foreground token, background token, minimum ratio, note)
PAIRS = [
 ("ink","bg",4.5),("ink","layer-01",4.5),("ink","layer-02",4.5),("ink","layer-03",4.5),
 ("ink-muted","bg",4.5),("ink-muted","layer-01",4.5),("ink-muted","layer-02",4.5),
 ("on-inverse-layer","inverse-layer",4.5),
 ("on-accent","accent",4.5),("on-accent-container","accent-container",4.5),
 ("link","bg",4.5),("link","layer-01",4.5),("link-visited","layer-01",4.5),
 ("accent","bg",3.0),("accent","layer-01",3.0),
 ("focus","bg",3.0),("focus","layer-01",3.0),
 ("border-strong","bg",3.0),("border-strong","layer-01",3.0),
 ("on-secondary-container","secondary-container",4.5),
 ("on-tertiary-container","tertiary-container",4.5),
 ("on-emphasis","success-emphasis",4.5),("on-emphasis","danger-emphasis",4.5),
 ("on-emphasis","info-emphasis",4.5),("on-emphasis","done-emphasis",4.5),
 ("on-emphasis","neutral-emphasis",4.5),("on-warning-emphasis","warning-emphasis",4.5),
 ("success-fg","layer-01",4.5),("warning-fg","layer-01",4.5),("danger-fg","layer-01",4.5),
 ("info-fg","layer-01",4.5),("done-fg","layer-01",4.5),
 ("ink","success-container",4.5),("ink","warning-container",4.5),("ink","danger-container",4.5),
 ("ink","info-container",4.5),("ink","done-container",4.5),
 ("danger-fg","danger-container",4.5),
]


def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check():
    c = {n: {"light": l, "dark": d} for n, l, d, _ in COLOR}
    bad = 0
    for fg, bg, need in PAIRS:
        for th in ("light", "dark"):
            r = ratio(c[fg][th], c[bg][th])
            if r < need:
                bad += 1
                print(f"FAIL {th:5} {fg} on {bg}: {r:.2f} < {need}")
    print(f"contrast: {len(PAIRS)*2 - bad}/{len(PAIRS)*2} pairs pass")
    return bad


def tokens_json():
    px = lambda n: f"{n}px"
    return {
        "name": "Vanyx",
        "version": 1,
        "color": {
            "themes": [{"id": "light", "name": "Light"}, {"id": "dark", "name": "Dark"}],
            "tokens": [{"name": n, "value": {"light": l, "dark": d}, "usage": u} for n, l, d, u in COLOR],
        },
        "type": {
            "fonts": [],
            "families": FAMILIES,
            "groups": [
                {"name": g, "family": f, "styles": [
                    {"name": n, "fontSize": px(s), "lineHeight": px(lh), "fontWeight": w} for n, s, lh, w in styles]}
                for g, f, styles in TYPE
            ],
        },
        "spacing": {"tokens": [{"name": n, "value": v, "usage": u} for n, v, u in SPACING]},
        "radius": {"tokens": [{"name": n, "value": v, "usage": u} for n, v, u in RADIUS]},
        "shadow": {"tokens": [{"name": n, "value": v, "usage": u} for n, v, u in SHADOW]},
    }


def tokens_css():
    out = ["/* Vanyx design tokens. GENERATED by build.py, do not edit by hand. */", ""]
    out.append(":root,\n:root[data-theme=\"light\"] {")
    for n, l, _, _ in COLOR:
        out.append(f"  --{n}: {l};")
    out.append("  color-scheme: light;\n}\n")
    dark = "\n".join(f"    --{n}: {d};" for n, _, d, _ in COLOR)
    out.append("@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {\n" + dark + "\n    color-scheme: dark;\n  }\n}\n")
    dark2 = "\n".join(f"  --{n}: {d};" for n, _, d, _ in COLOR)
    out.append(":root[data-theme=\"dark\"] {\n" + dark2 + "\n  color-scheme: dark;\n}\n")
    out.append(":root {")
    for k, v in FAMILIES.items():
        out.append(f"  --font-{k}: {v};")
    for n, v, _ in SPACING:
        out.append(f"  --{n}: {v};")
    for n, v, _ in RADIUS:
        out.append(f"  --{n}: {v};")
    for n, v, _ in SHADOW:
        out.append(f"  --{n}: {v};")
    for g, f, styles in TYPE:
        for n, s, lh, w in styles:
            out.append(f"  --type-{n}: {w} {s}px/{lh}px var(--font-{f});")
    out.append("}\n")
    out.append("/* Type utility classes: .t-body-medium { font: var(--type-body-medium); } */")
    for g, f, styles in TYPE:
        for n, *_ in styles:
            out.append(f".t-{n} {{ font: var(--type-{n}); }}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    bad = check()
    (ROOT / "tokens").mkdir(exist_ok=True)
    (ROOT / "tokens" / "tokens.json").write_text(json.dumps(tokens_json(), indent=2) + "\n")
    (ROOT / "tokens" / "tokens.css").write_text(tokens_css())
    print("wrote tokens/tokens.json, tokens/tokens.css")
    sys.exit(1 if bad else 0)
