from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from match_estagios.models.user import UserRole, UserStatus


class UsuarioForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])

    role = SelectField(
        "Role",
        choices=[(r.name, r.value.capitalize()) for r in UserRole],
        validators=[DataRequired()],
    )

    status = SelectField(
        "Status",
        choices=[(s.name, s.value.capitalize()) for s in UserStatus],
        validators=[DataRequired()],
    )

    submit = SubmitField("Criar")
