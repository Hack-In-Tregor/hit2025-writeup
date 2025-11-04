# Binary : ASCII-art
**Challenge Author(s):**  0xOri
**Difficulty:** Très facile  

## Synopsis
Cet étrange programme semble avoir plus à dire que sa simple animation. Saurez-vous regarder au-delà de l’art ?

## Steps to Solve:

Pour ce challenge, il est fournit un binaire : ascii_art

```bash
file ascii_art
ascii_art: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=81544629ae0a32249a48b0bc5134fb7b1455adea, stripped
```

Celui ci peut être executé et affiche un petit dessin animé. Mais pas de Flag

On cherche ensuite s'il continent des chaines de caractères lisible directement avec strings. On remarque qu'il y en a ok plusieurs. On filtre ensuite avec le format de flag attendu :


```bash
strings ascii_art| grep hit
hit{secret_no_so_hide}
```
