from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class NameForm(FlaskForm):
    # Campo para o nome do usuário
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])

    # Novo campo obrigatório: E-mail para recebimento da notificação
    email = StringField('Qual é o seu email (Envio de notificação do novo usuário)?', validators=[DataRequired(), Email()])

    # Botão de submissão
    submit = SubmitField('Enviar')