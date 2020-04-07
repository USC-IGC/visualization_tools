# Cortical Surfaces

These tools are provided to create figures reflecting the relevant study statistics on cortical surfaces.

### MATLAB

For some mythical reason, the `add_path` command doesn't always work. If you get the following error, use the GUI to add the path *othercolor* directory with subdirectories. 

```
Undefined function or variable 'othercolor'.

Error in map_corticalResults_inFS_ROIs_2panel_2hemi (line 135)
    colormap(othercolor('Reds9'));
```

### Python

Required packages: 
* nibabel
* plotly

Required environmental variable:
* FREESURFER_HOME

Usage: `stat_brain_surface.py -s {left,right,l,r} -r ROI_FILE
                             -p OUT_PREFIX [-a ATLAS]`

`stat_brain_surface.py` takes in a either a vertex_file (mgh) OR roi_file (xls, xlsx, csv,
tsv, txt) and maps the statistics to the cortical surface. For ROI files, one HTML file will be output
per statistic column.

required arguments:
* `-s {left,right,l,r}, --hemisphere {left,right,l,r}`
                        Hemisphere to render
* `-v VERTEX_FILE, --vertex_file VERTEX_FILE`
                        FreeSurfer mgh file with vertex-associated statistic.

* `-r ROI_FILE, --roi_file ROI_FILE`
                        file with regions of interest and associated
                        statistic(s). Column headers should be ROI for the
                        regions of interest column and statistic name for the
                        rest (e.g., p-value). Please DO NOT include spaces or
                        special characters in column headers.
* `-p OUT_PREFIX, --out_prefix OUT_PREFIX`
                        Output prefix for the name of HTML file(s) to output

optional arguments:
* `-h, --help`            show this help message and exit
* `-a ATLAS, --atlas ATLAS`
                        Atlas to use for ROI parcellation. Default:
                        aparc
* `-c COLORMAP, --colormap COLORMAP`
                        (Optional) Colormap. Default: YlOrRd
* `--cmin CMIN [CMIN ...]`
                        (Optional) Colormap minimum, provide one per stat
* `--cmax CMAX [CMAX ...]`
                        (Optional) Colormap maximum, provide one per stat


### R

TBA
