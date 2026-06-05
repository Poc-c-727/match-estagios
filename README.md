# Match estágios

Este repositório contém um banco de dados configurado para rodar em container **Docker** e uma aplicação web desenvolvida em **Flask** executada localmente.

##  Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
* [Docker](https://docs.google.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Poetry](https://python-poetry.org/)


## Como subir o ambiente

Siga os passos abaixo para clonar e executar o projeto localmente.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/litaglk/match-estagios](https://github.com/litaglk/match-estagios)
cd match-estagios
```

### 2. Construir e iniciar o container do banco de dados
Execute o comando abaixo para baixar as imagens necessárias, construir e iniciar o container do banco de dados:
```bash
docker-compose up --build
```

> **Dica:** Se quiser rodar o container em segundo plano (liberando o terminal), adicione a flag `-d`:
> ```bash
> docker-compose up --build -d
> ```

### 3. Subir a aplicação Flask (Local)
Em um novo terminal na pasta raiz do projeto, use o Poetry para instalar as dependências e iniciar o servidor do Flask:
```bash
# Instalar as dependências do projeto
poetry install

# Ativar o ambiente e rodar o Flask
poetry run flask run
```
*(Caso prefira usar o shell do Poetry para ativar o ambiente virtual diretamente, você também pode rodar `poetry shell` seguido de `flask run`)*

A aplicação estará disponível em: `http://localhost:5000` (ou na porta configurada no seu ambiente).


## Comandos úteis de gerenciamento

### Parar o container do banco de dados
Se você subiu o banco em segundo plano (`-d`), use este comando para pará-lo:
```bash
docker-compose down
```

### Parar o container removendo os volumes
Caso queira resetar o banco de dados completamente (apagando todos os dados persistidos nos volumes):
```bash
docker-compose down -v
```

### Ver logs do banco de dados
Útil para acompanhar as conexões e debugar erros na inicialização do banco de dados em tempo real:
```bash
docker-compose logs -f
```

### Acessar o terminal do container do banco
Se precisar rodar comandos direto dentro do container do banco de dados (como queries manuais ou checagem de tabelas):
```bash
docker-compose exec mariadb bash
```
