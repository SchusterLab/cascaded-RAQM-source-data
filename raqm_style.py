"""
Shared plotting style for the RAQM source-data figures.

A muted, earthy theme (cream background; terracotta, teal, slate-blue, gold)
inspired by the companion architecture paper, as an alternative to the
brighter palette used in the published figures.

Usage in a plot script:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import raqm_style as rs
    rs.apply()
    ... rs.PALETTE["rust"] ... rs.sequential(7, "teal") ... cmap=rs.CMAP ...
"""
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, to_rgb
import numpy as np

# ---- core palette -------------------------------------------------------- #
CREAM = "#F7F3E9"
INK = "#2E2A25"
PALETTE = {
    "rust":   "#B8532F",
    "teal":   "#3C8A6E",
    "slate":  "#4E6E8E",
    "gold":   "#D9A23B",
    "purple": "#8A6FA8",
    "olive":  "#8C8A3F",
    "ink":    INK,
    "cream":  CREAM,
}
# light/dark anchors for building sequential ramps within a family
_ANCHORS = {
    "rust":  ("#E8C4A8", "#7E3620"),
    "teal":  ("#A9D2C2", "#1F5544"),
    "slate": ("#AFC2D2", "#2C4258"),
    "gold":  ("#F0DBA6", "#9A6B14"),
    "purple":("#CBBBDD", "#553F71"),
}

def sequential(n, hue="teal"):
    """n colors from light to dark within a single earthy family."""
    lo, hi = _ANCHORS[hue]
    cm = LinearSegmentedColormap.from_list(hue, [lo, hi])
    return [cm(t) for t in np.linspace(0.15, 0.95, n)]

def categorical(keys=None):
    """A categorical earthy sequence."""
    order = keys or ["teal", "rust", "slate", "gold", "purple", "olive"]
    return [PALETTE[k] for k in order]

# warm sequential colormap for heatmaps (cream -> gold -> terracotta -> brown)
CMAP = LinearSegmentedColormap.from_list(
    "raqm_warm", ["#F2E7CE", "#E3B96B", "#C8703A", "#8A3B1E", "#4A1E12"])
CMAP.set_bad(CREAM)   # masked cells render as background cream

def apply():
    mpl.rcParams.update({
        "figure.facecolor": CREAM,
        "axes.facecolor": CREAM,
        "savefig.facecolor": CREAM,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.prop_cycle": mpl.cycler(color=categorical()),
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 11,
        "legend.frameon": False,
    })
