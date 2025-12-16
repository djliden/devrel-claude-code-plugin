---
name: screenshot-beautifier
description: Beautify screenshots using ImageMagick - add rounded corners, drop shadows, gradient backgrounds, padding. Use when preparing screenshots for blog posts, documentation, or presentations. Transforms raw Playwright/browser screenshots into polished images.
allowed-tools: Read, Glob, Bash
---

# Screenshot Beautifier (ImageMagick)

Transform raw screenshots into polished, professional images with rounded corners, shadows, and backgrounds.

## Prerequisites

ImageMagick must be installed:
```bash
# macOS
brew install imagemagick

# Ubuntu/Debian
apt-get install imagemagick

# Check installation
convert --version
```

## Quick Beautification Commands

### Default: macOS Window Style (RECOMMENDED)

This matches native macOS Cmd+Shift+4+Space window captures - rounded corners, soft shadow, light background:

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_polished.png"
RADIUS=10

convert "$INPUT" \
  \( +clone -alpha extract \
    -draw "fill black polygon 0,0 0,$RADIUS $RADIUS,0 fill white circle $RADIUS,$RADIUS $RADIUS,0" \
    \( +clone -flip \) -compose Multiply -composite \
    \( +clone -flop \) -compose Multiply -composite \
  \) -alpha off -compose CopyOpacity -composite \
  -background none -gravity center -extent $(identify -format '%[fx:w+80]x%[fx:h+80]' "$INPUT") \
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

convert "$INPUT" \
  \( +clone -alpha extract \
    -draw 'fill black polygon 0,0 0,12 12,0 fill white circle 12,12 12,0' \
    \( +clone -flip \) -compose Multiply -composite \
    \( +clone -flop \) -compose Multiply -composite \
  \) -alpha off -compose CopyOpacity -composite \
  -background none -gravity center -extent $(identify -format '%[fx:w+60]x%[fx:h+60]' "$INPUT") \
  \( +clone -background black -shadow 60x8+0+4 \) +swap \
  -background white -layers merge +repage \
  "$OUTPUT"
```

### Modern: Gradient Background (Purple/Blue)

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_gradient.png"
WIDTH=$(identify -format '%w' "$INPUT")
HEIGHT=$(identify -format '%h' "$INPUT")
BG_WIDTH=$((WIDTH + 120))
BG_HEIGHT=$((HEIGHT + 120))

# Create gradient background
convert -size ${BG_WIDTH}x${BG_HEIGHT} \
  gradient:'#667eea'-'#764ba2' \
  \( "$INPUT" \
    \( +clone -alpha extract \
      -draw 'fill black polygon 0,0 0,12 12,0 fill white circle 12,12 12,0' \
      \( +clone -flip \) -compose Multiply -composite \
      \( +clone -flop \) -compose Multiply -composite \
    \) -alpha off -compose CopyOpacity -composite \
    \( +clone -background black -shadow 80x12+0+8 \) +swap \
    -background none -layers merge +repage \
  \) -gravity center -composite \
  "$OUTPUT"
```

### Minimal: Light Gray Background + Subtle Shadow

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_minimal.png"

convert "$INPUT" \
  -background none -gravity center -extent $(identify -format '%[fx:w+80]x%[fx:h+80]' "$INPUT") \
  \( +clone -background 'rgba(0,0,0,0.15)' -shadow 40x6+0+3 \) +swap \
  -background '#f5f5f5' -layers merge +repage \
  "$OUTPUT"
```

### Dark Mode: Dark Background + Glow

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_dark.png"
WIDTH=$(identify -format '%w' "$INPUT")
HEIGHT=$(identify -format '%h' "$INPUT")
BG_WIDTH=$((WIDTH + 100))
BG_HEIGHT=$((HEIGHT + 100))

convert -size ${BG_WIDTH}x${BG_HEIGHT} xc:'#1a1a2e' \
  \( "$INPUT" \
    \( +clone -alpha extract \
      -draw 'fill black polygon 0,0 0,10 10,0 fill white circle 10,10 10,0' \
      \( +clone -flip \) -compose Multiply -composite \
      \( +clone -flop \) -compose Multiply -composite \
    \) -alpha off -compose CopyOpacity -composite \
    \( +clone -background '#4a00e0' -shadow 100x20+0+0 \) +swap \
    -background none -layers merge +repage \
  \) -gravity center -composite \
  "$OUTPUT"
```

## Batch Processing

Process all screenshots in a directory:

```bash
for img in screenshots/*.png; do
  OUTPUT="${img%.png}_polished.png"
  convert "$img" \
    -background none -gravity center -extent $(identify -format '%[fx:w+60]x%[fx:h+60]' "$img") \
    \( +clone -background black -shadow 60x8+0+4 \) +swap \
    -background white -layers merge +repage \
    "$OUTPUT"
  echo "Processed: $OUTPUT"
done
```

## Parameters Explained

- **Rounded corners**: The `-draw 'fill black polygon...'` creates corner masks
- **Shadow**: `-shadow 60x8+0+4` = opacity 60%, blur 8px, offset x+0 y+4
- **Padding**: `-extent` adds space around the image
- **Background**: Final `-background` sets the canvas color

## Common Adjustments

| Want | Change |
|------|--------|
| Larger shadow | Increase blur: `-shadow 80x12+0+8` |
| More padding | Increase extent: `%[fx:w+120]x%[fx:h+120]` |
| Sharper corners | Reduce radius: change `12` to `8` in polygon/circle |
| Different gradient | Change colors: `gradient:'#ff6b6b'-'#feca57'` |

## Integration with Playwright Screenshots

After taking a screenshot with Playwright:

```bash
# 1. Screenshot is saved by Playwright to screenshots/raw/
# 2. Beautify it
INPUT="screenshots/raw/mlflow-traces.png"
OUTPUT="screenshots/mlflow-traces.png"

convert "$INPUT" \
  [... beautification command ...]
  "$OUTPUT"

# 3. Reference the beautified version in blog posts
# ![MLflow Traces](./screenshots/mlflow-traces.png)
```

## Troubleshooting

**"convert: command not found"**
→ Install ImageMagick: `brew install imagemagick`

**Transparency not preserved**
→ Use `-background none` before operations, save as PNG

**Image too large/small after processing**
→ Adjust the extent calculation or add explicit resize: `-resize 1200x`
