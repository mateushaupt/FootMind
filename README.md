# FootMind

Um projeto de software web que transforma a febre dos jogos de adivinhação diários em um desafio de adivinhação com temática de futebol, usando **Python**, **Flask** e **JavaScript** em uma arquitetura limpa e modular.

## ⚽ Visão Geral do Projeto

O **FootMind** é um hub de jogos diários de adivinhação, onde a lógica de acerto é inspirada no Wordle e outros jogos parecidos. O objetivo é testar o conhecimento do usuário sobre o mundo do futebol.

### ⚙️ Tecnologias Utilizadas

| Camada | Tecnologia | Função |
| :--- | :--- | :--- |
| **Backend** | Python 3, Flask | Lógica de aplicação, roteamento e Controllers. |
| **Banco de Dados** | SQLite3 | Armazenamento leve e local dos dados de jogos e estatísticas. |
| **Frontend** | HTML5, Jinja2, CSS3 | Estrutura e estilização da interface. |
| **Interação** | JavaScript (ES6+), AJAX | Lógica de jogo no cliente e comunicação assíncrona com o servidor. |
| **Arquitetura** | MVC (Model-View-Controller) e Flask Blueprints | Separação de responsabilidades e modularização dos jogos. |

### 🏗️ Arquitetura e Estrutura

O projeto segue o padrão **Model-View-Controller (MVC)** e utiliza **Flask Blueprints** para modular a lógica de cada jogo.

| Diretório/Arquivo | Camada MVC | Descrição |
| :--- | :--- | :--- |
| `app.py` | - | Inicialização do Flask e registro dos *Blueprints*. |
| `config.py` | - | Variáveis de configuração (Secret Key, caminho do DB). |
| `core/games_logics.py` | **Model** / **Controller** | Lógica de jogo compartilhada (ex: função de checagem do palpite). |
| `database/` | **Model** | Arquivos de Banco de Dados (`footmind.db`) e *scripts* de inicialização. |
| `static/` | **View** | Arquivos estáticos (CSS, JS, Imagens). |
| `templates/` | **View** | Templates Jinja2 (`base.html` e templates dos jogos). |
| `games/game_wordle/` | **Controller** / **Model** | Módulo do primeiro jogo (Blueprint). |
| `games/game_wordle/controller.py` | **Controller** | Rotas e manipulação de requisições específicas do jogo. |
| `games/game_wordle/model.py` | **Model** | Funções de acesso ao SQLite (obter palavra do dia, salvar estatísticas). |

-----

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o **FootMind** em sua máquina.

### 1\. Verificar Python e pip

Certifique-se de que o Python 3.9+ e o `pip` (gerenciador de pacotes) estão instalados:

```bash
python --version
pip --version
```

### 2\. Clonar o repositório

```bash
git clone https://github.com/mateushaupt/FootMind
```

### 3\. Criar e Ativar Ambiente Virtual

#### **Criação (Apenas na primeira vez):**

```bash
python -m venv venv
```

#### **Ativação (Para cada nova sessão de terminal):**

| Sistema Operacional | Comando de Ativação |
| :--- | :--- |
| **Windows (PowerShell)** | `.\venv\Scripts\Activate.ps1` |
| **Windows (CMD/Prompt)** | `.\venv\Scripts\activate.bat` |
| **Linux / macOS (Bash)** | `source venv/bin/activate` |

> 💡 Após ativar, seu terminal deve mostrar `(venv)` no início da linha de comando.

### 4\. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 5\. Configurar o Flask (Variáveis de Ambiente)

#### **Windows (PowerShell):**

```bash
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
```

#### **Linux / macOS (Bash):**

```bash
export FLASK_APP="app.py"
export FLASK_ENV="development"
```

### 6\. Inicializar o Banco de Dados

```bash
python database/dbSetup.py
```

### 7\. Executar o Servidor

```bash
flask run
```

**Saída esperada:**

```
 * Serving Flask app 'app.py'
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Abra no navegador: 👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### 8\. Encerrar

Pressione `Ctrl + C` no terminal para parar o servidor.

Para sair do ambiente virtual:

```bash
deactivate
```
