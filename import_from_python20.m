pyenv( "Version", "your_conda_environment")

dossierProjet = "your_path";

cd(dossierProjet);

fichierMat = "path_of_the_data.mat";

commande = sprintf(['your_conda_environment ' ...
    'your_path/pour_matlab.py "%s"'], ...
    fichierMat);

system(commande);
