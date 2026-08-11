# SpikeNet2
This repository contains the code used to preprocess EEG recordings and adapt them to the input format required by the SpikeNet2 model.


# 1. Preprocessing

The first step is to preprocess the EEG recordings directly from Brainstorm. 
The following preprocessing steps are applied:

1- Band-pass filtering: 0.5 Hz - 100 Hz

2- Notch filtering: 60 Hz

3- Resampling: 128 Hz


# 2. Reordering

The model expects the EEG channels to be provided in a specific order.

Two functions are available for this step:

1- `export_and_reordered` 
This function reorders the channels and creates the average and bipolar montage used by the model.

2- `reorderedfonction` 
This function only reorders the channels.

Both functions create a new EEG file that can be used to run predictions with SpikeNet2.

# 3. Predictions

There are two ways to run the SpikeNet2 model.

1- If you want to run the model directly from MATLAB, you can use the `import from python` code. This code calls the `pour_matlab.py` Python script, which runs the model and returns the predictions to MATLAB.

For this method, the `export_and_reordered` for the channel reordering step.

2- You can also use the `import from python2` code. This code calls the `for_matlab.py` Python script, which runs the model and returns the predictions to MATLAB.

For this method use `reorderedfonction` for the channel reordering step.

These functions are part of the original SpikeNet2 implementation and should already be available when downloading the SpikeNet2 GitHub repository.


The first method is faster than the second because processes a larger number of windows.

The second method is the original method provided by SpikeNet2, while the first method has been modified and adapted to make it faster and easier to use directly from MATLAB.

# 4. Visualization

If you want to convert the model prediction into annotation you can be imported in Brainstorm, you can use the `save_threshold` code. 

This code identifies all prediction peaks above a threshold of 0.5 and creates a text file containing the corresponding times.
The resulting text file can be imported into Brainstorm as annotations.


# Original work

This work is a direct adaptation of [spikenet2](https://bdsp.io/content/spikenet2/1.0/).

If you use this code in your work please cite : Li, J., Goldenholz, D., Hong, S., Sun, C., Jing, J., & Westover, M. B. (2025). SpikeNet 2.0 (version 1.0). Brain Data Science Platform. https://doi.org/10.60508/mbxb-hn49.

Li J, Goldenholz DM, Alkofer M, Sun C, Nascimento FA, Halford JJ, Dean BC, Galanti M, Struck AF, Greenblatt AS, Lam AD, Herlopian A, Nwankwo C, Weber D, Maus D, Haider HA, Karakis I, Yoo JY, Ng MC, Selioutski O, Taraschenko O, Osman G, Katyal R, Schmitt SE, Benbadis S, Cash SS, Tatum WO, Sheikh Z, Kong WY, Bayas G, Turley N, Hong S, Westover MB, Jing J. Expert-Level Detection of Epilepsy Markers in EEG on Short and Long Timescales. NEJM AI. 2025 Jul;2(7):10.1056/aioa2401221. doi: 10.1056/aioa2401221. Epub 2025 Jun 26. PMID: 40689158; PMCID: PMC12276842.

