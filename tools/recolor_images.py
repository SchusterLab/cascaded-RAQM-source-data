"""Raster pass. For each embedded image:
 - if its colors lie along the source colormap (cividis heatmaps + colorbars),
   value-remap onto the warm earthy CMAP (preserving white 'no-data' cells);
 - otherwise hue-remap (earthy) like the vector colors.
Near-neutral pixels (white/black/gray) always pass through.
"""
import sys, numpy as np, fitz
import matplotlib
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb, LinearSegmentedColormap
from scipy.spatial import cKDTree

CIVIDIS = matplotlib.colormaps['cividis'](np.linspace(0, 1, 256))[:, :3]
_TREE = cKDTree(CIVIDIS)
WARM = LinearSegmentedColormap.from_list(
    "raqm_warm", ["#F2E7CE", "#E3B96B", "#C8703A", "#8A3B1E", "#4A1E12"])(np.linspace(0, 1, 256))[:, :3]

def _hue_remap(flat):
    hsv = rgb_to_hsv(flat); h, s, v = hsv[:, 0], hsv[:, 1], hsv[:, 2]
    hd = h * 360.0; th = np.empty_like(h); sc = np.ones_like(h)
    for lo, hi, t, c in [(-1, 35, 16, .95), (35, 70, 40, .95), (70, 100, 75, .85),
                         (100, 185, 159, .9), (185, 255, 209, .9), (255, 320, 266, .85)]:
        m = (hd >= lo) & (hd < hi); th[m] = t; sc[m] = c
    m = hd >= 320; th[m] = 16; sc[m] = .95
    out = hsv_to_rgb(np.stack([th / 360.0, np.minimum(1, s * sc), v], axis=1))
    g = s < 0.12; out[g] = flat[g]
    return out

def remap_image(arr):
    flat = arr.reshape(-1, 3).astype(np.float64) / 255.0
    near_white = (flat > 0.88).all(1)
    color = ~near_white & (flat.max(1) - flat.min(1) > 0.04)
    # cividis test: of the colored pixels, what fraction is near the cividis curve?
    out = flat.copy()
    if color.sum() > 50:
        dist, idx = _TREE.query(flat[color])
        is_cmap = color.copy(); is_cmap[color] = dist < 0.06
        frac = is_cmap[color].mean()
        if frac > 0.7:                       # this image IS a cividis heatmap/colorbar
            d2, i2 = _TREE.query(flat[~near_white])
            t = i2 / 255.0
            out[~near_white] = WARM[(t * 255).round().astype(int)]
            out[near_white] = flat[near_white]
            return (out.reshape(arr.shape) * 255).round().astype(np.uint8)
    # else hue-remap the colored pixels
    out[color] = _hue_remap(flat[color])
    return (out.reshape(arr.shape) * 255).round().astype(np.uint8)

def process(path_in, path_out):
    doc = fitz.open(path_in); done = set()
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in done:
                continue
            done.add(xref)
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 3 or pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            arr = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3]
            new = remap_image(arr)
            newpix = fitz.Pixmap(fitz.csRGB, pix.width, pix.height, np.ascontiguousarray(new).tobytes(), False)
            page.replace_image(xref, pixmap=newpix)
    doc.save(path_out, garbage=4, deflate=True)
    print("wrote", path_out)

if __name__ == "__main__":
    process(sys.argv[1], sys.argv[2])
