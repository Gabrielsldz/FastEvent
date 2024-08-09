
# FastEvent

FastEvent é uma API desenvolvida em Python usando FastAPI, projetada para gerenciar usuários e eventos com suporte a autenticação JWT, upload de imagens, e integração com Prisma e PostgreSQL.

## Instalação

Siga os passos abaixo para configurar e rodar o projeto localmente.

### 1. Clonar o Repositório

Primeiro, clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/Gabrielsldz/FastEvent.git
cd FastEvent
```

### 2. Instalar Dependências

Instale todas as dependências necessárias usando o `pip`:

```bash
pip install -r requirements.txt
```

### 3. Configurar o Prisma

#### 3.1 Gerar o Prisma

Após instalar as dependências, é necessário gerar o Prisma de acordo com o schema definido no projeto. Execute o seguinte comando:

```bash
prisma generate
```

#### 3.2 Configurar o Banco de Dados

O banco de dados padrão utilizado é o PostgreSQL, mas você pode alterá-lo conforme necessário. Para configurar a conexão com o banco de dados, edite o arquivo `schema.prisma` na seção `datasource db`:

```prisma
datasource db {
  provider = "postgres"
  url      = "postgres://<USERNAME>:<PASSWORD>@localhost:5432/<DATABASE_NAME>"
}
```

Substitua `<USERNAME>`, `<PASSWORD>`, e `<DATABASE_NAME>` pelos valores correspondentes ao seu ambiente. Para mais detalhes sobre as opções de configuração do Prisma, consulte a [documentação oficial](https://www.prisma.io/docs/orm/overview/databases).

### 4. Preparar o Banco de Dados

Com o banco de dados configurado e em execução, crie as tabelas necessárias usando o comando:

```bash
prisma db push
```

Esse comando sincroniza o esquema do Prisma com o banco de dados, criando as tabelas e estruturas conforme definido no schema.

### 5. Rodar o Back-End

Agora que tudo está configurado, você pode iniciar o servidor back-end:

```bash
python main.py
```

O servidor estará rodando e pronto para receber requisições.

---
