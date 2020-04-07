#!/usr/bin/env python
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
# import colorlover as cl
import nibabel as nib
import argparse
import sys
import os

### OKAY, LET'S GET STARTED

parser = argparse.ArgumentParser(description="stat_brain_surface.py takes in a spreadsheet or text file (xls, xlsx, csv, tsv, txt) and maps the statistics to the cortical surface. Please provide either a vertex_file OR roi_file but NOT BOTH. One HTML file will be output per statistic column.")
parser.add_argument("-s", "--hemisphere", help="Hemisphere to render", choices=["left", "right", "l", "r"])
parser.add_argument("-v", "--vertex_file", help="FreeSurfer mgh file with vertex-associated statistic.")
# parser.add_argument("-v", "--vertex_file", help="file with vertex coordinates and associated statistic(s). The first three columns will be assumed to be the x, y, and z coordinates of the vertex, and following columns will be considered as statistics. Please DO NOT include spaces or special characters in column headers.")
parser.add_argument("-r", "--roi_file", help="file with regions of interest and associated statistic(s). Column headers should be ROI for the regions of interest column and statistic name for the rest (e.g., p-value). Please DO NOT include spaces or special characters in column headers.")
parser.add_argument("-p", "--out_prefix", help="Output prefix for the name of HTML file(s) to output")
parser.add_argument("-a", "--atlas", help="(Optional) Atlas to use for ROI parcellation. Default: aparc", default="aparc")
parser.add_argument("-c", "--colormap", help="(Optional) Colormap. Default: YlOrRd", default="YlOrRd")
parser.add_argument("--cmin", nargs="+", help="(Optional) Colormap minimum, provide one per stat", type=float)
parser.add_argument("--cmax", nargs="+", help="(Optional) Colormap maximum, provide one per stat", type=float)
args = parser.parse_args()
# plotly colorscale options: Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis

### CHECK ENVIRONMENTAL VARIABLE(S)

if "FREESURFER_HOME" not in os.environ.keys():
    print("\nPlease make sure that the environmental variable FREESURFER_HOME is set\n")
    sys.exit(1)

### DEFINE FUNCTIONS

def vertex_color(labels, stat, df):
    vertex_colors = []
    for label in labels:
        if label == 0:
            vertex_colors.append(0)
        else:
            roi = labelix2name[label]
            vertex_colors.append(df.loc[roi, stat])
            
    return vertex_colors

def add_buttons(figure, axes, hemisphere):
    if hemisphere == 'rh':
        buttons = [
                    dict(label="Lateral",
                         method="relayout",
                         args=["scene", dict(camera=dict(eye=dict(x=2.5, y=0, z=0)),
                                             xaxis=axes,
                                             yaxis=axes,
                                             zaxis=axes)
                              ]),
                    dict(label="Medial",
                         method="relayout",
                         args=["scene", dict(camera=dict(eye=dict(x=-2.5, y=0, z=0)),
                                             xaxis=axes,
                                             yaxis=axes,
                                             zaxis=axes)
                              ])
                  ]
    else:
        buttons = [
                    dict(label="Lateral",
                         method="relayout",
                         args=["scene", dict(camera=dict(eye=dict(x=-2.5, y=0, z=0)),
                                             xaxis=axes,
                                             yaxis=axes,
                                             zaxis=axes)
                              ]),
                    dict(label="Medial",
                         method="relayout",
                         args=["scene", dict(camera=dict(eye=dict(x=2.5, y=0, z=0)),
                                             xaxis=axes,
                                             yaxis=axes,
                                             zaxis=axes)
                              ])
                    ]

    buttons += [
                dict(label="Dorsal",
                     method="relayout",
                     args=["scene", dict(camera=dict(eye=dict(x=0, y=0, z=2.5)),
                                             xaxis=axes,
                                             yaxis=axes,
                                             zaxis=axes)]),
                dict(label="Ventral",
                     method="relayout",
                     args=["scene", dict(camera=dict(eye=dict(x=0, y=0, z=-2.5)),
                                             xaxis=axes,
                                             yaxis=axes,
                                             zaxis=axes)]),
                dict(label="Rostral",
                     method="relayout",
                     args=["scene", dict(camera=dict(eye=dict(x=0, y=2.5, z=0)),
                                             xaxis=axes,
                                             yaxis=axes,
                                             zaxis=axes)]),
                dict(label="Caudal",
                     method="relayout",
                     args=["scene", dict(camera=dict(eye=dict(x=0, y=-2.5, z=0)),
                                             xaxis=axes,
                                             yaxis=axes,
                                             zaxis=axes)])
               ]

    figure.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                buttons=buttons,
            )
        ]
    )
    return figure

### PARSE INPUTS/SETUP VARIABLES

if args.vertex_file and args.roi_file:
    print("\nPlease provide EITHER a vertex_file OR an roi_file\n")
    sys.exit(1)

