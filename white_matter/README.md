# White Matter

### JHU ROIs

Written in python

Required package:
* nibabel

`JHU_rois.py` takes in a spreadsheet (xls, xlsx, csv) and maps the statistics to
JHU regions of interest (ROIs). Please ensure that ROI names match the JHU
lookup table

Usage: `JHU_rois.py -infile INFILE -outpref OUTPREF [-jhu_lut JHU_LUT] [-jhu_nii JHU_NII]`
                   
required arguments:
* `-infile INFILE`    CSV or excel file with JHU regions of interest and
                    associated statistic(s). Column headers should be ROI for
                    the regions of interest column and statistic name for the
                    rest (e.g., p-value). Bilaterally averaged ROIs can be
                    given in a single row without the -R/-L suffixes. Please
                    DO NOT include spaces or special characters in column
                    headers.
* `-outpref OUTPREF`  Prefixes for output niftis of JHU ROIs filled with
                    statistics

optional arguments:
* `-h, --help`        show this help message and exit
* `-jhu_lut JHU_LUT`  Path to JHU LUT; Default:
                    ENIGMA_look_up_table.txt
* `-jhu_nii JHU_NII`  Path to JHU nifti, e.g., JHU-WhiteMatter-
                    labels-1mm.nii.gz

