from flask_wtf import FlaskForm
from wtforms.fields import (
    DateField,
    EmailField,
    StringField,
    SubmitField,
    TelField,
    TextAreaField,
    URLField,
)
from wtforms.validators import DataRequired, Email, Length


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