if args.hemisphere in ["r", "right"]:
    hemi = "rh"
elif args.hemisphere in ["l", "left"]:
    hemi = "lh"

coords, faces = nib.freesurfer.io.read_geometry(os.path.join(os.environ["FREESURFER_HOME"], "subjects/fsaverage/surf/{hemi}.pial".format(hemi=hemi)))
labels, ctab, labnames = nib.freesurfer.io.read_annot(os.path.join(os.environ["FREESURFER_HOME"], "subjects/fsaverage/label/{hemi}.{parc}.annot".format(hemi=hemi, parc=args.atlas)))

if isinstance(labnames[0][0], int):
    labnames = [ll.decode("ASCII") for ll in labnames]

hoverlabels = [labnames[ll] for ll in labels]
ctab[0,:3] = 128 # Set unknown to gray instead of black

### RENDER BRAIN SURFACE

background = [go.Mesh3d(x=coords[:,0], y=coords[:,1], z=coords[:,2],
                        i=faces[:,0], j=faces[:,1], k=faces[:,2],
                        text=hoverlabels,
                        hoverinfo='text',
                        hoverlabel={'bgcolor': "white"},
                        color="#C0C0C0"
                        )]

axes_settings = dict(
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

layout_scene = dict(
    xaxis=axes_settings,
    yaxis=axes_settings,
    zaxis=axes_settings
    )

layout = go.Layout(
    width=1000,
    height=1000,
    scene=layout_scene
)

if args.vertex_file:
    mgh_file = nib.load(args.vertex_file)
    vertex_colors = mgh_file.get_data()[:,0,0]
    data = [go.Mesh3d(x=coords[:, 0], y=coords[:, 1], z=coords[:, 2], 
                      i=faces[:, 0], j=faces[:, 1], k=faces[:, 2], 
                      text=hoverlabels,
                      hoverinfo='text',
                      intensity=vertex_colors,
                      colorscale=args.colormap,
                      colorbar={'tickmode': 'auto',
                                'nticks': 10}
                     )]
    fig = go.Figure(data=data, layout=layout)
    if len(args.cmin) > 0:
        fig.data[0].update(cmin=args.cmin[0])
    if len(args.cmax) > 0:
        fig.data[0].update(cmax=args.cmax[0])
    fn = "_".join([args.out_prefix, hemi, args.atlas+".html"])
    fig = add_buttons(fig, axes_settings, hemi)
    py.plot(fig, filename=fn, auto_open=False)


if args.roi_file:

    if args.roi_file.endswith(".csv"):
        df = pd.read_csv(args.roi_file, index_col="ROI")
    elif args.roi_file.endswith(".xls") or args.roi_file.endswith(".xlsx"):
        df = pd.read_excel(args.roi_file, index_col="ROI")
    else:
        df = pd.read_csv(args.roi_file, index_col="ROI", delimiter='\s+')

    labelix2name = {}
    for roi in df.index:
        if roi in labnames:
            labelix2name[labnames.index(roi)] = roi

    vertices_to_keep = []
    for i, label in enumerate(labels):
        if label in list(labelix2name.keys()):
            vertices_to_keep.append(i)

    faces_to_keep = faces[np.all(np.isin(faces, vertices_to_keep), axis=1), :] 
    for ix, v in enumerate(vertices_to_keep):
        faces_to_keep[faces_to_keep == v] = -ix
    faces_to_keep = -faces_to_keep

    for ix, stat in enumerate(df.columns):
        vertex_colors = vertex_color(labels[vertices_to_keep], stat, df)
        data = [go.Mesh3d(x=coords[vertices_to_keep, 0], y=coords[vertices_to_keep, 1], z=coords[vertices_to_keep, 2], 
                          i=faces_to_keep[:, 0], j=faces_to_keep[:, 1], k=faces_to_keep[:, 2], 
                          text=[hoverlabels[v] for v in vertices_to_keep],
                          hoverinfo='text',
                          intensity=vertex_colors,
                          colorscale=args.colormap,
                          colorbar={'title': stat,
                                    'tickmode': 'auto',
                                    'nticks': 10}
                         )]

        fig = go.Figure(data=background+data, layout=layout)
        fig.update_layout(title=stat)
        if len(args.cmin) > 0:
            fig.data[1].update(cmin=args.cmin[ix])
        if len(args.cmax) > 0:
            fig.data[1].update(cmax=args.cmax[ix])
        fn = "_".join([args.out_prefix, hemi, args.atlas, stat+".html"])
        fig = add_buttons(fig, axes_settings, hemi)
        py.plot(fig, filename=fn, auto_open=False)
        # fig.write_image(output_path) # maybe with inputs: width=600, height=350, scale=2
        print("\nCreated {}\n".format(fn)) 
