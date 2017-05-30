from django.contrib import admin

from .models import *

class ServidorAdmin(admin.ModelAdmin):
	pass

class MembrosComunidadeAdmin(admin.ModelAdmin):
    pass

class ProgramaAdmin(admin.ModelAdmin):
    pass

class UnidadeAdministrativaAdmin(admin.ModelAdmin):
    pass

class CampusAdmin(admin.ModelAdmin):
    pass

class CentroAdmin(admin.ModelAdmin):
    pass

class GrandeAreaAdmin(admin.ModelAdmin):
    pass

class AreaTematicaAdmin(admin.ModelAdmin):
    pass

class LinhaExtensaoAdmin(admin.ModelAdmin):
    pass

class CursoUnioesteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Servidor, ServidorAdmin)
admin.site.register(MembrosComunidade, MembrosComunidadeAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(UnidadeAdministrativa, UnidadeAdministrativaAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Centro, CentroAdmin)
admin.site.register(GrandeArea, GrandeAreaAdmin)
admin.site.register(AreaTematica, AreaTematicaAdmin)
admin.site.register(LinhaExtensao, LinhaExtensaoAdmin)
admin.site.register(CursoUnioeste, CursoUnioesteAdmin)