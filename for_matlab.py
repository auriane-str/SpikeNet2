#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
import os
import pickle
from torchvision import transforms
import pytorch_lightning as pl
import torch
from tqdm import tqdm
import scipy.io as sio
import matplotlib.pyplot as plt

# load own code
import sys
sys.path.append('../')
from sleeplib.Resnet_15.model import ResNet
from sleeplib.datasets import BonoboDataset, ContinousToSnippetDataset
# this holds all the configuration parameters
from sleeplib.config import Config
import pickle

from pytorch_lightning.callbacks import ModelCheckpoint
from torch.utils.data import DataLoader
from torchvision import transforms

from sleeplib.datasets import BonoboDataset , ContinousToSnippetDataset
from sleeplib.montages import CDAC_bipolar_montage,CDAC_common_average_montage,CDAC_combine_montage,con_combine_montage, con_ECG_combine_montage
from sleeplib.transforms import cut_and_jitter, channel_flip,extremes_remover

# load config and show all default parameters
config = Config()
path_model = 'your_path/SpikeNet2/'

# set up dataloader to predict all samples in test dataset
transform_train = transforms.Compose([extremes_remover(signal_max = 2000, signal_min = 20)])
con_combine_montage = con_ECG_combine_montage()


# load pretrained model
model = ResNet.load_from_checkpoint('your_path/SpikeNet2/model/new_weights.ckpt',
                                        lr=config.LR,
                                        n_channels=37,
                                        map_location=torch.device('cpu') ,
                                       )
                                        #map_location=torch.device('cpu') add this if running on CPU machine

    
# init trainer
#trainer = pl.Trainer(fast_dev_run=False,enable_progress_bar=False,devices = 1,strategy ='ddp')
trainer = pl.Trainer(devices=1, accelerator="gpu",fast_dev_run=False,enable_progress_bar=False)

# store results
path_controls = os.path.join("your_path/SpikeNet2/controlset.csv")

controls = pd.read_csv(path_controls)
i = 0
#controls = controls[controls['Mode']=='Test']

path = sys.argv[1]


Bonobo_con = ContinousToSnippetDataset(
    path,
    montage=con_combine_montage,
    transform=None,
    Fq=128,
    window_size=1,
    step=32
)

print("Number of windows:", len(Bonobo_con))

con_dataloader = DataLoader(
    Bonobo_con,
    batch_size=128,
    shuffle=False,
    num_workers=4
)

preds = trainer.predict(model, con_dataloader)
preds = np.concatenate(preds).astype(float).squeeze()

sio.savemat(path + 'predictions.mat',{'preds': preds})
    

reference_file = path + "predictions.mat"

mat = sio.loadmat(reference_file)

# Remplace "preds_true" par le nom réel de la variable
reference = mat['preds'].squeeze()

window_size = 128
step = 32
fs_pred = 128

time = time = np.arange(len(Bonobo_con))*step/fs_pred

plt.figure(figsize=(12, 4))
plt.plot(time, reference)

plt.xlabel("Time (s)")
plt.ylabel("Prediction score")
plt.title("SpikeNet2 predictions")
plt.grid(True)
plt.tight_layout()
plt.show()

