#!/usr/bin/env python 
import sys
import nibabel as nib
# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description="JHU_rois.py takes in a spreadsheet (xls, xlsx, csv) and maps the statistics to JHU regions of interest (ROIs). Please ensure that ROI names match the JHU lookup table")
parser.add_argument("-infile", help="CSV or excel file with JHU regions of interest and associated statistic(s). Column headers should be ROI for the regions of interest column and statistic name for the rest (e.g., p-value). Bilaterally averaged ROIs can be given in a single row without the -R/-L suffixes. Please DO NOT include spaces or special characters in column headers.")
parser.add_argument("-jhu_lut", help="(optional) Path to JHU LUT; Default: ENIGMA_look_up_table.txt", default="enigma")
parser.add_argument("-jhu_nii", help="(optional) Path to JHU nifti, e.g., JHU-WhiteMatter-labels-1mm.nii.gz", default="script_path")
# parser.add_argument("-template", help="Path to FA template file")
parser.add_argument("-outpref", help="Prefixes for output niftis of JHU ROIs filled with statistics")
args = parser.parse_args()

try:
    if args.infile.endswith(".csv"):
        ef = pd.read_csv(args.infile, index_col="ROI")
    elif args.infile.endswith(".xls") or args.infile.endswith(".xlsx"):
        ef = pd.read_excel(args.infile, index_col="ROI")
    else:
        print("Invalid --infile type given")
        sys.exit(1)
except ValueError:
        print("--infile input doesn't have an ROI column. Please check input again before re-running.")
        sys.exit(1)

jhu = {}

if args.jhu_lut == "enigma":
    jhu_lut = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "ENIGMA_look_up_table.txt")
else:
    jhu_lut = args.jhu_lut

with open(jhu_lut, "r") as f:
    lines = [l.strip() for l in f.readlines()]
    for l in lines:
        if len(l) > 2:
            jhu[l.split()[1]] = {"ROI": int(l.split()[0])}
            
jhu_dict = pd.DataFrame.from_dict(jhu, orient="index")

if args.jhu_nii == "script_path":
    jhu_nii = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "JHU-WhiteMatter-labels-1mm.nii.gz")
else:
    jhu_nii = args.jhu_nii

if not os.path.exists(jhu_nii):
    print("Cannot find JHU nifti path. Please include one with -jhu_nii or check the input path")
    sys.exit(1)
if not os.path.exists(jhu_lut):
    print("Cannot find JHU lookup table. Please include one with -jhu_lut or check the input path")
    sys.exit(1)

jhu = nib.load(jhu_nii)
jhu_img = jhu.get_data()
jhu_affine = jhu.affine

out_data = {}
for c in ef.columns:
    out_data[c] = np.zeros_like(jhu_img).astype(float)

for i, row in ef.iterrows():
    if i == "FXST":
        i = "FX/ST"
    if i in jhu_dict.index:
        vals = [jhu_dict.loc[i, "ROI"]]
    else:
        if i+"-R" in jhu_dict.index:
            vals = list(jhu_dict.loc[[i+"-R", i+"-L"], "ROI"])
        else:
            print("Warning: %s is not a valid ROI name\n" %i)
            continue
    for c in ef.columns:
        for v in vals:
            out_data[c][jhu_img == v] = row[c]


for k, v in out_data.items():
    nib.save(nib.Nifti1Image(v, jhu_affine), args.outpref+"_"+k.replace(" ", "_")+".nii.gz")


### BELOW IS TO CREATE 2D SLICE IMAGES INSTEAD OF 3D NIFTIS

