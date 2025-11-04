# Reseau : 5G register
**Challenge Author(s):**  0xOri
**Difficulty:** Facile  

## Synopsis
Il semblerait qu'il n'y a qu'une seule personne dans cette zone... à moins que.
Retrouver le MSIN de l'utilisateur qui ne s'est attaché qu'une seule fois.

Format du flag : 
si MSIN: 12345678 alors hit{12345678}

## Steps to solve
Pour ce challenge, il nous est donne un trace de capture réseau ou le but est de retrouver le MSIN du mobile qui n'a fait qu'une seule connexion au réseau 5G.

tout d'abord, il est possible que par défaut, Wireshark ne décode pas les protocoles associés à la 5G notament le NAS. 

Pour ce faire il faut se rendre dans Editer > Préférences > Protocols > NAS-5GS  puis cocher 'Try to detect and decode 5G-EA0 ciphered messages'

Par défaut ce protocol est chiffré, dans certaines conditions cela n'est pas le cas (comme ici) mais il faut explicitement le dire à Wireshark qui, sinon, assumera que c'est chiffré.

On peut voir en regarder la trace à première vue que les séquence s'enchaine les une après les autres.

Nous cherchons ou se trouve dans ces paquets l'info MSIN. on remarque que les paquets TCP sont assez pauvres en informations.

On peut alors utiliser le filtre ngap pour ne garder que les paquets lisibles. Ensuite on chercher l'information.

En analysant le premier échange 'InitilUEMessage, Registration request' et en développant l'ensemble des arborescences on remarque le champs MSIN dans 5GS mobile identity dans Plain NAS 5GS Message, le protocole NAS étant utilisé entre le téléphone et le coeur de réseau 5G.

afin de l'afficher en tant que colone sur notre trace écran principale on peut glisser le champs depuis la fenêtre de détail du paquet vers la fenêtre principal de wireshark au niveau des colonnes.

On peut ensuite trier les paquets selon ce champs.

On remarque alors que tout les MSIN sont identiques sauf pour une procédure (le MSIN apparait dans 2 paquets) nous donnant ainsi le flag hit{00004683}