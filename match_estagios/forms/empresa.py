from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class EmpresaForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=3)])
    cnpj = StringField("CNPJ", validators=[DataRequired()])
    ramo = StringField("Ramo", validators=[DataRequired()])
    endereco = StringField("Endereço", validators=[DataRequired()])
    site = StringField("Site")
    descricao = StringField("Descrição")

    submit = SubmitField("Salvar")
