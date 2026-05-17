from flask_wtf import FlaskForm
from wtforms.fields import DateField, SelectField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Length


class SolicitacaoVerificacaoForm(FlaskForm):
    ra = StringField("RA", validators=[DataRequired(), Length(max=50)])

    cpf = StringField("CPF", validators=[DataRequired(), Length(min=11, max=20)])

    curso = StringField(
        "Curso",
        validators=[DataRequired(), Length(max=255)],
    )

    data_nascimento = DateField(
        "Data de nascimento",
        validators=[DataRequired()],
    )

    endereco = StringField(
        "Endereço",
        validators=[DataRequired(), Length(max=255)],
    )

    telefone = TelField("Telefone", validators=[Length(max=20)])

    id_faculdade = SelectField("Faculdade", validators=[DataRequired()])

    enviar = SubmitField("Enviar solicitação")
