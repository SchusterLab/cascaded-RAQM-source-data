"""Fig 4a source data: cross-Kerr matrix (kHz) between RAQM modes.
Source: 240911/RAM_paper_results/datasets/QubitBufferStorage_cross_kerr.csv
(identical to Supplementary Table 3). Row/col index order:
0:Q 1:C 2:B1 3:B2 4:S1 5:S2 6:S3 7:S4 8:S5 9:S6 10:S7 11:R
Diagonal = self-Kerr; off-diagonal = cross-Kerr. Lower triangle is measured.
"""
import pandas as pd, numpy as np
SRC="/Volumes/slab/Multimode/experiment/240911/RAM_paper_results/datasets/QubitBufferStorage_cross_kerr.csv"
labels=["Q","C","B1","B2","S1","S2","S3","S4","S5","S6","S7","R"]
M=pd.read_csv(SRC, header=0).values.astype(float)   # 12x12
df=pd.DataFrame(M, index=labels, columns=labels)
df.to_csv("fig4a_cross_kerr_matrix_kHz.csv")
print(df.round(3).to_string())
