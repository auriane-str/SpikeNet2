%% Charger les prédictions
load('/NAS/home/auristre/Documents/software/SpikeNet2/data/PA07_05bis_reorderd_predictions.mat')  % contient la variable preds

%% Parameters
fs = 128;      
step = 32;      
dt = step / fs; 


%% Threshold
threshold = 0.5;

[pks, locs] = findpeaks(preds, 'MinPeakHeight', threshold);

times = (locs - 1)*dt;   % si une prédiction = 1 seconde

spike_detected = preds > threshold;

idx = find(spike_detected);

% Une prédiction = une fenêtre de 1 seconde
times = (idx - 1)*dt;   % temps en secondes


%% Sauvegarde txt

filename = '/NAS/home/auristre/Documents/software/SpikeNet2/data/PA07_05bis_reorderd_predictions_events_maxima.mat.txt';

fid = fopen(filename,'w');


for i = 1:length(times)
    fprintf(fid,'\t%.3f\n',...
        times(i));
end

fclose(fid);

disp('Fichier txt créé')

