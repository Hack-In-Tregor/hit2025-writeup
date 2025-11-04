La plus simple, faire un "strings" sur le fichier et en option cibler des mot-clés comme "hit":
on le trouve encodé en base64

```bash
admin@l ORO_5G % echo aGl0e09uVm9pdFRvdXRJY2l9Cg== | base64 -d
hit{OnVoitToutIci}
```