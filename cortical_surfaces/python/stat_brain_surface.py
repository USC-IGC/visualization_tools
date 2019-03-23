#!/usr/bin/env python
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import colorlover as cl
import nibabel as nib
import argparse
import sys
import os

### OKAY, LET'S GET STARTED

parser = argparse.ArgumentParser(description="stat_brain_surface.py takes in a spreadsheet or text file (xls, xlsx, csv, tsv, txt) and maps the statistics to the cortical surface. Please provide either a vertex_file OR roi_file but NOT BOTH. One HTML file will be output per statistic column.")
parser.add_argument("-s", "--hemisphere", help="Hemisphere to render", choices=["left", "right", "l", "r"])
# parser.add_argument("-v", "--vertex_file", help="file with vertex coordinates and associated statistic(s). The first three columns will be assumed to be the x, y, and z coordinates of the vertex, and following columns will be considered as statistics. Please DO NOT include spaces or special characters in column headers.")
parser.add_argument("-r", "--roi_file", help="file with regions of interest and associated statistic(s). Column headers should be ROI for the regions of interest column and statistic name for the rest (e.g., p-value). Please DO NOT include spaces or special characters in column headers.")
parser.add_argument("-p", "--out_prefix", help="Output prefix for the name of HTML file(s) to output")
parser.add_argument("-a", "--atlas", help="(Optional) Atlas to use for ROI parcellation. Default: aparc", default="aparc")
args = parser.parse_args()

### DEFINE FUNCTIONS

# plotly colorscale options: Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis
# may need to set marker.line.cmin/cmax and colorbar.tick*

def vertex_color(labels, stat, df):
    vertex_colors = []
    for label in labels:
        if label == 0:
            vertex_colors.append(0)
        else:
            roi = labelix2name[label]
            vertex_colors.append(df.loc[roi, stat])
            
    return vertex_colors

### PARSE INPUTS/SETUP VARIABLES

# if args.vertex_file:
#     stat_file = args.vertex_file 
# elif args.roi_file:
#     stat_file = args.roi_file
stat_file = args.roi_file

if stat_file.endswith(".csv"):
    df = pd.read_csv(stat_file, index_col="ROI")
elif stat_file.endswith(".xls") or stat_file.endswith(".xlsx"):
    df = pd.read_excel(stat_file, index_col="ROI")
else:
    df = pd.read_csv(stat_file, index_col="ROI", delim_whitespace=True)

stats = df.columns

if args.hemisphere in ["r", "right"]:
    hemi = "rh"
elif args.hemisphere in ["l", "left"]:
    hemi = "lh"

if "FREESURFER_HOME" not in os.environ.keys():
    print("\nPlease make sure that the environmental variable FREESURFER_HOME is set\n")
    sys.exit(1)

coords, faces = nib.freesurfer.io.read_geometry(os.path.join(os.environ["FREESURFER_HOME"], "subjects/fsaverage/surf/{hemi}.pial".format(hemi=hemi)))
labels, ctab, labnames = nib.freesurfer.io.read_annot(os.path.join(os.environ["FREESURFER_HOME"], "subjects/fsaverage/label/{hemi}.{parc}.annot".format(hemi=hemi, parc=args.atlas)))

if isinstance(labnames[0][0], int):
    labnames = [ll.decode("ASCII") for ll in labnames]

hoverlabels = [labnames[ll] for ll in labels]
ctab[0,:3] = 128 # Set unknown to gray instead of black

### RENDER BRAIN SURFACE

for stat in stats:
    data = [go.Mesh3d(x=coords[:,0], y=coords[:,1], z=coords[:,2],
                      i=faces[:,0], j=faces[:,1], k=faces[:,2],
                      text=hoverlabels,
                      hoverinfo='text',
                      hoverlabel={'bgcolor': "white"},
                      color="#C0C0C0"
                      # facecolor=annot,
                      # intensity=vertex_colors,
                      # colorscale="YlOrRd",
                      # colorbar={'title': stat,
                      #           'tickmode': 'auto',
                      #           'nticks': 5}
                      )]

    # if args.vertex_file:
    #     annot = ['rgb({},{},{})'.format(*vertex_color(v1,v2,v3)) for v1,v2,v3 in faces]
    # elif args.roi_file:
    if args.roi_file:
        labelix2name = {}
        for roi in df.index:
            if roi in labnames:
                labelix2name[labnames.index(roi)] = roi

        # for label in set(labels):
        #     if label not in list(labelix2name.keys()):
        #         labels[labels == label] = 0
        vertices_to_keep = []
        for i, label in enumerate(labels):
            if label in list(labelix2name.keys()):
                vertices_to_keep.append(i)

        faces_to_keep = faces[np.all(np.isin(faces, vertices_to_keep), axis=1), :] 
        for i, v in enumerate(vertices_to_keep):
            faces_to_keep[faces_to_keep == v] = -i
        faces_to_keep = -faces_to_keep

        # annot = [parc_color(v1,v2,v3,stat,ctab,labels) for v1,v2,v3 in faces]
        vertex_colors = vertex_color(labels[vertices_to_keep], stat, df)
        data += [go.Mesh3d(x=coords[vertices_to_keep, 0], y=coords[vertices_to_keep, 1], z=coords[vertices_to_keep, 2], 
                           i=faces_to_keep[:, 0], j=faces_to_keep[:, 1], k=faces_to_keep[:, 2], 
                           text=[hoverlabels[v] for v in vertices_to_keep],
                           hoverinfo='text',
                           intensity=vertex_colors,
                           colorscale="YlOrRd",
                           colorbar={'title': stat,
                                     'tickmode': 'auto',
                                     'nticks': 10}
                          )]

    layout = go.Layout(
        title=stat,
        width=1000,
        height=1000,
        scene=dict(
            xaxis=dict(
                showbackground=False,
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                # showspikes=False,
                title="",
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                showbackground=False,
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                # showspikes=False,
                title="",
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                backgroundcolor='rgb(230, 230,230)'
            ),
            zaxis=dict(
                showbackground=False,
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                # showspikes=False,
                title="",
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                backgroundcolor='rgb(230, 230,230)'
            )
        )
    )

    fig = go.Figure(data=data, layout=layout)
    fn = "_".join([args.out_prefix, hemi, args.atlas, stat+".html"])
    py.plot(fig, filename=fn, auto_open=False)
    print("\nCreated {}\n".format(fn)) 
