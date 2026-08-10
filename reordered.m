
%sFiles = {'PA65/PA65_EPI-ekobayashi_20090720_04_600Hz_SingleTrial-f-CA_band_notch_resample/data_block001.mat'};
%sFiles = {'PA11/sub-PA11_ses-EEGfNIRS01_task-sleep_mod-eeg_run-04_synced_band_notch_resample/data_block001.mat'};

sFiles = {...
    'Subject10/sub-PA07_ses-EEGfNIRS02_task-sleep_mod-eeg_run-05_synced_band_notch_resample/data_block001.mat'};


export_and_reordered(sFiles{1}, 'PA07_05bis_reorderd')


%reorderedfonction(sFiles{1}, 'PA65_ordre')