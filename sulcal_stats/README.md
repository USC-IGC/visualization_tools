# Sulcal Stats

Required software
* BrainVISA

Required environmental variable:
* BVHOME 

Example: `BVHOME=/Applications/brainvisa-4.5.0/`

### Setup Procedures

We use a modified version of an existing script, so let's rename the original to keep it around.

`mv $BVHOME/bin/real-bin/siCsvMapGraph.py $BVHOME/bin/real-bin/siCsvMapGraph_old.py`

And then copy this version to the original's previous path.

`cp siCsvMapGraph.py $BVHOME/bin/real-bin/`

Now in order to run it, we should add it to `$PATH`.

`export PATH="${BVHOME}/bin/:$PATH"`

### Running the Script

After running the script as described below, Anatomist (the BrainVISA viewer) starts loading the mapped sulci.

Input Flags:

* `-g` is the graph file, that is the sulci meshes
* `--csv` is a csv file including sulci labels used by brainvisa and  values we want to map for each label, in 2 columns (an example attached)
* `--palette` set the colorbar (I am attaching some example used by BrainVISA)
* `--min` sets the minimum value to map
* `--max` sets the maximum value to map


Example Usage:

`siCsvMapGraph.py -g $BVHOME/share/brainvisa-share-4.5/models/models_2008/descriptive_models/segments/talairach_spam_left/meshes/Lspam_model_meshes_1.arg --palette French --label-attribute 'name' --csv stat.csv --min 0.5 --max 1`

