#!/usr/bin/env python3
"""Measure a reference UI image and diff it against a render.

Requires Pillow (PIL). No other third-party dependencies.

Usage:
    python image_probe.py info reference.png [--dpr 2]
    python image_probe.py palette reference.png --colors 16
    python image_probe.py sample reference.png --points "24,24;232,64" --radius 2
    python image_probe.py grid reference.png --step 100 --out grid.png
    python image_probe.py crop reference.png --box 0,0,400,300 --out crop.png
    python image_probe.py diff reference.png render.png --out diff.png \
        --overlay overlay.png --tolerance 8 --fail-over 0.5

The diff uses the maximum per-channel difference. `--tolerance` is 0-255.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps, ImageStat
except ImportError:  # pragma: no cover - environment-dependent
    print("error: Pillow is required. Install with: python3 -m pip install Pillow", file=sys.stderr)
    raise SystemExit(2)


def load_rgb(path: str) -> Image.Image:
    try:
        image = Image.open(path)
    except FileNotFoundError:
        raise SystemExit(f"error: file not found: {path}")
    except OSError as exc:
        raise SystemExit(f"error: cannot read {path}: {exc}")
    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGBA")
        background = Image.new("RGB", image.size, "white")
        background.paste(image, mask=image.getchannel("A"))
        return background
    return image.convert("RGB")


def hex_color(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def cmd_info(args: argparse.Namespace) -> int:
    try:
        image = Image.open(args.image)
    except FileNotFoundError:
        raise SystemExit(f"error: file not found: {args.image}")
    except OSError as exc:
        raise SystemExit(f"error: cannot read {args.image}: {exc}")

    width, height = image.size
    dpr = args.dpr if args.dpr > 0 else 1.0
    css_width = width / dpr
    css_height = height / dpr
    info = {
        "file": args.image,
        "format": image.format,
        "mode": image.mode,
        "pixels": [width, height],
        "css_size": [round(css_width, 2), round(css_height, 2)],
        "dpr": dpr,
        "dpi": list(image.info.get("dpi", [])),
        "has_alpha": "A" in image.getbands(),
    }

    rgb = load_rgb(args.image)
    colors = rgb.getcolors(maxcolors=1_000_000)
    if colors:
        colors.sort(reverse=True)
        info["unique_colors"] = len(colors)
        info["top_colors"] = [
            {"color": hex_color(color), "pixels": count}
            for count, color in colors[:8]
        ]
    else:
        info["unique_colors"] = ">1,000,000"

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print(f"file:        {info['file']}")
        print(f"format:      {info['format']} ({info['mode']})")
        print(f"pixels:      {width} x {height}")
        print(f"CSS size:    {css_width:g} x {css_height:g} at DPR {dpr:g}")
        if info["dpi"]:
            print(f"DPI:         {info['dpi']}")
        print(f"alpha:       {info['has_alpha']}")
        print(f"unique:      {info['unique_colors']}")
        print("top colors:")
        for entry in info.get("top_colors", []):
            print(f"  {entry['color']}  {entry['pixels']:>10} px")
    return 0


def cmd_palette(args: argparse.Namespace) -> int:
    rgb = load_rgb(args.image)
    if args.colors < 2 or args.colors > 256:
        raise SystemExit("error: --colors must be between 2 and 256")
    quantized = rgb.quantize(colors=args.colors, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette() or []
    counts = quantized.getcolors(maxcolors=args.colors * 4) or []
    counts.sort(reverse=True)

    total = rgb.width * rgb.height
    entries = []
    for count, index in counts:
        base = index * 3
        rgb_value = tuple(palette[base:base + 3]) if base + 3 <= len(palette) else (0, 0, 0)
        entries.append(
            {
                "color": hex_color(rgb_value),
                "rgb": list(rgb_value),
                "pixels": count,
                "percent": round(100 * count / total, 3),
            }
        )

    if args.json:
        print(json.dumps({"colors": entries}, indent=2))
    else:
        print(f"{len(entries)} colors (quantized to {args.colors}):")
        for entry in entries:
            print(
                f"  {entry['color']}  {entry['percent']:>6.2f}%  "
                f"{entry['pixels']:>9} px  rgb({entry['rgb'][0]}, {entry['rgb'][1]}, {entry['rgb'][2]})"
            )
    return 0


def parse_points(raw: str) -> list[tuple[int, int]]:
    points = []
    for pair in raw.replace(";", " ").split():
        if not pair:
            continue
        if "," not in pair:
            raise SystemExit(f"error: invalid point {pair!r}; expected x,y")
        x, y = pair.split(",", 1)
        try:
            points.append((int(x), int(y)))
        except ValueError:
            raise SystemExit(f"error: invalid point {pair!r}; expected integers")
    if not points:
        raise SystemExit("error: no points provided")
    return points


def cmd_sample(args: argparse.Namespace) -> int:
    rgb = load_rgb(args.image)
    points = []
    for raw in args.points:
        points.extend(parse_points(raw))

    entries = []
    for x, y in points:
        if not (0 <= x < rgb.width and 0 <= y < rgb.height):
            raise SystemExit(f"error: point {x},{y} is outside {rgb.width}x{rgb.height}")
        radius = max(0, args.radius)
        box = (max(0, x - radius), max(0, y - radius),
               min(rgb.width, x + radius + 1), min(rgb.height, y + radius + 1))
        center = rgb.getpixel((x, y))
        mean = tuple(int(round(v)) for v in ImageStat.Stat(rgb.crop(box)).mean)
        entries.append(
            {
                "x": x,
                "y": y,
                "center": hex_color(center),
                "average": hex_color(mean),
                "average_rgb": list(mean),
            }
        )

    if args.json:
        print(json.dumps({"samples": entries}, indent=2))
    else:
        for entry in entries:
            print(
                f"({entry['x']:>4},{entry['y']:>4})  center {entry['center']}  "
                f"avg {entry['average']}  rgb({entry['average_rgb'][0]}, "
                f"{entry['average_rgb'][1]}, {entry['average_rgb'][2]})"
            )
    return 0


def cmd_grid(args: argparse.Namespace) -> int:
    rgb = load_rgb(args.image).convert("RGBA")
    if args.step < 2:
        raise SystemExit("error: --step must be >= 2")
    overlay = Image.new("RGBA", rgb.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    line = (214, 0, 214, 110)
    for x in range(0, rgb.width, args.step):
        draw.line((x, 0, x, rgb.height), fill=line, width=1)
    for y in range(0, rgb.height, args.step):
        draw.line((0, y, rgb.width, y), fill=line, width=1)

    if args.labels:
        font = ImageFont.load_default()
        for x in range(0, rgb.width, args.step):
            draw.text((x + 3, 2), str(x), fill=(180, 0, 180, 255), font=font)
        for y in range(0, rgb.height, args.step):
            if y == 0:
                continue
            draw.text((2, y + 2), str(y), fill=(180, 0, 180, 255), font=font)

    result = Image.alpha_composite(rgb, overlay).convert("RGB")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    result.save(out)
    print(f"wrote {out} ({rgb.width}x{rgb.height}, step {args.step})")
    return 0


def cmd_crop(args: argparse.Namespace) -> int:
    rgb = load_rgb(args.image)
    try:
        x, y, width, height = (int(v) for v in args.box.split(","))
    except ValueError:
        raise SystemExit("error: --box must be x,y,width,height")
    box = (x, y, x + width, y + height)
    if box[0] < 0 or box[1] < 0 or box[2] > rgb.width or box[3] > rgb.height:
        raise SystemExit(f"error: box {box} outside {rgb.width}x{rgb.height}")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rgb.crop(box).save(out)
    print(f"wrote {out} ({width}x{height} from {x},{y})")
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    reference = load_rgb(args.reference)
    render = load_rgb(args.render)
    if reference.size != render.size:
        raise SystemExit(
            f"error: size mismatch: reference {reference.size}, render {render.size}. "
            "Render at the same CSS viewport and DPR."
        )

    difference = ImageChops.difference(reference, render)
    red, green, blue = difference.split()
    maximum = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    histogram = maximum.histogram()
    total = reference.width * reference.height
    tolerance = max(0, min(255, args.tolerance))

    mismatch = sum(histogram[tolerance + 1:])
    percent = 100.0 * mismatch / total
    mean_error = sum(i * count for i, count in enumerate(histogram)) / total
    mask = maximum.point(lambda value: 255 if value > tolerance else 0)
    bbox = mask.getbbox()

    tiles = []
    columns, rows = 8, 8
    for row in range(rows):
        for column in range(columns):
            left = column * reference.width // columns
            right = (column + 1) * reference.width // columns
            top = row * reference.height // rows
            bottom = (row + 1) * reference.height // rows
            if right <= left or bottom <= top:
                continue
            mean = ImageStat.Stat(maximum.crop((left, top, right, bottom))).mean[0]
            tiles.append(
                {
                    "x": left,
                    "y": top,
                    "w": right - left,
                    "h": bottom - top,
                    "mean_diff": round(mean, 2),
                }
            )
    tiles.sort(key=lambda item: item["mean_diff"], reverse=True)

    if args.out:
        heat = ImageOps.colorize(maximum, black="#FFFFFF", white="#D00000")
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        heat.save(out)

    if args.overlay:
        base = Image.blend(reference, render, 0.5)
        red_layer = Image.new("RGB", base.size, (208, 0, 0))
        overlay = base.copy()
        overlay.paste(red_layer, mask=mask)
        out = Path(args.overlay)
        out.parent.mkdir(parents=True, exist_ok=True)
        overlay.save(out)

    result = {
        "reference": args.reference,
        "render": args.render,
        "size": list(reference.size),
        "tolerance": tolerance,
        "mismatch_pixels": mismatch,
        "mismatch_percent": round(percent, 4),
        "mean_channel_error": round(mean_error, 3),
        "diff_bbox": list(bbox) if bbox else None,
        "worst_tiles": tiles[:6],
        "diff_image": args.out,
        "overlay_image": args.overlay,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"size:             {reference.width} x {reference.height}")
        print(f"tolerance:        {tolerance}/255 max channel")
        print(f"mismatch:         {mismatch} px ({percent:.4f}%)")
        print(f"mean error:       {mean_error:.3f}/255")
        print(f"diff bbox:        {bbox if bbox else 'none'}")
        if args.out:
            print(f"diff image:       {args.out}")
        if args.overlay:
            print(f"overlay image:    {args.overlay}")
        print("worst 8x8 tiles:")
        for tile in tiles[:6]:
            print(
                f"  ({tile['x']:>4},{tile['y']:>4}) {tile['w']:>4}x{tile['h']:<4} "
                f"mean {tile['mean_diff']:>6.2f}"
            )

    if args.fail_over is not None and percent > args.fail_over:
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Measure and diff UI reference images.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    info = subparsers.add_parser("info", help="image size, DPR, and top colors")
    info.add_argument("image")
    info.add_argument("--dpr", type=float, default=1.0, help="device pixel ratio (default 1)")
    info.add_argument("--json", action="store_true")
    info.set_defaults(func=cmd_info)

    palette = subparsers.add_parser("palette", help="dominant colors")
    palette.add_argument("image")
    palette.add_argument("--colors", type=int, default=16)
    palette.add_argument("--json", action="store_true")
    palette.set_defaults(func=cmd_palette)

    sample = subparsers.add_parser("sample", help="sample pixel colors")
    sample.add_argument("image")
    sample.add_argument("--points", action="append", default=[], help='e.g. "24,24;232,64"')
    sample.add_argument("--radius", type=int, default=0, help="average a box of this radius")
    sample.add_argument("--json", action="store_true")
    sample.set_defaults(func=cmd_sample)

    grid = subparsers.add_parser("grid", help="overlay a measurement grid")
    grid.add_argument("image")
    grid.add_argument("--step", type=int, default=100)
    grid.add_argument("--out", required=True)
    grid.add_argument("--labels", action="store_true")
    grid.set_defaults(func=cmd_grid)

    crop = subparsers.add_parser("crop", help="crop a region")
    crop.add_argument("image")
    crop.add_argument("--box", required=True, help="x,y,width,height")
    crop.add_argument("--out", required=True)
    crop.set_defaults(func=cmd_crop)

    diff = subparsers.add_parser("diff", help="compare reference and render")
    diff.add_argument("reference")
    diff.add_argument("render")
    diff.add_argument("--out", help="write a heatmap diff image")
    diff.add_argument("--overlay", help="write a 50/50 overlay with differences in red")
    diff.add_argument("--tolerance", type=int, default=8, help="0-255 max channel difference")
    diff.add_argument("--fail-over", type=float, default=None, help="exit 1 above this mismatch %%")
    diff.add_argument("--json", action="store_true")
    diff.set_defaults(func=cmd_diff)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
