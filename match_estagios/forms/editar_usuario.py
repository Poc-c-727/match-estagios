from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

from match_estagios.models.user import UserRole, UserStatus


class MaintainerUsuarioForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Senha")

    role = SelectField(
        "Role",
        choices=[(r.name, r.value) for r in UserRole],
        validators=[DataRequired()],
    )

    status = SelectField(
        "Status",
        choices=[(s.name, s.value) for s in UserStatus],
        validators=[DataRequired()],
    )

    submit = SubmitField("Criar")
