#!/usr/bin/env python
# coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

sys.path.append('../')
from sleeplib.Resnet_15.model import ResNet
from sleeplib.datasets import ContinousToSnippetDataset
from sleeplib.montages import con_ECG_combine_montage
from sleeplib.config import Config



# Configuration

config = Config()
path_model = 'your_path/SpikeNet2/'

Batch_size = 128
Fs = config.FQ
Window_size = config.WINDOWSIZE
step = 32

# load montage
transform_train = transforms.Compose([extremes_remover(signal_max = 2000, signal_min = 20)])
con_combine_montage = con_ECG_combine_montage()


# load pretrained model
model = ResNet.load_from_checkpoint('yout_path/model/new_weights.ckpt',
                                        lr=config.LR,
                                        n_channels=37,
                                        map_location=torch.device('cpu') ,
                                       )
                                        

trainer = pl.Trainer(
  devices=1,
  accelerator="gpu",
  fast_dev_run=False,
  enable_progress_bar=False
)

# store results
path_controls = os.path.join("your_path/SpikeNet2/controlset.csv")

controls = pd.read_csv(path_controls)
i = 0



for eeg_file in tqdm(controls.EEG_index):
    
    path = sys.argv[1]
    
    Bonobo_con = ContinousToSnippetDataset(
      path,
      montage=con_combine_montage,
      transform=None,
      window_size=config.WINDOWSIZE
    )
  
    con_dataloader = DataLoader(
      onobo_con, 
      batch_size=128,
      shuffle=False,
      num_workers=os.cpu_count()
    )
 
    preds = trainer.predict(model,con_dataloader)
    
    preds = np.concatenate(preds).astype(float)

    preds = pd.DataFrame(preds)
    preds.to_csv(path + '_predictions2' +'.csv',index=False)
    
    

# path to csv file
path_pred = path + '_predictions2.csv'

# load predictions
preds = pd.read_csv(path_pred)

# convert into numpy
preds = preds.values.squeeze()

# predictions frequency
fs_pred = 128  

# axe temporel
step=32
#time = np.arange(len(preds)) *step / fs_pred
time = np.arange(len(preds))

# Visualization

plt.figure(figsize=(12,4))
plt.plot(time, preds)

plt.xlabel("Time (s)")
plt.ylabel("Prediction score")
plt.title("SpikeNet2 predictions")
plt.grid(True)

plt.show()

