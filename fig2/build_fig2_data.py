"""Convert the raw BS-RB analysis CSV into tidy per-figure source data.
Source: /Volumes/slab/.../240911/RAM_paper_results/datasets/DualRail_BeamSplitters.csv
Outputs:
  fig2c_beamsplitter_rb_vs_depth.csv  (per mode, per depth)
  fig2e_swap_infidelity.csv           (per mode summary)
Mapping (fit_display.RB_extract...): P00=ee, P01=eg, P10=ge, P11=gg.
Swap infidelity = 1 - fid**1.5 (a swap = 1.5 RB beamsplitter gates).
"""
import ast, numpy as np, pandas as pd
SRC = "/Volumes/slab/Multimode/experiment/240911/RAM_paper_results/datasets/DualRail_BeamSplitters.csv"
df = pd.read_csv(SRC)
def L(s): return np.array(ast.literal_eval(s), dtype=float)

rows = []
for _, r in df.iterrows():
    m = int(r["Mode"])
    depth = L(r["depth_list"])
    fid_raw = L(r["fids_list"]); fid_post = L(r["fids_post_list"])
    eb = L(r["ebars_list"]); ebp = L(r["ebars_post_list"])
    P11 = L(r["gg_list"]); P10 = L(r["ge_list"]); P01 = L(r["eg_list"]); P00 = L(r["ee_list"])
    P11e = L(r["gg_list_err"]); P10e = L(r["ge_list_err"]); P01e = L(r["eg_list_err"]); P00e = L(r["ee_list_err"])
    n = len(depth)
    for i in range(n):
        rows.append(dict(mode=m, depth=int(depth[i]),
            fid_raw=fid_raw[i], fid_raw_err=eb[i],
            fid_post=fid_post[i], fid_post_err=ebp[i],
            P00=P00[i], P00_err=P00e[i], P01=P01[i], P01_err=P01e[i],
            P10=P10[i], P10_err=P10e[i], P11=P11[i], P11_err=P11e[i]))
out_c = pd.DataFrame(rows)
out_c.to_csv("fig2c_beamsplitter_rb_vs_depth.csv", index=False)

# 2e summary
srows = []
for _, r in df.iterrows():
    m = int(r["Mode"]); f = float(r["fid"]); fe = float(r["fid_err"])
    fp = float(r["fid_post"]); fpe = float(r["fid_post_err"])
    infid_raw = 1 - f**1.5; infid_raw_err = 1.5*np.sqrt(f)*fe
    infid_post = 1 - fp**1.5; infid_post_err = 1.5*np.sqrt(fp)*fpe
    srows.append(dict(mode=m, gate_fid_raw=f, gate_fid_raw_err=fe,
        gate_fid_post=fp, gate_fid_post_err=fpe,
        swap_infid_raw_pct=100*infid_raw, swap_infid_raw_err_pct=100*infid_raw_err,
        swap_infid_post_pct=100*infid_post, swap_infid_post_err_pct=100*infid_post_err))
out_e = pd.DataFrame(srows)
out_e.to_csv("fig2e_swap_infidelity.csv", index=False)
print(out_e[["mode","swap_infid_raw_pct","swap_infid_post_pct"]].round(3).to_string(index=False))
print("\nrows in 2c:", len(out_c))
