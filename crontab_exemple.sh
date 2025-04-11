# execution au demarage du moteur de stockage et de l'ecouteur du nombre de sondes
@reboot python3 ~/Systeme/Partie2_Moteur_Alertes/moteur_de_stockage.py
@reboot python3 /path/Systeme/Partie2_Moteur_Alertes/update_number.py

# suppression des données obselétes
0 * * * * python3 /path/Systeme/Partie2_Moteur_Alertes/supp_bdd.py sonde_data 1 DAY

# sondes
0 * * * * python3 /path/Systeme/Partie1_Sondes/cpu_sonde.py
0 * * * * python3 /path/Systeme/Partie1_Sondes/disk_sonde.py
0 * * * * bash /path/Systeme/Partie1_Sondes/users_sonde.sh