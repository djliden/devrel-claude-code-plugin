---
name: screenshot-beautifier
description: Beautify screenshots using ImageMagick - add rounded corners, drop shadows, gradient backgrounds, padding. Use when preparing screenshots for blog posts, documentation, or presentations. Transforms raw Playwright/browser screenshots into polished images.
allowed-tools: Read, Glob, Bash
---

# Screenshot Beautifier (ImageMagick)

Transform raw screenshots into polished, professional images with rounded corners, shadows, and backgrounds.

## Prerequisites

ImageMagick 7 must be installed:
```bash
# macOS
brew install imagemagick

# Ubuntu/Debian
apt-get install imagemagick

# Check installation
magick --version
```

## Quick Beautification Commands

### Default: macOS Window Style (RECOMMENDED)

This matches native macOS Cmd+Shift+4+Space window captures - rounded corners, soft shadow, light background:

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_polished.png"
RADIUS=10

# Get dimensions
WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")

# Create mask from scratch (not from source alpha) and apply with shadow
magick "$INPUT" -alpha set \
  \( -size ${WIDTH}x${HEIGHT} xc:black \
    -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
  \) -alpha off -compose CopyOpacity -composite \
  -background none -gravity center -extent $((WIDTH+80))x$((HEIGHT+80)) \
  \( +clone -background 'rgba(0,0,0,0.35)' -shadow 100x24+0+12 \) +swap \
  -background '#f0f0f0' -layers merge +repage \
  "$OUTPUT"
```

Or use the helper script:
```bash
./scripts/beautify.sh screenshot.png macos screenshot_polished.png
```

### Alternative: Rounded Corners + Shadow + White Background

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_polished.png"
RADIUS=12

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")

magick "$INPUT" -alpha set \
  \( -size ${WIDTH}x${HEIGHT} xc:black \
    -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
  \) -alpha off -compose CopyOpacity -composite \
  -background none -gravity center -extent $((WIDTH+60))x$((HEIGHT+60)) \
  \( +clone -background black -shadow 60x8+0+4 \) +swap \
  -background white -layers merge +repage \
  "$OUTPUT"
```

### Modern: Gradient Background (Purple/Blue)

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_gradient.png"
RADIUS=12

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")
BG_WIDTH=$((WIDTH + 120))
BG_HEIGHT=$((HEIGHT + 120))

# Create gradient background with rounded screenshot
magick -size ${BG_WIDTH}x${BG_HEIGHT} \
  gradient:'#667eea'-'#764ba2' \
  \( "$INPUT" -alpha set \
    \( -size ${WIDTH}x${HEIGHT} xc:black \
      -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
    \) -alpha off -compose CopyOpacity -composite \
    \( +clone -background black -shadow 80x12+0+8 \) +swap \
    -background none -layers merge +repage \
  \) -gravity center -composite \
  "$OUTPUT"
```

### Minimal: Light Gray Background + Subtle Shadow (No Rounded Corners)

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_minimal.png"

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")

magick "$INPUT" \
  -background none -gravity center -extent $((WIDTH+80))x$((HEIGHT+80)) \
  \( +clone -background 'rgba(0,0,0,0.15)' -shadow 40x6+0+3 \) +swap \
  -background '#f5f5f5' -layers merge +repage \
  "$OUTPUT"
```

### Dark Mode: Dark Background + Glow

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_dark.png"
RADIUS=10

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")
BG_WIDTH=$((WIDTH + 100))
BG_HEIGHT=$((HEIGHT + 100))

magick -size ${BG_WIDTH}x${BG_HEIGHT} xc:'#1a1a2e' \
  \( "$INPUT" -alpha set \
    \( -size ${WIDTH}x${HEIGHT} xc:black \
      -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
    \) -alpha off -compose CopyOpacity -composite \
    \( +clone -background '#4a00e0' -shadow 100x20+0+0 \) +swap \
    -background none -layers merge +repage \
  \) -gravity center -composite \
  "$OUTPUT"
```

## Batch Processing

Process all screenshots in a directory (shadow only, no rounded corners):

```bash
for img in screenshots/*.png; do
  OUTPUT="${img%.png}_polished.png"
  WIDTH=$(magick identify -format '%w' "$img")
  HEIGHT=$(magick identify -format '%h' "$img")
  magick "$img" \
    -background none -gravity center -extent $((WIDTH+60))x$((HEIGHT+60)) \
    \( +clone -background black -shadow 60x8+0+4 \) +swap \
    -background white -layers merge +repage \
    "$OUTPUT"
  echo "Processed: $OUTPUT"
done
```

## Parameters Explained

- **Rounded corners**: Create a black canvas with `-size WxH xc:black`, then draw a white `roundrectangle` mask (format: `x1,y1,x2,y2,rx,ry` where rx/ry are corner radii). Apply as alpha with `-compose CopyOpacity -composite`
- **Alpha setup**: Use `-alpha set` on opaque PNGs (like Playwright screenshots) to ensure they have an alpha channel before applying the mask
- **Shadow**: `-shadow 60x8+0+4` = opacity 60%, blur 8px, offset x+0 y+4
- **Padding**: `-extent` adds space around the image
- **Background**: Final `-background` sets the canvas color

## Common Adjustments

| Want | Change |
|------|--------|
| Larger shadow | Increase blur: `-shadow 80x12+0+8` |
| More padding | Increase extent values (e.g., `+120` instead of `+80`) |
| Sharper corners | Reduce `RADIUS` value (e.g., `8` instead of `12`) |
| Rounder corners | Increase `RADIUS` value (e.g., `20` instead of `12`) |
| Different gradient | Change colors: `gradient:'#ff6b6b'-'#feca57'` |

## Integration with Playwright Screenshots

After taking a screenshot with Playwright:

```bash
# 1. Screenshot is saved by Playwright to screenshots/raw/
# 2. Beautify it
INPUT="screenshots/raw/mlflow-traces.png"
OUTPUT="screenshots/mlflow-traces.png"
RADIUS=10

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")

magick "$INPUT" -alpha set \
  \( -size ${WIDTH}x${HEIGHT} xc:black \
    -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
  \) -alpha off -compose CopyOpacity -composite \
  -background none -gravity center -extent $((WIDTH+80))x$((HEIGHT+80)) \
  \( +clone -background 'rgba(0,0,0,0.35)' -shadow 100x24+0+12 \) +swap \
  -background '#f0f0f0' -layers merge +repage \
  "$OUTPUT"

# 3. Reference the beautified version in blog posts
# ![MLflow Traces](./screenshots/mlflow-traces.png)
```

## Troubleshooting

**"magick: command not found"**
→ Install ImageMagick: `brew install imagemagick`

**Transparency not preserved**
→ Use `-background none` before operations, save as PNG

**Image too large/small after processing**
→ Adjust the extent calculation or add explicit resize: `-resize 1200x`

**White border appears around image / corners not rounded**
→ Playwright screenshots are fully opaque PNGs. Don't extract alpha from the source; create the mask from scratch with `-size WxH xc:black` instead of `+clone -alpha extract`
