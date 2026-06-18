"""Recolor a vector PDF into the RAQM earthy palette by hue-remapping every
DeviceRGB color while preserving saturation/value (so lightness, sequential
shading, fonts, ticks, geometry are untouched). Grays/blacks/whites pass through.
"""
import sys, re, colorsys
import pikepdf

# target hues (deg) for the earthy palette, by source hue family
#   rust ~16, gold ~40, teal ~159, slate ~209, purple ~266
def remap_rgb(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < 0.12:                      # gray/black/white -> unchanged
        return None
    hd = h * 360.0
    if hd < 35 or hd >= 320:          # reds / salmons / magenta-red
        th, sscale = 16, 0.95
    elif hd < 70:                     # yellow / gold
        th, sscale = 40, 0.95
    elif hd < 100:                    # yellow-green / lime
        th, sscale = 75, 0.85         # olive
    elif hd < 185:                    # green / teal / cyan
        th, sscale = 159, 0.9
    elif hd < 255:                    # blue
        th, sscale = 209, 0.9
    else:                             # purple / violet
        th, sscale = 266, 0.85
    nr, ng, nb = colorsys.hsv_to_rgb(th / 360.0, min(1.0, s * sscale), v)
    return nr, ng, nb

_NUM = r'(-?\d*\.?\d+)'
_PAT = re.compile((r'%s\s+%s\s+%s\s+(rg|RG)' % (_NUM, _NUM, _NUM)).encode())

def _sub(m):
    r, g, b = float(m.group(1)), float(m.group(2)), float(m.group(3))
    op = m.group(4)
    out = remap_rgb(r, g, b)
    if out is None:
        return m.group(0)
    return ("%.4f %.4f %.4f " % out).encode() + op

def recolor_stream(obj):
    try:
        raw = obj.read_bytes()
    except Exception:
        return
    new = _PAT.sub(_sub, raw)
    if new != raw:
        obj.write(new)

def process(path_in, path_out):
    pdf = pikepdf.open(path_in)
    seen = set()
    def walk_forms(resources):
        xo = resources.get('/XObject', None)
        if xo is None:
            return
        for name, form in xo.items():
            if form.objgen in seen:
                continue
            seen.add(form.objgen)
            if form.get('/Subtype') == '/Form':
                recolor_stream(form)
                r = form.get('/Resources', None)
                if r is not None:
                    walk_forms(r)
    for page in pdf.pages:
        c = page.obj.get('/Contents')
        if isinstance(c, pikepdf.Array):
            for s in c:
                recolor_stream(s)
        elif c is not None:
            recolor_stream(c)
        res = page.obj.get('/Resources')
        if res is not None:
            walk_forms(res)
    pdf.save(path_out)
    print("wrote", path_out)

if __name__ == "__main__":
    process(sys.argv[1], sys.argv[2])
