from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Definindo o formulário usando Flask-WTF
class InfoForm(FlaskForm):
    nome = StringField('Informe o seu nome:', validators=[DataRequired()], render_kw={"class": "form-control"})
    sobrenome = StringField('Informe o seu sobrenome:', validators=[DataRequired()], render_kw={"class": "form-control"})
    instituicao = StringField('Informe a sua Instituição de ensino:', validators=[DataRequired()], render_kw={"class": "form-control"})
    disciplina = SelectField(
        'Informe a sua disciplina:', 
        choices=[('DSWA5', 'DSWA5'), ('DSWA4', 'DSWA4'), ('Gestão de projeto', 'Gestão de projeto')],  # Adiciona mais duas opções
        render_kw={"class": "form-control"}
    )
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})

@app.route("/", methods=['GET', 'POST'])
def index():
    form = InfoForm()
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Recupera os dados do formulário armazenados na sessão
    nome = session.get('nome', None)
    sobrenome = session.get('sobrenome', None)
    instituicao = session.get('instituicao', None)
    disciplina = session.get('disciplina', None)

    if form.validate_on_submit():
        # Checa se o nome já existe e foi alterado, sem considerar outros campos
        if 'nome' in session and form.nome.data != session['nome']:
            flash("Você alterou o seu nome!")
        
        # Atualiza os dados na sessão
        session['nome'] = form.nome.data
        session['sobrenome'] = form.sobrenome.data
        session['instituicao'] = form.instituicao.data
        session['disciplina'] = form.disciplina.data

        return redirect(url_for('index'))  # Redireciona para limpar o formulário
    
    # Renderiza o template com os valores da sessão
    return render_template('index.html', form=form, nome=nome, sobrenome=sobrenome,
                           instituicao=instituicao, disciplina=disciplina, now=now)

if __name__ == "__main__":
    app.run(debug=True)
