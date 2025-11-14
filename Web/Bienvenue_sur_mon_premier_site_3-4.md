# Web : Bienvenue sur mon premier site 3/4
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Le créateur du site nous indique que de nombreux flags sont à trouver !

## Steps to solve

On remarque sur la page d'accueil un lien vers l'administration du site. Cependant, la page nous indique que le cookie de session n'est pas le bon. Dans la configuration du navigateur, on remarque que le site nous a renseigné le cookie suivant :

- nom : ``premier-site-user-type``
- valeur : `user`

En remplaçant la valeur `user` par `admin`, puis en actualisant la page, le flag apparait : `hit{ADMIN_ACCESS_GRANTED}`