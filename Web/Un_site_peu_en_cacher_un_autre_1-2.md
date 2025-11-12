# Web : Un site peut en cacher un autre 1/2
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Un site de cours sur les télécommunications semble cacher un autre site. Partons à sa recherche.

## Steps to solve

Le site expose un fichier `robots.txt` qui vise à empêcher les robots d'exploration (web crawlers) d'accéder à tout ou une partie d'un site web.

```txt
User-agent: *
Disallow: /6c4e961d009dec1cf55ee946f4eb84161/
```

Une fois sur le site un premier flag apparait : `hit{1_week_before_halloween}`