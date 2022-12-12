from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Pacientes(models.Model):
    choice_sexo = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )
    nome = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=choice_sexo)
    data_nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.CharField(max_length=19)
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome}"


class DadosPaciente(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data = models.DateTimeField()
    peso = models.IntegerField()
    altura = models.IntegerField()
    percentual_gordura = models.IntegerField()
    percentual_musculo = models.IntegerField()
    colesterol_hdl = models.IntegerField()
    colesterol_ldl = models.IntegerField()
    colesterol_total = models.IntegerField()
    trigliceridios = models.IntegerField()

    def __str__(self):
        return f"Paciente({self.paciente.nome}, {self.peso})"