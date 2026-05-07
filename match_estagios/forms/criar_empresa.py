from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class MaintainerEmpresaForm(FlaskForm):
    """Formulário de criação de empresa. O usuário é criado, antes, porque não é possível ter empresa sem usuário para gerenciar"""

    # User
    user_name = StringField("Nome do responsável", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])

    # Empresa
    name = StringField("Nome da empresa", validators=[DataRequired()])
    cnpj = StringField("CNPJ", validators=[DataRequired()])
    ramo = StringField("Ramo", validators=[DataRequired()])
    endereco = StringField("Endereço", validators=[DataRequired()])
    site = StringField("Site")
    descricao = StringField("Descrição")

    submit = SubmitField("Criar empresa")
