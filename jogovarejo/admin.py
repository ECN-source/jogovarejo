from django.contrib import admin

from django.contrib import admin

from . import models

admin.site.register(models.Controle)
admin.site.register(models.Grupo)
admin.site.register(models.Sorteado)
admin.site.register(models.Compra)
admin.site.register(models.Movimento)

