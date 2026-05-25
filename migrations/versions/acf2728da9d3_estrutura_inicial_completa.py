"""estrutura inicial completa

Revision ID: acf2728da9d3
Revises: 
Create Date: 2026-05-25 17:20:20.313432

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'acf2728da9d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 1. Criar a tabela base de usuários do zero (id_user como String(36))
    op.create_table('users',
    sa.Column('id_user', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('MAINTAINER', 'ESTUDANTE', 'EMPRESA', 'FACULDADE', name='userrole'), nullable=False),
    sa.Column('status', sa.Enum('PENDENTE', 'VERIFICADO', 'REJEITADO', name='userstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id_user'),
    sa.UniqueConstraint('email')
    )

    # 2. Criar as tabelas de perfis que apontam para users
    op.create_table('empresas',
    sa.Column('id_empresa', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('cnpj', sa.String(length=20), nullable=False),
    sa.Column('ramo', sa.String(length=255), nullable=False),
    sa.Column('endereco', sa.String(length=255), nullable=False),
    sa.Column('site', sa.String(length=255)),
    sa.Column('descricao', sa.Text()),
    sa.Column('id_user', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_empresa'),
    sa.UniqueConstraint('cnpj'),
    sa.UniqueConstraint('id_user')
    )

    op.create_table('estudantes',
    sa.Column('id_estudante', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('cpf', sa.String(length=20), nullable=False),
    sa.Column('data_nascimento', sa.Date(), nullable=False), # <- Corrigido aqui!
    sa.Column('endereco', sa.String(length=255), nullable=False),
    sa.Column('telefone', sa.String(length=20)),
    sa.Column('id_user', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_estudante'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('id_user')
    )

    op.create_table('faculdades',
    sa.Column('id_faculdade', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('cnpj', sa.String(length=20), nullable=False),
    sa.Column('site', sa.String(length=255)),
    sa.Column('telefone', sa.String(length=20)),
    sa.Column('id_user', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_faculdade'),
    sa.UniqueConstraint('cnpj'),
    sa.UniqueConstraint('id_user')
    )

    # 3. Criar as tabelas de negócio e relacionamentos secundários
    op.create_table('solicitacoes_verificacao',
    sa.Column('id_solicitacao', sa.String(length=22), nullable=False),
    sa.Column('ra', sa.String(length=50), nullable=False),
    sa.Column('cpf', sa.String(length=20), nullable=False),
    sa.Column('curso', sa.String(length=255), nullable=False),
    sa.Column('data_nascimento', sa.Date(), nullable=False),
    sa.Column('endereco', sa.String(length=255), nullable=False),
    sa.Column('telefone', sa.String(length=20), nullable=True),
    sa.Column('status', sa.Enum('PENDENTE', 'APROVADA', 'RECUSADA', name='solicitacaostatus'), nullable=False),
    sa.Column('data_solicitacao', sa.DateTime(), nullable=False),
    sa.Column('id_user', sa.String(length=36), nullable=False),
    sa.Column('id_faculdade', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['id_faculdade'], ['faculdades.id_faculdade'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_solicitacao'),
    sa.UniqueConstraint('id_user', 'id_faculdade', name='uq_solicitacao_user_faculdade')
    )

    op.create_table('vagas',
    sa.Column('id_vaga', sa.String(length=22), nullable=False),
    sa.Column('titulo', sa.String(length=255), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=False),
    sa.Column('bolsa', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('modalidade', sa.Enum('REMOTO', 'PRESENCIAL', 'HIBRIDO', name='vagamodalidade'), nullable=False),
    sa.Column('status', sa.Enum('ABERTA', 'PAUSADA', 'FECHADA', 'PREENCHIDA', name='vagastatus'), nullable=False),
    sa.Column('id_empresa', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['id_empresa'], ['empresas.id_empresa'], ),
    sa.PrimaryKeyConstraint('id_vaga')
    )

    op.create_table('candidaturas',
    sa.Column('id_candidatura', sa.String(length=22), nullable=False),
    sa.Column('status', sa.Enum('PENDENTE', 'APROVADO', 'RECUSADO', name='candidaturastatus'), nullable=False),
    sa.Column('data_candidatura', sa.DateTime(), nullable=False),
    sa.Column('id_estudante', sa.String(length=36), nullable=False),
    sa.Column('id_vaga', sa.String(length=22), nullable=False),
    sa.ForeignKeyConstraint(['id_estudante'], ['estudantes.id_estudante'], ),
    sa.ForeignKeyConstraint(['id_vaga'], ['vagas.id_vaga'], ),
    sa.PrimaryKeyConstraint('id_candidatura'),
    sa.UniqueConstraint('id_estudante', 'id_vaga', name='uq_candidatura_estudante_vaga')
    )

def downgrade():
    op.drop_table('candidaturas')
    op.drop_table('vagas')
    op.drop_table('solicitacoes_verificacao')
    op.drop_table('faculdades')
    op.drop_table('estudantes')
    op.drop_table('empresas')
    op.drop_table('users')