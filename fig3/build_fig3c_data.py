"""Fig 3c source data: random read infidelity vs RAQM size.
Source: 240911/RAM_paper_results/datasets/all_rbam.csv
Each config (row) has a list of per-mode random-read fidelities (rbam_fidelities)
and their errors. RAQM size = number of modes in the config.
"""
import pandas as pd, numpy as np, re
SRC="/Volumes/slab/Multimode/experiment/240911/RAM_paper_results/datasets/all_rbam.csv"
df=pd.read_csv(SRC)
def pf(s): return [float(x) for x in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', str(s))]
def pi(s): return [int(x) for x in re.findall(r'\d+', str(s))]
rows=[]
for ci,(_,r) in enumerate(df.iterrows()):
    modes=pi(r['mode_list']); fids=pf(r['rbam_fidelities']); errs=pf(r['rbam_fidelity_errs'])
    size=len(modes)
    for m,f,e in zip(modes,fids,errs):
        rows.append(dict(raqm_size=size, config_id=ci, mode=m,
            random_read_fidelity=f, random_read_fidelity_err=e,
            infidelity=1-f, infidelity_err=e))
out=pd.DataFrame(rows)
out.to_csv("fig3c_random_read_infidelity.csv", index=False)
print(out.groupby('raqm_size')['infidelity'].agg(['count','mean']).round(4))
