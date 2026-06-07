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

    area = SelectField(
        "Área da Vaga",
        choices=[
            ("", "Selecione a área..."), # Opção vazia padrão
            ("Tecnologia", "Tecnologia"),
            ("Administração", "Administração"),
            ("Design", "Design")
        ],
        validators=[DataRequired(message="Por favor, selecione uma área.")]
    )

    disponibilidade = SelectField(
        "Disponibilidade / Período",
        choices=[
            ("", "Selecione a disponibilidade..."), # Opção vazia padrão
            ("Matutino", "Matutino"),
            ("Vespertino", "Vespertino"),
            ("Noturno", "Noturno")
        ],
        validators=[DataRequired(message="Por favor, selecione a disponibilidade.")]
    )

    submit = SubmitField("Criar vaga")