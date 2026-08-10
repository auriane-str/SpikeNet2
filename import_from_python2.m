pyenv( "Version", "your_conda_environment")

dossierProjet = "your_path";

cd(dossierProjet);

fichierMat = "yout_data_path.mat";

commande = sprintf(['your_conda_environment' ...
    'your_path/for_matlab.py "%s"'], ...
    fichierMat);

system(commande);
