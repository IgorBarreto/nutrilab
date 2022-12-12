from django.contrib import admin

from .models import DadosPaciente, Pacientes

# Register your models here.
admin.site.register(Pacientes)
admin.site.register(DadosPaciente)
