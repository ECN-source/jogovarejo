from django.contrib import admin

from django.contrib import admin

from . import models

admin.site.register (models.Controle)

class GrupoAdmin (admin.ModelAdmin):
    list_display  = ["Nome", "GrupoOperador", "Ativo"]
    ordering = ["Numero"]
admin.site.register (models.Grupo, GrupoAdmin)

admin.site.register (models.Sorteado)

admin.site.register (models.Compra)

admin.site.register (models.Movimento)

