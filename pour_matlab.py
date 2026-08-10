#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scipy.io as sio
import torch
import numpy as np


#mat = sio.loadmat("/NAS/home/auristre/Documents/software/SpikeNet2/data/data_tutorial_preprocessed_reordered_avgbip.mat")

import sys

# premier argument = fichier à prédire
fichier_entree = sys.argv[1]

mat = sio.loadmat(fichier_entree)
eeg = mat["data"]
eeg = eeg / (np.quantile(np.abs(eeg), q=0.95, method="linear", axis=-1, keepdims=True) + 1e-8)


# première seconde
window = eeg[:,0:128]

print(window.shape)

x = torch.tensor(window, dtype=torch.float32)

print(x.shape)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc, f1_score,accuracy_score ,precision_recall_curve, average_precision_score
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
import os
import pickle
from torchvision import transforms
import pytorch_lightning as pl
import torch

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
from sleeplib.montages import CDAC_bipolar_montage,CDAC_common_average_montage,CDAC_combine_montage,con_combine_montage
from sleeplib.transforms import cut_and_jitter, channel_flip, extremes_remover


from torch.utils.data import Dataset
import torch
import numpy as np


class MyEEGDataset(Dataset):
    def __init__(self, eeg, window_size=128):
        self.eeg = eeg
        self.window_size = window_size
        
        # positions de début des fenêtres
        self.starts = np.arange(
            0,
            eeg.shape[1] - window_size + 1,
            window_size
        )
    def __len__(self):
        return len(self.starts)

    def __getitem__(self, idx):
        start = self.starts[idx]

        x = self.eeg[:, start:start+self.window_size]

        x = torch.tensor(
            x,
            dtype=torch.float32
        )

        return x, torch.tensor(0)
    
    
dataset = MyEEGDataset(
    eeg,
    window_size=128
)

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=False
)


config = Config()
config.print_config()


model = ResNet.load_from_checkpoint(
    '/NAS/home/auristre/Documents/software/SpikeNet2/model/new_weights.ckpt',
    lr=config.LR,
    n_channels=config.N_CHANNELS,
    map_location='cpu'
)



trainer = pl.Trainer(
    devices=1,
    accelerator="gpu",
    enable_progress_bar=True
)

preds = trainer.predict(
    model,
    loader
)


preds = torch.cat(preds).cpu().numpy()


plt.plot(preds)
plt.xlabel("Temps (s)")
plt.ylabel("Probabilité spike")
plt.show()

import os
import scipy.io as sio

# Nom du fichier de sortie
fichier_sortie = os.path.splitext(fichier_entree)[0] + "_predictions.mat"

# Sauvegarde
sio.savemat(fichier_sortie, {"preds": preds})

print(f"Predictions sauvegardées dans : {fichier_sortie}")


# In[ ]:





# In[ ]:




