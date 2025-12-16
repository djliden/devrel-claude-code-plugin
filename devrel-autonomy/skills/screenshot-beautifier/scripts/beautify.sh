#!/bin/bash
# Screenshot Beautifier - Add polish to raw screenshots
# Usage: ./beautify.sh <input.png> [preset] [output.png]
# Presets: macos (default), gradient, minimal, dark, white

set -e

INPUT="$1"
PRESET="${2:-macos}"
OUTPUT="${3:-${INPUT%.png}_beautified.png}"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <input.png> [preset] [output.png]"
  echo "Presets: macos (default), gradient, minimal, dark, white"
  exit 1
fi

if ! command -v convert &> /dev/null; then
  echo "Error: ImageMagick not installed. Run: brew install imagemagick"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Error: File not found: $INPUT"
  exit 1
fi

WIDTH=$(identify -format '%w' "$INPUT")
HEIGHT=$(identify -format '%h' "$INPUT")

case "$PRESET" in
  macos)
    # macOS window screenshot style - rounded corners, soft shadow, light background
    # Matches native macOS Cmd+Shift+4+Space window captures
    RADIUS=10
    convert "$INPUT" \
      \( +clone -alpha extract \
        -draw "fill black polygon 0,0 0,$RADIUS $RADIUS,0 fill white circle $RADIUS,$RADIUS $RADIUS,0" \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
      \) -alpha off -compose CopyOpacity -composite \
      -background none -gravity center -extent $((WIDTH + 80))x$((HEIGHT + 80)) \
      \( +clone -background 'rgba(0,0,0,0.35)' -shadow 100x24+0+12 \) +swap \
      -background '#f0f0f0' -layers merge +repage \
      "$OUTPUT"
    ;;

  gradient)
    # Purple/blue gradient background
    BG_WIDTH=$((WIDTH + 120))
    BG_HEIGHT=$((HEIGHT + 120))
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
    ;;

  minimal)
    # Light gray background, subtle shadow
    convert "$INPUT" \
      -background none -gravity center -extent $((WIDTH + 80))x$((HEIGHT + 80)) \
      \( +clone -background 'rgba(0,0,0,0.15)' -shadow 40x6+0+3 \) +swap \
      -background '#f5f5f5' -layers merge +repage \
      "$OUTPUT"
    ;;

  dark)
    # Dark background with purple glow
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
    ;;

  white)
    # Clean white background with shadow
    convert "$INPUT" \
      \( +clone -alpha extract \
        -draw 'fill black polygon 0,0 0,12 12,0 fill white circle 12,12 12,0' \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
      \) -alpha off -compose CopyOpacity -composite \
      -background none -gravity center -extent $((WIDTH + 60))x$((HEIGHT + 60)) \
      \( +clone -background black -shadow 60x8+0+4 \) +swap \
      -background white -layers merge +repage \
      "$OUTPUT"
    ;;

  *)
    echo "Unknown preset: $PRESET"
    echo "Available presets: gradient, minimal, dark, white"
    exit 1
    ;;
esac

echo "Created: $OUTPUT (preset: $PRESET)"
