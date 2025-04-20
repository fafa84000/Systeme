#!/bin/bash

read -p "Avez-vous verifié le contenu de crontab avant de lancer ce script ? (Y/n)" choix

choix=${choix,,}

if [[ "$choix" == "y" || "$choix" == "" ]]; then
	crontab -l > /tmp/crontab_tmp.txt
	cat crontab.txt >> /tmp/crontab_tmp.txt
	crontab /tmp/crontab_tmp.txt
	echo "Contenu de \"crontab.txt\" copié dans crontab."
else
	echo "pour modifer crontab faire: crontab -e"
	echo "pour afficher le contenu de crontab faire: crontab -l"
fi