# mni_fa = nib.load(args.template).get_data()
# 
# # In[61]:
# 
# jhu_fa = np.zeros_like(jhu_img)
# jhu_fa = jhu_fa.astype(float)
# 
# for i, row in ef.iterrows():
#     if i == "AverageFA":
#         continue
#     if i == "FXST":
#         i = "FX/ST"
#     if i in jhu_dict.index:
#         vals = [jhu_dict.loc[i, "ROI"]]
#     else:
#         if i+"-R" in jhu_dict.index:
#             vals = list(jhu_dict.loc[[i+"-R", i+"-L"], "ROI"])
#         else:
#             print(i, row["FDR P-value"])
#             continue
#     if row["FDR P-value"] < 0.05:
#         for v in vals:
#             jhu_fa[jhu_img == v] = row["Cohen's d"]
# 
# 
# # In[83]:
# 
# jhu_md = np.zeros_like(jhu_img)
# jhu_md = jhu_md.astype(float)
# 
# for i, row in md_adults.iterrows():
#     if i == "FXST":
#         i = "FX/ST"
#     if i in jhu_dict.index:
#         vals = [jhu_dict.loc[i, "ROI"]]
#     else:
#         if i+"-R" in jhu_dict.index:
#             vals = list(jhu_dict.loc[[i+"-R", i+"-L"], "ROI"])
#         else:
#             print(i, row["FDR P-value"])
#             continue
#     if row["FDR P-value"] < 0.05:
#         for v in vals:
#             jhu_md[jhu_img == v] = row["Cohen's d"]
# 
# 
# # In[84]:
# 
# jhu_rd = np.zeros_like(jhu_img)
# jhu_rd = jhu_rd.astype(float)
# 
# for i, row in rd_adults.iterrows():
#     if i == "FXST":
#         i = "FX/ST"
#     if i in jhu_dict.index:
#         vals = [jhu_dict.loc[i, "ROI"]]
#     else:
#         if i+"-R" in jhu_dict.index:
#             vals = list(jhu_dict.loc[[i+"-R", i+"-L"], "ROI"])
#         else:
#             print(i, row["FDR P-value"])
#             continue
#     if row["FDR P-value"] < 0.05:
#         for v in vals:
#             jhu_rd[jhu_img == v] = row["Cohen's d"]
# 
# 
# # In[85]:
# 
# jhu_ad = np.zeros_like(jhu_img)
# jhu_ad = jhu_ad.astype(float)
# 
# for i, row in ad_adults.iterrows():
#     if i == "FXST":
#         i = "FX/ST"
#     if i in jhu_dict.index:
#         vals = [jhu_dict.loc[i, "ROI"]]
#     else:
#         if i+"-R" in jhu_dict.index:
#             vals = list(jhu_dict.loc[[i+"-R", i+"-L"], "ROI"])
#         else:
#             print(i, row["FDR P-value"])
#             continue
#     if row["FDR P-value"] < 0.05:
#         for v in vals:
#             jhu_ad[jhu_img == v] = row["Cohen's d"]
# 
# 
# # In[141]:
# 
# rd_adults.loc[rd_adults["FDR P-value"] < 0.05]
# 
# 
# # In[131]:
# 
# fig, axes = plt.subplots(10, 4, figsize=(20,60))
# ax = axes.ravel()
# metrics = ["FA", "MD", "RD", "AD"]
# for i, m in enumerate([jhu_fa, jhu_md, jhu_rd, jhu_ad]):
#     ax[i].imshow(np.rollaxis(mni_fa[:,:,60], 1), origin="lower", cmap="gray")
#     ax[i+4].imshow(np.rollaxis(mni_fa[:,:,65], 1), origin="lower", cmap="gray")
#     ax[i+8].imshow(np.rollaxis(mni_fa[:,:,70], 1), origin="lower", cmap="gray")
#     ax[i+12].imshow(np.rollaxis(mni_fa[:,:,75], 1), origin="lower", cmap="gray")
#     ax[i+16].imshow(np.rollaxis(mni_fa[:,:,80], 1), origin="lower", cmap="gray")
#     ax[i+20].imshow(np.rollaxis(mni_fa[:,:,85], 1), origin="lower", cmap="gray")
#     ax[i+24].imshow(np.rollaxis(mni_fa[:,:,90], 1), origin="lower", cmap="gray")
#     ax[i+28].imshow(np.rollaxis(mni_fa[:,:,95], 1), origin="lower", cmap="gray")
#     ax[i+32].imshow(np.rollaxis(mni_fa[:,:,100], 1), origin="lower", cmap="gray")
#     ax[i+36].imshow(np.rollaxis(mni_fa[:,:,105], 1), origin="lower", cmap="gray")
#     m[m == 0] = np.nan
#     m *= -1
#     ax[i].imshow(np.rollaxis(m[:,:,60], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[i].set_title(metrics[i])
#     ax[4+i].imshow(np.rollaxis(m[:,:,65], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[8+i].imshow(np.rollaxis(m[:,:,70], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[12+i].imshow(np.rollaxis(m[:,:,75], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[16+i].imshow(np.rollaxis(m[:,:,80], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[20+i].imshow(np.rollaxis(m[:,:,85], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[24+i].imshow(np.rollaxis(m[:,:,90], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[28+i].imshow(np.rollaxis(m[:,:,95], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[32+i].imshow(np.rollaxis(m[:,:,100], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     ax[36+i].imshow(np.rollaxis(m[:,:,105], 1), origin="lower", vmin=-0.3, vmax=0.3, cmap="RdBu")
#     
# for a in ax:
#     a.axis('off')
# 
# plt.tight_layout()    
# fig.colorbar(high, ax=ax.tolist(), shrink=0.5)
# plt.savefig("2s_slices_axial_fa_many.png")
# plt.show()
