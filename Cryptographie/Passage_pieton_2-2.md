# Crypto : Passage piéton 2/2
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Une fois le code source de la page récupérée, il semble possible d'atteindre également la base de données SQLite. Cette dernière stocke des éléments chiffrés

## Steps to solve

En ouvrant la base de données avec SQLite on trouve les valeurs suivantes :

```bash
admin@HIT2025:~/bdd-passages$ sqlite3 troadeg-bZh.sqlite
SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> .tables
SECRET_TABLE  passages
sqlite> select * from SECRET_TABLE;
aes-256-cbc-pbkdf2|HGEpbfYHAhL3owqsT1lsTBUqO6|U2FsdGVkX1+2XA4zEtBoatZtxkF4QsDz2nRM0bgZnTY6zGJBb0GahGHmGwMNAmmq
```

Il semblerait que la base de données stocke une données chiffrées avec l'algorithme `AES-256-CBC-PBKDF2`. On en déduit que les entrées suivantes sont un texte chiffré et une clé.

Après quelques recherches, la commande `openssl aes-256-cbc -d -a -pbkdf2 -in encrypted_data` semble permettre de déchiffrer les données.

```bash
$ echo 'U2FsdGVkX1+2XA4zEtBoatZtxkF4QsDz2nRM0bgZnTY6zGJBb0GahGHmGwMNAmmq' > encrypted_data
admin@HIT2025:~/bdd-passages$ openssl aes-256-cbc -d -a -pbkdf2 -in encrypted_data
enter AES-256-CBC decryption password: HGEpbfYHAhL3owqsT1lsTBUqO6
hit{LFI/AES/FTW}
```