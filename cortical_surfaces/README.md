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

**stat_brain_surface.py**

Required packages: 
* nibabel
* plotly

Required environmental variable:
* FREESURFER_HOME

### R

TBA
