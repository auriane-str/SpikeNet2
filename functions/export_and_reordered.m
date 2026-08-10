function export_and_reordered(sFiles, out)
    % Importation des données depuis Brainstorm
    sExport = in_bst_data(sFiles);

    % Load channel file
    channel_file = bst_get('ChannelFileForStudy', sFiles);
    sChannels = in_bst_channel(channel_file);
    
    % Initialisation de la structure de sortie
    newFile = struct();
    newFile.Fs = 1 / (sExport.Time(2) - sExport.Time(1));
    
    % Extraction et uniformisation des noms de canaux
    channels = upper({sChannels.Channel.Name}'); 
    data = sExport.F * 1e6;

    % Mappage des noms (Standardisation 10-20)
    keys = {'FP1','FP2','F3','F4','C3','C4','P3','P4','O1','O2','F7','F8','T7','T8','P7','P8','FZ','PZ','CZ'};
    values = {'FP1','FP2','F3','F4','C3','C4','P3','P4','O1','O2','F7','F8','T3','T4','T5','T6','FZ','PZ','CZ'};
    mapping = containers.Map(keys, values);
    
    channels_mapped = channels;
    for i = 1:numel(channels)
        if isKey(mapping, channels{i})
            channels_mapped{i} = mapping(channels{i});
        end
    end

    % Réorganisation selon l'ordre cible (Monopolaires)
    target_order = {'FP1','F3','C3','P3','F7','T3','T5','O1','FZ','CZ','PZ','FP2','F4','C4','P4','F8','T4','T6','O2'};
    idx = zeros(1, numel(target_order));
    for k = 1:numel(target_order)
        found = find(strcmp(channels_mapped, target_order{k}), 1);
        if isempty(found)
            error('Canal requis manquant dans les données : %s', target_order{k});
        end
        idx(k) = found;
    end
    fprintf('Nombre de lignes dans data : %d\n', size(data, 1));
    fprintf('Index maximum demandé dans idx : %d\n', max(idx));
    fprintf('Index minimum demandé dans idx : %d\n', min(idx));

    data_reordered = data(idx, :);
    channels_reordered = channels_mapped(idx);

    % Montage Référence Moyenne (Average Reference)
    average_data = data_reordered - mean(data_reordered, 1);
    average_labels = cellfun(@(x) [x '-AVG'], channels_reordered, 'UniformOutput', false);

    % Montage Bipolaire
    bipolar_channels = {'FP1-F7','F7-T3','T3-T5','T5-O1','FP2-F8','F8-T4','T4-T6','T6-O2','FP1-F3','F3-C3','C3-P3','P3-O1','FP2-F4','F4-C4','C4-P4','P4-O2','FZ-CZ','CZ-PZ'};
    bipolar_data = zeros(numel(bipolar_channels), size(data_reordered, 2));

    for i = 1:numel(bipolar_channels)
        parts = split(bipolar_channels{i}, '-');
        idx1 = find(strcmp(channels_reordered, parts{1}));
        idx2 = find(strcmp(channels_reordered, parts{2}));
        bipolar_data(i, :) = data_reordered(idx1, :) - data_reordered(idx2, :);
    end

    % Concaténation finale (Données et Noms correspondants)
    %newFile.data = [average_data; bipolar_data];
    newFile.data = [bipolar_data; average_data];
    %newFile.channels = [average_labels; bipolar_channels(:)];
    newFile.channels = [bipolar_channels(:); average_labels];

    % Sauvegarde
    fileout = fullfile('/NAS/home/auristre/Documents/software/SpikeNet2/data/', out);
    save(fileout, '-struct', 'newFile');
end
