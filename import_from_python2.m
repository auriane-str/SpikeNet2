pyenv( "Version", "/home/auristre/.conda/envs/SpikeNet2/bin/python")

dossierProjet = "/NAS/home/auristre/Documents/software/SpikeNet2/";

cd(dossierProjet);

fichierMat = "/NAS/home/auristre/Documents/software/SpikeNet2/data/PA07_05bis_reorderd.mat";

commande = sprintf(['/home/auristre/.conda/envs/SpikeNet2/bin/python ' ...
    '/NAS/home/auristre/Documents/software/SpikeNet2/for_matlab.py "%s"'], ...
    fichierMat);

system(commande);