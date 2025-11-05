# FootMind

Um projeto de software web que transforma a febre dos jogos de adivinhação diários em um desafio de adivinhação com temática de futebol, usando **Python**, **Flask** e **JavaScript** em uma arquitetura limpa e modular.

## ⚽ Visão Geral do Projeto

O **FootMind** é um hub de jogos diários de adivinhação com temática de futebol, inspirado no Wordle. O objetivo é testar o conhecimento do usuário sobre o mundo do futebol através de jogos interativos e desafiadores.

### ⚙️ Tecnologias Utilizadas

| Camada | Tecnologia | Função |
| :--- | :--- | :--- |
| **Backend** | Python 3.9+, Flask | Lógica de aplicação, roteamento e Controllers. |
| **Banco de Dados** | SQLite3, SQLAlchemy | Armazenamento leve e local dos dados de jogos e estatísticas. |
| **Frontend** | HTML5, Jinja2, CSS3 | Estrutura e estilização da interface. |
| **Interação** | JavaScript (ES6+), AJAX | Lógica de jogo no cliente e comunicação assíncrona com o servidor. |
| **Arquitetura** | MVC (Model-View-Controller) e Flask Blueprints | Separação de responsabilidades e modularização dos jogos. |

### 🏗️ Arquitetura e Estrutura

O projeto segue o padrão **Model-View-Controller (MVC)** e utiliza **Flask Blueprints** para modular a lógica de cada jogo. Além disso, implementa o padrão **Application Factory** para configuração flexível e testabilidade.

| Diretório/Arquivo | Camada MVC | Descrição |
| :--- | :--- | :--- |
| `app.py` | - | Application Factory e inicialização do Flask. |
| `run.py` | - | Ponto de entrada para execução da aplicação. |
| `config.py` | - | Variáveis de configuração (Secret Key, caminho do DB). |
| `extensions.py` | - | Extensões Flask (SQLAlchemy, etc.). |
| `database/` | **Model** | Arquivos de Banco de Dados (`footmind.db`) e scripts de inicialização. |
| `database/dbSetup.py` | **Model** | Script de inicialização do banco de dados. |
| `database/seed_players.py` | **Model** | Script para popular a tabela Player com dados de jogadores. |
| `models/` | **Model** | Modelos SQLAlchemy (User, Player, HistoryGame, UserGame). |
| `games/gameWordle/` | **Controller** / **Model** | Módulo do jogo FootWordle (Blueprint). |
| `games/gameWordle/controller.py` | **Controller** | Rotas e manipulação de requisições HTTP. |
| `games/gameWordle/model.py` | **Model** | Funções de acesso ao banco e lógica de negócio do jogo. |
| `static/` | **View** | Arquivos estáticos (CSS, JS, Imagens). |
| `static/css/` | **View** | Estilos CSS (globais e específicos por jogo). |
| `static/js/` | **View** | Scripts JavaScript (globais e específicos por jogo). |
| `templates/` | **View** | Templates Jinja2 (`base.html` e templates dos jogos). |

---

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o **FootMind** em sua máquina.

### 📋 Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonar o repositório)

### 1. Verificar Python e pip

Certifique-se de que o Python 3.9+ e o `pip` estão instalados:

```bash
python --version
pip --version
```

### 2. Clonar o repositório

```bash
git clone https://github.com/mateushaupt/FootMind
cd FootMind
```

### 3. Criar e Ativar Ambiente Virtual

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

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar o Flask (Variáveis de Ambiente)

#### **Windows (PowerShell):**

```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
```

#### **Windows (CMD/Prompt):**

```cmd
set FLASK_APP=app.py
set FLASK_ENV=development
```

#### **Linux / macOS (Bash):**

```bash
export FLASK_APP="app.py"
export FLASK_ENV="development"
```

> 💡 **Alternativa:** Você pode criar um arquivo `.env` na raiz do projeto com essas variáveis e usar `python-dotenv` para carregá-las automaticamente.

### 6. Inicializar o Banco de Dados

Execute o script de inicialização para criar as tabelas no banco de dados:

```bash
python database/dbSetup.py
```

**Saída esperada:**

```
✅ Banco de dados FootMind inicializado com sucesso!
Tabelas criadas: USER, PLAYER, HISTORY_GAMES, USER_GAMES
```

### 7. Popular o Banco de Dados com Jogadores

Execute o script de seed para popular a tabela `Player` com dados de jogadores de futebol:

```bash
python database/seed_players.py
```

**Saída esperada:**

```
✅ Adicionado: NEYMAR JR
✅ Adicionado: MESSI
✅ Adicionado: RONALDO
...
==================================================
✅ Seed concluído!
   📊 Jogadores adicionados: 10
   ⏭️  Jogadores pulados: 0
   📈 Total no banco: 10
==================================================
```

> ⚠️ **Importante:** O jogo FootWordle requer que existam jogadores no banco de dados. Sem executar este passo, o jogo não funcionará corretamente.

### 8. Executar o Servidor

```bash
flask run
```

**Saída esperada:**

```
 * Serving Flask app 'app.py'
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### 9. Acessar a Aplicação

Abra no navegador: 👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

Você verá a página inicial com os jogos disponíveis. Clique em **"Jogar Agora"** em qualquer jogo disponível

### 10. Encerrar o Servidor

Pressione `Ctrl + C` no terminal para parar o servidor.

Para sair do ambiente virtual:

```bash
deactivate
```
