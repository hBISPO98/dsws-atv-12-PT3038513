from flask import render_template, redirect, url_for, session, current_app
from . import main
from .forms import NameForm  # Ajuste o nome do formulário se necessário
from .. import db
from ..models import User
from ..email import send_simple_message

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # 1. Procura se o utilizador já existe na base de dados
        user = User.query.filter_by(username=form.name.data).first()
        
        if user is None:
            # 2. Cria o novo utilizador e guarda no banco de dados
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            
            # 3. Dispara a notificação por e-mail (usando o try-except do email.py)
            # Passa o e-mail do formulário, o assunto limpo e o nome do novo utilizador
            send_simple_message(
                to=form.email.data, 
                subject="Novo Utilizador Cadastrado", 
                newUser=form.name.data
            )
        else:
            session['known'] = True
            
        session['name'] = form.name.data
        return redirect(url_for('main.index'))
    
    # 4. Procura todos os utilizadores para exibir na tabela da página principal
    users = User.query.all()
    
    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'),
                           known=session.get('known', False),
                           users=users)