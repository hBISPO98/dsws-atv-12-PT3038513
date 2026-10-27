from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

import requests
from datetime import datetime

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    
    # Ajuste anti-spam: Enviando o subject sem a tag engessada para evitar filtros anti-spam
    msg = Message(subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_simple_message(to, subject, newUser):
    app = current_app._get_current_object()

    # Definição dos destinatários (e-mails fixos + e-mail digitado no formulário)
    # Garante envio para o e-mail informado no cadastro caso seja válido/autorizado
    destinatarios_lista = ["flaskaulasweb@zohomail.com", "b.hiandra@aluno.ifsp.edu.br"]
    if to and to not in destinatarios_lista:
        destinatarios_lista.append(to)
    
    destinatarios = ", ".join(destinatarios_lista)

    # Requisito: meu prontuário, nome e nome do novo usuário
    meu_prontuario = "PT3038513"
    meu_nome = "Hiandra Bispo"

    conteudo_texto = (
        f"Novo usuário cadastrado: {newUser}\n"
        f"Prontuário: {meu_prontuario}\n"
        f"Nome do Aluno: {meu_nome}"
    )

    # Ajuste anti-spam: Removida a tag fixa '[Flasky]' do assunto para evitar classificação automática como spam
    assunto_limpo = subject

    # Ajuste anti-spam: Formatação do remetente amigável 'Hiandra Bispo <e-mail>'
    remetente_formatado = app.config.get('API_FROM')
    if remetente_formatado and not remetente_formatado.startswith("Hiandra"):
        remetente_formatado = f"Hiandra Bispo <{remetente_formatado}>"

    print('Enviando mensagem (POST)...', flush=True)
    print('URL: ' + str(app.config['API_URL']), flush=True)
    print('api: ' + str(app.config['API_KEY']), flush=True)
    print('from: ' + str(remetente_formatado), flush=True)
    print('to: ' + str(destinatarios), flush=True)
    print('subject: ' + str(assunto_limpo), flush=True)
    print('text: ' + conteudo_texto, flush=True)

    # Tratamento de exceção para evitar crash caso o e-mail não esteja autorizado no Mailgun Sandbox
    try:
        resposta = requests.post(app.config['API_URL'],
                               auth=("api", app.config['API_KEY']), data={
                                   "from": remetente_formatado,
                                   "to": destinatarios,
                                   "subject": assunto_limpo,
                                   "text": conteudo_texto
                               })
        
        # Dispara erro HTTP se o status for 4xx ou 5xx
        resposta.raise_for_status()

        print('Enviando mensagem (Resposta)...' + str(resposta) + ' - ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)
        return resposta

    except requests.exceptions.RequestException as e:
        # Registra a falha no log sem interromper a execução do aplicativo (anti-crash)
        print(f"[Aviso anti-crash] O e-mail não pôde ser enviado via Mailgun: {e}", flush=True)
        print(f"[Aviso anti-crash] O cadastro no banco prosseguirá normalmente. - " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)
        return None