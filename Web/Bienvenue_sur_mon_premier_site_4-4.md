# Web : Bienvenue sur mon premier site 4/4
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Le créateur du site nous indique que de nombreux flags sont à trouver !

## Steps to solve

Pour ce dernier flag, le site nous permet de voir la configuration IP ainsi que d'executer une commande `ping` qui prend en paramètre une adresse IP. Or il semble n'y avoir aucune vérification sur les entrées utilisateurs. Ainsi si on remplace l'adresse IP par `127.0.0.1 && ls /`, on obtient :

```bash

```

En executant ouvrant de cette même manière le fichier flag.txt (`127.0.0.1 && cat /flag.txt`), on obtient le résutalt suivant : `hit{bien-joue-le-site-est-dans-vos-mains}`



