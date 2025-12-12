# Fleshi — Aplicação Web de Exibição de Fotos

Aplicação web desenvolvida permitindo registro de usuários, login social (Google, etc.) e compartilhamento de fotos em um feed social realizado nas dependências do SENAI sob tutoria do docente [Lincoln Souza](https://github.com/souzalb).

Projeto ideal para demonstrar domínio de arquitetura MVC/MVT, segurança de autenticação (Local + OIDC) e persistência de dados.

## 📚 Sumário

- [Visão Geral](#visão-geral)
- [Layout do Projeto](#layout-do-projeto)
- [Vídeo do Projeto](#vídeo-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Como Usar](#como-usar)
- [Tecnologias](#tecnologias)
- [Licença](#licença)

##  🔎 Visão Geral

Este projeto é uma aplicação de rede social simplificada desenvolvida com o micro-framework **Flask** em Python.

Ele se destaca por seu sistema de autenticação híbrida, que gerencia usuários locais (com hash Bcrypt) e usuários externos (Auth0 via OpenID Connect), garantindo uma experiência de login moderna e segura. Os dados dos usuários e das fotos são persistidos em um banco de dados **SQLite** gerenciado pelo **SQLAlchemy**.

## 🧩 Layout do Projeto

![Imagem final do Projeto](https://)

## ▶️ Vídeo do Projeto

- Acesse o vídeo do projeto para melhor visualização: [https://drive.google.com/file/d/10P7AhgsQbFG2cn5iKK3KZPS8oRwnlV_7/view?usp=sharing](https://drive.google.com/file/d/10P7AhgsQbFG2cn5iKK3KZPS8oRwnlV_7/view?usp=sharing)


## ✨ Funcionalidades

- **Autenticação Dupla:** Login e Registro com e-mail/senha (local) ou Login Social (SSO) via Auth0.
- **Segurança OIDC:** Uso de `prompt=login` para forçar a reautenticação no provedor externo, evitando problemas de cache de sessão (Google).
- **Gerenciamento de Fotos:** Upload de arquivos e exibição de feed global.
- **Perfis de Usuário:** Visualização de perfil próprio e de terceiros com histórico de fotos.
- **Validação de Formulários:** Uso de Flask-WTF para validação de dados e verificação de unicidade (e-mail e nome de usuário).
- **Persistência de Usuário Auth0:** Criação automática de um perfil local para usuários externos. 

## 📁 Estrutura de Pastas

```
/appfleshi
  /__init__.py     
  /routes.py      
  /models.py        
  /forms.py         
  /create_database.py 
  /static
    /posts_photos   
    /templates 
  datafleshi.db    
  .env               
  README.md
```

## 🚀 Como Usar

1. Clone o repositório:  
   ```bash
   git clone https://github.com/AlbertZiurk/fleshi
    ```
2. Compile o projeto:
   ```bash
    pip install -r requirements.txt
    ```
3. Crie o banco de dados:
   ```bash
    python create_database.py
    ```
4. Crie um projeto no https://auth0.com/:
   ```bash
    Defina como Regular Web Application o tipo da aplicação 
    ```
5. Entre na aba "Settings" da aplicaçã:
   ```bash
    Configure o Allowed Callback URLs (http://localhost:5000/callback)
    Configure o Allowed Logout URLs (http://localhost:5000/logout,http://localhost:5000/)
    ```
6. Configure as credenciais do Auth0 no arquivo `.env`:
   ```env
    # Variáveis críticas de Autenticação Auth0
    AUTH0_DOMAIN="dev-seu-dominio.us.auth0.com" 
    AUTH0_CLIENT_ID="SEU_CLIENT_ID_AQUI"
    AUTH0_CLIENT_SECRET="SEU_CLIENT_SECRET_AQUI"
    
    # URLs de Redirecionamento configuradas no Auth0
    AUTH0_CALLBACK_URL="http://localhost:5000/callback"
    AUTH0_LOGOUT_URL="http://localhost:5000/logout"
    ```
7. Execute a aplicação:
   ```bash
    python run.py 
    ```

## 🛠 Tecnologias

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![Auth0](https://img.shields.io/badge/Auth0-EB5424?style=for-the-badge&logo=auth0&logoColor=white)

![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-333333?style=for-the-badge&logo=sqlalchemy&logoColor=white)

![Flask-Bcrypt](https://img.shields.io/badge/Flask%20Bcrypt-000000?style=for-the-badge&logo=bcrypt&logoColor=white)

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)

![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

![Bootstrap](https://img.shields.io/badge/bootstrap-%238511fa.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## 📄 Licença
Este projeto está licenciado sob a MIT. 

![MIT License](https://img.shields.io/badge/License-MIT-green.svg)
