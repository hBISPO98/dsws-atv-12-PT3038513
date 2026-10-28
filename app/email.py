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

    # Requisito: meu prontuário, nome e nome do novo usuário
    meu_prontuario = "PT3038513"
    meu_nome = "Hiandra Bispo"

    # Conteúdo em HTML
    conteudo_html = f"""
    <h3>Novo Cadastro na Aplicação</h3>
    <p><b>Prontuário do aluno:</b> {meu_prontuario}</p>
    <p><b>Nome do aluno:</b> {meu_nome}</p>
    <hr>
    <p><b>Novo usuário cadastrado:</b> {newUser}</p>
    <p><b>E-mail de contato:</b> {to}</p>
    """

    remetente = app.config.get('FLASKY_MAIL_SENDER')

    print('Enviando mensagem via Flask-Mail (SMTP)...', flush=True)
    print(f'From: {remetente}', flush=True)
    print(f'To: {destinatarios_lista}', flush=True)
    print(f'Subject: {subject}', flush=True)

    msg = Message(
        subject=subject,
        sender=remetente,
        recipients=destinatarios_lista
    )
    msg.html = conteudo_html

    try:
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        print('E-mail disparado assincronamente com sucesso! - ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)
        return thr
    except Exception as e:
        print(f"[Aviso anti-crash] O e-mail não pôde ser enviado via SMTP: {e}", flush=True)
        print(f"[Aviso anti-crash] O cadastro no banco prosseguirá normalmente. - " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)
        return None
