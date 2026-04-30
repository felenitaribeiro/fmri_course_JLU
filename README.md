# fmri_course_JLU

fMRI preprocessing pipeline for the JLU fMRI course, run on [Neurodesk](https://neurodesk.org/).

The workflow is split across three notebooks, intended to be run in order:

1. **[1_bids_conversion.ipynb](1_bids_conversion.ipynb)** — Convert the raw Siemens DICOMs into a [BIDS](https://bids.neuroimaging.io/)-compliant dataset using `heudiconv` (with `dcm2niix`) and the project-specific [heuristic.py](heuristic.py).
2. **[2_deface.ipynb](2_deface.ipynb)** — Remove identifiable facial features from the T1w/T2w structural scans with `pydeface`, keeping a backup and a side-by-side QC plot.
3. **[3_fmriprep_run.ipynb](3_fmriprep_run.ipynb)** — Run [fMRIPrep](https://fmriprep.org/) on the BIDS dataset to produce preprocessed anatomical and functional derivatives (requires a FreeSurfer license).

All tools are loaded as Neurodesk container modules, so no local pip/conda install is needed.
