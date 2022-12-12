from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import DadosPaciente, Pacientes

# Create your views here.


@login_required(login_url='/auth/logar')
def pacientes(request: HttpRequest):
    if request.method == 'GET':
        paciente = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes': paciente})
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if (
            (len(nome.strip()) == 0)
            or (len(sexo.strip()) == 0)
            or (len(data_nascimento.strip()) == 0)
            or (len(email.strip()) == 0)
            or (len(telefone.strip()) == 0)
        ):
            messages.add_message(
                request, constants.ERROR, 'Preencha todos os campos'
            )
            return redirect('/pacientes/')
        try:
            data_nascimento = datetime.strptime(data_nascimento, 'dd/mm/yyyy')
        except:  # pylint: disable=bare-except
            messages.add_message(
                request, constants.ERROR, 'Digite uma data válida'
            )
            return redirect('/pacientes/')
        paciente = Pacientes.objects.filter(email=email)
        if pacientes.exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Já existe um paciente com esse E-mail',
            )
            return redirect('/pacientes/')
        try:
            paciente = Pacientes(
                nome=nome,
                sexo=sexo,
                data_nascimento=data_nascimento,
                email=email,
                telefone=telefone,
                nutri=request.user,
            )

            paciente.save()
            messages.add_message(
                request, constants.SUCCESS, 'Paciente cadastrado com sucesso'
            )
            return redirect('/pacientes/')
        except:  # pylint: disable=bare-except
            messages.add_message(
                request, constants.ERROR, 'Erro interno do sistema'
            )
            return redirect('/pacientes/')


@login_required(login_url='/auth/logar/')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes_nutricionista = Pacientes.objects.filter(nutri=request.user)
        return render(
            request,
            'dados_paciente_listar.html',
            {'pacientes': pacientes_nutricionista},
        )


@login_required(login_url='/auth/logar/')
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(
            request, constants.ERROR, 'Esse paciente não é seu'
        )
        return redirect('/dados_paciente/')

    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(
            request,
            'dados_paciente.html',
            {'paciente': paciente, 'dados_paciente': dados_paciente},
        )

    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        trigliceridios = request.POST.get('triglicerídios')
        if (
            peso.strip() == ''
            or altura.strip() == ''
            or gordura.strip() == ''
            or musculo.strip() == ''
            or hdl.strip() == ''
            or ldl.strip() == ''
            or colesterol_total.strip() == ''
            or trigliceridios.strip() == ''
        ):
            messages.add_message(
                request, constants.ERROR, 'Todos os campos são obrigatórios'
            )
            return redirect('dados_paciente')
        paciente = DadosPaciente(
            paciente=paciente,
            data=datetime.now(),
            peso=peso,
            altura=altura,
            percentual_gordura=gordura,
            percentual_musculo=musculo,
            colesterol_hdl=hdl,
            colesterol_ldl=ldl,
            colesterol_total=colesterol_total,
            trigliceridios=trigliceridios,
        )
        return redirect('/dados_paciente/')


@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data")

    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos, 'labels': labels}
    return JsonResponse(data)
