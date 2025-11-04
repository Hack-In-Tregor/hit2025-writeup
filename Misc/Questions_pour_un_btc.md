# MISC : questions_pour_un_btc
**Challenge Author(s):**  0xOri
**Difficulty:** Moyen  

## Synopsis
Saurez-vous répondre ? 

Attention les réponses sont sensibles à la casses. Réponses en minusculte uniquement. Le nombre de * correspond au nombre de caractères dans la réponse.

## Steps to Solve:
Pour ce challenge, un service nous est exposé.

En se connectant au service en utilisant nc, une question nous est posée, puis après un petit temps, la connexion est close.

Il faut donc trouver un moyen pour envoyer la réponse de manière automatique. La commande suivante permet de le faire.

```bash
echo 'test' | nc localhost 9000
Incorrect. Connection closing.
```
attardons nous maitenant sur les questions :

Question 1: Quel organisme a installe un centre de recherche telecoms a Lannion ? https://fr.wikipedia.org/wiki/Centre_national_d%27%C3%A9tudes_des_t%C3%A9l%C3%A9communications CNET

```bash
echo 'cnet' | nc localhost 9000
Question 1: Quel organisme a installe un centre de recherche telecoms a Lannion ? (****)
> Question 2: Quel site breton a accueilli la premiere antenne satellite en Europe en 1962 ? (*************)
```

Cela nous donne accès à la question suivante, nous devons donc contrsuire un script pour envoyer plusieurs questions séquenciellement

```bash
#!/bin/bash

HOST="localhost"
PORT=9000

{
  echo "cnet"; sleep 0.1
  echo "pleumeur-bodou";sleep 0.1
} | nc localhost 9000
```
et ainsi de suite pour les questions suivantes :

Question 1: Quel organisme a installe un centre de recherche telecoms a Lannion ? (****) => https://fr.wikipedia.org/wiki/Centre_national_d%27%C3%A9tudes_des_t%C3%A9l%C3%A9communications cnet

Question 2: Quel site breton a accueilli la premiere antenne satellite en Europe en 1962 ? (*************) => https://fr.wikipedia.org/wiki/Centre_de_t%C3%A9l%C3%A9communication_par_satellite_de_Pleumeur-Bodou pleumeur-bodou

Question 3: Quel dôme protecteur abritait l’antenne geante a Pleumeur-Bodou ? (******) => radome

Question 4: Quel est le nom du projet du prototype de commutateur téléphonique numérique développé à Lannion ? (******) => https://memoire-alcatel-lannion.fr/histoires/RecueilT%C3%A9moinages/LeProjetPlaton.pdf platon

Question 5: En 2012, combien le parc Pakistanais comptait de commutateurs OCB283 ? (***) => https://memoire-alcatel-lannion.fr/histoires/RecueilT%C3%A9moinages/IntroductionOCB283AuPakistan.pdf 127

Question 6: Quel est le nom de l'ancien sénateur français ayant eu une influence considérable sur le développement économique et des télécommunications à Lannion ? => https://fr.wikipedia.org/wiki/Pierre_Marzin Marzin 

Question 7: Quel est le nom de du responsable de projet écran plat du CNET de Lannion ? (***********) => https://enseignants.lumni.fr/fiche-media/00000000965/le-centre-national-d-etudes-des-telecommunications-de-lannion.html 02:00 lecontellec

Question 8: Avec quel ville des USA le premier direct France-USA à eu lieu ? (*******) => https://www.ouest-france.fr/bretagne/le-premier-direct-europe-etats-unis-50-ans-1577053 andover

Question 9: Quelle firme américaine a développé le satelite ayant permis cette première communication direct ? (****) => https://fr.wikipedia.org/wiki/Telstar_1 at&t

Nous donnant ainsi le script final : 

```bash
#!/bin/bash

HOST="localhost"
PORT=9000

{
  echo "cnet"; sleep 0.1
  echo "pleumeur-bodou";sleep 0.1
  echo "radome";sleep 0.1
  echo "platon";sleep 0.1
  echo "127";sleep 0.1
  echo "marzin";sleep 0.1
  echo "lecontellec";sleep 0.1
  echo "andover";sleep 0.1
  echo "at&t"
} | nc "$HOST" "$PORT"
```
Révelant ainsi le flag : Correct! Flag : hit{qpuc_on_the_way}