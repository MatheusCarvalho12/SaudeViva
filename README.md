# Sistema de Agendamento da Clínica SaúdeViva

Este é um sistema simples de agendamento de consultas médicas para a Clínica SaúdeViva, desenvolvido em Python com integração com a API da OpenAI.

## Descrição do Projeto

O sistema permite agendar, listar e cancelar consultas médicas através de uma interface de linha de comando (CLI). Ele utiliza a API da OpenAI para duas finalidades principais:
1.  Gerar mensagens de confirmação de agendamento de forma cordial e humanizada.
2.  Interpretar solicitações de agendamento em linguagem natural, extraindo dados como nome do paciente, data e horário.

As consultas são salvas localmente em um arquivo `data/consultas.json`.

## Como Executar Localmente

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Pré-requisitos

-   Python 3.10 ou superior
-   `pip` (gerenciador de pacotes do Python)

### 2. Instalação

**Clone o repositório:**
```bash
git clone https://github.com/MatheusCarvalho12/SaudeViva
cd <NOME_DO_DIRETORIO>
```

**Crie e ative um ambiente virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

**Instale as dependências:**
O projeto utiliza as bibliotecas listadas no arquivo `requirements.txt`. Para instalá-las, execute:
```bash
pip install -r requirements.txt
```

### 3. Configuração da API

Para que a integração com a OpenAI funcione, você precisa de uma chave de API.

**Crie o arquivo `.env`:**
Copie o arquivo de exemplo para criar seu próprio arquivo de configuração:
```bash
cp env.example .env
```

**Adicione sua chave de API:**
Abra o arquivo `.env` e substitua `coloque_sua_chave_aqui` pela sua chave da API da OpenAI:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Executando a Aplicação

Com tudo configurado, execute o seguinte comando no terminal:
```bash
python app.py
```

## Exemplos de Uso

Ao iniciar a aplicação, um menu principal será exibido:

```
--- MENU PRINCIPAL ---
1. Agendar consulta
2. Listar consultas
3. Cancelar consulta
4. Agendar por linguagem natural
5. Sair
```

-   **Opção 1:** Pede o nome do paciente, data (YYYY-MM-DD) e horário (HH:MM) para um novo agendamento.
-   **Opção 2:** Exibe todas as consultas marcadas e canceladas.
-   **Opção 3:** Lista as consultas ativas e permite cancelar uma pelo seu ID.
-   **Opção 4:** Permite que você digite um pedido em linguagem natural, como:
    -   `"Quero marcar consulta para João amanhã às 10h"`
    -   `"Agendar Maria para sexta-feira às 14:30"`
-   **Opção 5:** Encerra a aplicação.
