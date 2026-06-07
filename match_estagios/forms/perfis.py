from flask_wtf import FlaskForm
from wtforms.fields import (
    DateField,
    EmailField,
    StringField,
    SubmitField,
    TelField,
    TextAreaField,
    URLField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, Length, Optional


class UserPerfilForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=3, max=255)])
    email = EmailField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=255)]
    )

    salvar = SubmitField("Salvar")


class EstudantePerfilForm(UserPerfilForm):
    cpf = StringField("CPF", validators=[DataRequired(), Length(min=11, max=20)])
    data_nascimento = DateField("Data de nascimento", validators=[DataRequired()])
    endereco = StringField("Endereço", validators=[DataRequired(), Length(max=255)])
    telefone = TelField("Telefone", validators=[Length(max=20)])
    curso = SelectField(
        "Curso",
        choices=[
            ("", "Selecione seu curso..."),
            ("Análise e Des. de Sistemas", "Análise e Desenvolvimento de Sistemas"),
            ("Engenharia de Software", "Engenharia de Software")
        ],
        validators=[DataRequired(message="Por favor, selecione seu curso.")]
    )

    semestre = SelectField(
        "Semestre Atual",
        choices=[
            ("", "Selecione o semestre..."),
            ("1", "1º Semestre"),
            ("2", "2º Semestre"),
            ("3", "3º Semestre"),
            ("4", "4º Semestre"),
            ("5", "5º Semestre"),
            ("6", "6º Semestre")
        ],
        coerce=lambda x: int(x) if x and str(x).isdigit() else None,
        validators=[DataRequired(message="Por favor, selecione seu semestre.")]
    )

    disponibilidade = SelectField(
        "Disponibilidade",
        choices=[
            ("", "Selecione sua disponibilidade..."),
            ("Matutino", "Matutino"),
            ("Vespertino", "Vespertino"),
            ("Noturno", "Noturno")
        ],
        validators=[DataRequired(message="Por favor, selecione sua disponibilidade.")]
    )

    area_interesse = SelectField(
        "Área de Interesse",
        choices=[
            ("", "Selecione sua área principal..."),
            ("Tecnologia", "Tecnologia"),
            ("Administração", "Administração"),
            ("Design", "Design")
        ],
        validators=[DataRequired(message="Por favor, selecione uma área.")]
    )

    # TextAreaField é perfeito para blocos grandes de texto (Currículo)
    curriculo_texto = TextAreaField(
        "Currículo Profissional (Texto)", 
        validators=[Optional()]
    )


class EmpresaPerfilForm(UserPerfilForm):
    cnpj = StringField("CNPJ", validators=[DataRequired(), Length(min=14, max=20)])
    ramo = StringField("Ramo", validators=[DataRequired(), Length(max=255)])
    endereco = StringField("Endereço", validators=[DataRequired(), Length(max=255)])
    site = URLField("Site", validators=[Length(max=255)])
    descricao = TextAreaField("Descrição")


class FaculdadePerfilForm(UserPerfilForm):
    cnpj = StringField("CNPJ", validators=[DataRequired(), Length(min=14, max=20)])
    site = URLField("Site", validators=[Length(max=255)])
    telefone = TelField("Telefone", validators=[Length(max=20)])
