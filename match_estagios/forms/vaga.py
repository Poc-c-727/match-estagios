from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, TextAreaField
from wtforms.fields import SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, NumberRange

from match_estagios.models.vaga import VagaModalidade, VagaStatus


class VagaForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    descricao = TextAreaField("Descrição", validators=[DataRequired()])
    bolsa = DecimalField(
        "Bolsa", validators=[DataRequired(), NumberRange(min=0)], places=2
    )

    modalidade = SelectField(
        "Modalidade",
        choices=[(m.name, m.value.capitalize()) for m in VagaModalidade],
        validators=[DataRequired()],
    )

    status = SelectField(
        "Status",
        choices=[(s.name, s.value.capitalize()) for s in VagaStatus],
        validators=[DataRequired()],
    )

    submit = SubmitField("Criar vaga")
