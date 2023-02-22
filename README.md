Ce projet a été réalisé dans le cadre d'un projet en 5ième année d'études à Polytech Tours. Il a pour but de de mettre en place un outil d'analyse d'une base de données sur le journalisme de données produite à l'occasion des élections présidentielles françaises 2022.
Les différentes parties concernent la détection de mots-clés, la transcription audio, le string matching et des affichages sous forme de graphes.

Voici le lien de la base de donnée : http://mathieu.delalandre.free.fr/projects/stvd/fc/

Et du site miroir : https://dataset-stvd.univ-tours.fr/

Pour utiliser les différents script il faut dans un premier temps installer les dépendances nécessaires.
Dans chaque dossier faire : "pip install -r requirements.txt"
Si le script utilise spacy, installer le modèle avec : "python -m spacy download fr_core_news_md"

Ce projet est en plusieurs parties.
Voici le workflow :
    - Extraire les metadonnées des fichiers XML de la base de données 
        Code : xmlExtractor/main
        Resultat : metadata.json

    - Générer le transcript des fichiers audio avec transcripts
        Code : transcripts/main
        Résultats : audio_transcripts.json
        Code : transcripts/separateTranscripts
        Resultats : database/.../ts_transcript.json

    - Générer une liste de mots-clés avec keywords_database et keywords_factoscope. Il faut alors nettoyer les résultats à la main et transformer les dictionnaires en une liste de chaine de caractères
        Code :  keywords_database/main
                keywords_factoscope/main
        Resultats : keywords.json

    - Générer des fichiers de string matching entre les mots-clés et les trasncripts
        Code : string_matching/main
        Resultats : database/.../ts_spot.json
        Code : string_matching/uniqueFile
        Resultats : string_matching.json
        
    - Analyser les résultats avec analytics pour produire des graphes

La base de donnée est disponible dans le dossier database et possède donc la même architecture que la base de données audio
