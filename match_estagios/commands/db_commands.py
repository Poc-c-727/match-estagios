from datetime import date

from match_estagios.extensions import bcrypt, db
from match_estagios.models import Empresa, Estudante, Faculdade
from match_estagios.models.user import User, UserRole, UserStatus


def register_commands(app):
    @app.cli.command("reset-db")
    def reset_db():
        """Apaga e Recriar todas as tabelas"""
        db.drop_all()
        db.create_all()
        print("Banco resetado com sucesso")

    @app.cli.command("create-users")
    def create_users():
        """Cria usuários padrões"""

        # ADMIN
        admin = User(
            name="Admin",
            email="admin@email.com",
            password_hash=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role=UserRole.ADMIN,
            status=UserStatus.VERIFICADO,
        )

        # USUÁRIO PENDENTE
        user_pendente = User(
            name="Pendente",
            email="pendente@email.com",
            password_hash=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role=UserRole.ESTUDANTE,
            status=UserStatus.PENDENTE,
        )

        # ESTUDANTE VALIDADO
        estudante_user = User(
            name="Estudante",
            email="estudante@email.com",
            password_hash=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role=UserRole.ESTUDANTE,
            status=UserStatus.VERIFICADO,
        )

        estudante = Estudante(
            name="Estudante Teste",
            cpf="12345678900",
            data_nascimento=date(2000, 1, 1),
            endereco="Rua Teste",
            telefone="11999999999",
            user=estudante_user,
        )

        # EMPRESA
        empresa_user = User(
            name="Empresa",
            email="empresa@email.com",
            password_hash=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role=UserRole.EMPRESA,
            status=UserStatus.VERIFICADO,
        )

        empresa = Empresa(
            name="Empresa Teste",
            cnpj="12345678000100",
            ramo="Tecnologia",
            endereco="Rua Empresa",
            user=empresa_user,
        )

        # FACULDADE
        faculdade_user = User(
            name="Faculdade",
            email="faculdade@email.com",
            password_hash=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role=UserRole.FACULDADE,
            status=UserStatus.VERIFICADO,
        )

        faculdade = Faculdade(
            name="Faculdade Teste",
            cnpj="00987654000100",
            telefone="1133333333",
            user=faculdade_user,
        )

        # salva tudo
        db.session.add_all(
            [
                admin,
                user_pendente,
                estudante_user,
                estudante,
                empresa_user,
                empresa,
                faculdade_user,
                faculdade,
            ]
        )

        db.session.commit()

        print("Todos os usuários foram criados com sucesso")

    @app.cli.command("seed-db")
    def seed_db():
        print("Comando ainda não implementado")
