from django.contrib import admin

from .models import DadosPaciente, Opcao, Pacientes, Refeicao

# Register your models here.
admin.site.register(Pacientes)
admin.site.register(DadosPaciente)
admin.site.register(Opcao)
admin.site.register(Refeicao)
