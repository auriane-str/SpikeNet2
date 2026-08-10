# SpikeNet2
This repository contains the code used to preprocess EEG recordings and adapt them to the input format required by the SpikeNet2 model.


# 1. Preprocessing

The first step is to preprocess the EEG recordings directly from Brainstorm. 
The following preprocessing steps are applied:
1- Band-pass filtering: 0.5 Hz - 100 Hz
2- Notch filtering: 60 Hz
3- Resampling: 128 Hz

# 2. Reordering

The model is expecting the channels in a certain order.

1- The function export_and_reordered reorders the channels and creates average and bipolar montage use by the model.

2- The function reorderedfonction just reorders the channels.

Both of them creates the new file you can use to do predictions.

# 3. Predictions

If you want to run the model directly from matlab, you can use the code import from python, which calls the code pour_matlab.py. With this method, you should use the method 1 for reordering.

You can also use the code .... in a Jupyter notebook, in this case use the method 2 for reordering.

The first code is faster than the second because they are more windows in the second. The second code is totally given by SpikeNet2, whereas I arranged a little the first one.

# 4. Visualization

If you want to convert the prediction into annotation you can import in Brainstorm, you can run the code save_treshold. It will create a text file containing all the times when the prediction has a peak above 0.5.
