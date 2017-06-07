from django.contrib import admin

from .models import *

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
class TipoServidorAdmin(admin.ModelAdmin):
    pass
class ServidorAdmin(admin.ModelAdmin):
    pass
class PrevisaoOrcamentariaAdmin(admin.ModelAdmin):
    pass
class TipoGestaoRecursosFinanceirosAdmin(admin.ModelAdmin):
    pass
class GestaoRecursosFinanceirosAdmin(admin.ModelAdmin):
    pass
class CursoExtensaoAdmin(admin.ModelAdmin):
    pass
class PalavraChave_CursoExtensaoAdmin(admin.ModelAdmin):
    pass
class FuncaoServidorAdmin(admin.ModelAdmin):
    pass
class Servidor_CursoExtensaoAdmin(admin.ModelAdmin):
    pass
class TurnoCursoAdmin(admin.ModelAdmin):
    pass
class Discente_CursoExtensaoAdmin(admin.ModelAdmin):
    pass
class MembroComunidade_CursoExtensaoAdmin(admin.ModelAdmin):
    pass


admin.site.register(MembrosComunidade, MembrosComunidadeAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(UnidadeAdministrativa, UnidadeAdministrativaAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Centro, CentroAdmin)
admin.site.register(GrandeArea, GrandeAreaAdmin)
admin.site.register(AreaTematica, AreaTematicaAdmin)
admin.site.register(LinhaExtensao, LinhaExtensaoAdmin)
admin.site.register(CursoUnioeste, CursoUnioesteAdmin)
admin.site.register(TipoServidor, TipoServidorAdmin)
admin.site.register(Servidor, ServidorAdmin)
admin.site.register(PrevisaoOrcamentaria, PrevisaoOrcamentariaAdmin)
admin.site.register(TipoGestaoRecursosFinanceiros, TipoGestaoRecursosFinanceirosAdmin)
admin.site.register(GestaoRecursosFinanceiros, GestaoRecursosFinanceirosAdmin)
admin.site.register(CursoExtensao, CursoExtensaoAdmin)
admin.site.register(PalavraChave_CursoExtensao, PalavraChave_CursoExtensaoAdmin)
admin.site.register(FuncaoServidor, FuncaoServidorAdmin)
admin.site.register(Servidor_CursoExtensao, Servidor_CursoExtensaoAdmin)
admin.site.register(TurnoCurso, TurnoCursoAdmin)
admin.site.register(Discente_CursoExtensao, Discente_CursoExtensaoAdmin)
admin.site.register(MembroComunidade_CursoExtensao, MembroComunidade_CursoExtensaoAdmin)
