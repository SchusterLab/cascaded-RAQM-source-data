# Recolored paper figures (earthy theme)

Vector PDFs of the four main paper figures, recolored into the earthy palette
while leaving **everything else byte-for-byte identical** — fonts (ArialMT, as
recommended by Nature), font sizes, tick marks, panel sizing, geometry, and the
schematic/circuit artwork are untouched.

| File | Paper figure |
|---|---|
| `fig1_earthy.pdf` | Fig 1 — architecture, device, frequency/coherence |
| `fig2_earthy.pdf` | Fig 2 — single-mode access (traces, RB, swap infidelity) |
| `fig3_earthy.pdf` | Fig 3 — RAQM operation (RB vs accesses, infidelity vs size) |
| `fig4_earthy.pdf` | Fig 4 — crosstalk (cross-Kerr, access error, dephasing, budget) |

## How they were made (`../tools/`)

Two passes operate directly on the source PDFs (originals in `~/Downloads`):

1. `recolor.py` — rewrites every DeviceRGB vector color operator. Each color is
   hue-remapped into the earthy palette (rust / gold / olive / teal / slate /
   purple) while **preserving its saturation and value**, so light↔dark
   sequential shading and 3D schematic shading are kept. Near-neutral colors
   (black text, gray axes, white) pass through unchanged.
2. `recolor_images.py` — recolors embedded raster images. Heatmaps drawn with
   the `cividis` colormap are value-remapped onto a warm earthy colormap
   (cream→terracotta→brown); white "no-data" cells stay white. Any other colored
   raster is hue-remapped like the vector colors.

Regenerate, e.g.:
```bash
python tools/recolor.py in.pdf tmp.pdf && python tools/recolor_images.py tmp.pdf out.pdf
```

The palette matches `../raqm_style.py` used for the standalone per-panel scripts.
