#!/usr/bin/env python
# coding: utf-8


import os
import sys
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import torch

from torch.utils.data import DataLoader,  Dataset
import pytorch_lightning as pl

import pickle
from torchvision import transforms

sys.path.append('../')
from sleeplib.Resnet_15.model import ResNet
from sleeplib.config import Config


# Create EEG windows
class MyEEGDataset(Dataset):
    def __init__(self, eeg, window_size=128):
        self.eeg = eeg
        self.window_size = window_size
        
        # positions de début des fenêtres
        self.starts = np.arange(
            0,
            eeg.shape[1] - (window_size//2) + 1,
            1
        )
    def __len__(self):
        return len(self.starts)

    def __getitem__(self, idx):
        start = self.starts[idx]

        x = self.eeg[:, (start-self.window_size//2):(start+self.window_size//2)]
        
        x = torch.tensor(
            x,
            dtype=torch.float32
        )

        return x, torch.tensor(0)


# Load input data
fichier_entree = sys.argv[1]

mat = sio.loadmat(fichier_entree)
eeg = mat["data"]

# Preprocessing
eeg = eeg / (np.quantile(np.abs(eeg), q=0.95, method="linear", axis=-1, keepdims=True) + 1e-8)

window = eeg[:,0:128]
x = torch.tensor(window, dtype=torch.float32)


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


# Load model
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

# Generate predictions
preds = trainer.predict(
    model,
    loader
)

preds = torch.cat(preds).cpu().numpy()

# Visualization of the predictions
plt.plot(preds)
plt.xlabel("Temps (s)")
plt.ylabel("Probabilité spike")
plt.show()


# Define output file
fichier_sortie = os.path.splitext(fichier_entree)[0] + "_predictions.mat"

# Save predictions
sio.savemat(fichier_sortie, {"preds": preds})

print(f"Predictions sauvegardées dans : {fichier_sortie}")





