import os
from hashlib import sha256

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Ativacao
from .utils import campos_branco, email_html, password_is_valid


# Create your views here.
def cadastro(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not (
            campos_branco(request, email, usuario, senha, confirmar_senha)
            or password_is_valid(request, senha, confirmar_senha)
        ):
            return redirect('/auth/cadastro')
        try:
            user = User.objects.filter(username=usuario)
            if user:
                messages.add_message(
                    request, constants.ERROR, 'Username já cadastrado'
                )
                return redirect('/auth/cadastro')
            user = User.objects.create_user(
                username=usuario,
                password=senha,
                is_active=False,
            )
            user.save()
            path_template = os.path.join(
                settings.BASE_DIR,
                'autenticacao/templates/emails/cadastro_confirmado.html',
            )

            email_html(
                path_template,
                'Cadastro confirmado',
                [
                    email,
                ],
                username=usuario,
                link_ativacao="127.0.0.1:8000/auth/ativar_conta/{token}",
            )
            token = sha256(f'{usuario}{email}'.encode()).hexdigest()
            ativacao = Ativacao(token=token, user=user)
            ativacao.save()
            messages.add_message(
                request, constants.SUCCESS, 'Usuário cadastrado com sucesso'
            )
            return redirect('/auth/logar')
        except:  # pylint: disable=bare-except
            messages.add_message(
                request, constants.ERROR, 'Erro interno no servidor'
            )
            return redirect(('/auth/cadastro'))
    # TODO: ERRO DE 500
    return HttpResponse('ERRO MÉTODO INVÁLIDA')


def logar(request: HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'logar.html')
    if request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(
                request, constants.ERROR, 'Username ou senha inválidos'
            )
            return redirect('/auth/logar')
        auth.login(request, usuario)
        return redirect('/')
    # TODO: ERRO DE 500
    return HttpResponse('ERRO MÉTODO INVÁLIDA')


def sair(request):
    auth.logout(request)
    return redirect('auth/logar')


def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(
            request, constants.WARNING, 'Essa token já foi usado'
        )
        return redirect('/auth/logar')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/logar')
