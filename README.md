```markdown
# AcreBot 🤖🌿
Bot IRC para o canal **#Acre** na rede **Rizon**.

O AcreBot é um bot simples porém poderoso escrito em **Python**, projetado para:

- moderar o canal
- criar interações divertidas
- registrar logs
- permitir comandos customizados
- manter ranking de karma entre usuários

Ele foi construído para ser **leve, extensível e fácil de modificar**.
<img width="705" height="535" alt="image" src="https://github.com/user-attachments/assets/d2650706-d3b4-4172-874c-a8db8844fbcd" />

---
<img width="739" height="513" alt="image" src="https://github.com/user-attachments/assets/cd9055b8-a622-4dba-a03f-dc1f93e2f08b" />

# Funcionalidades
<img width="747" height="523" alt="image" src="https://github.com/user-attachments/assets/e0b9e952-4cd4-4749-85a0-4fb38a61395b" />

## 🎮 Mini-jogos

### Dado
```

!dado

```

Exemplo:

```

walbarellos rolou 4

```

---

### Moeda
```

!moeda

```

Resultado:

```

cara
ou
coroa

```

---

### Número aleatório
```

!numero

```

Resultado:

```

Número sorteado: 42

```

---

### Escolha aleatória
```

!escolhe pizza hamburguer sushi

```

Resposta:

```

Escolhi: sushi

```

---

# Sistema de Karma ⭐

Usuários podem dar ou remover karma.

### Aumentar karma
```

nick++

```

### Diminuir karma
```

nick--

```

### Ver karma
```

!karma nick

```

Exemplo:

```

Karma de walbarellos: 3

```

---

# Ranking de Karma

Mostra os usuários com mais karma.

```

!top

```

Exemplo:

```

Top karma:
walbarellos(10)
AcreBot(3)

```

---

# Sistema de Comandos Dinâmicos

Admins podem criar comandos diretamente pelo IRC.

### Criar comando

```

!addcmd regra Sem spam no canal.

```

### Usar comando

```

!regra

```

Resposta:

```

Sem spam no canal.

```

---

### Remover comando

```

!delcmd regra

```

---

# Moderação

Comandos disponíveis apenas para **administradores**.

### Dar operador
```

!op nick

```

### Kick
```

!kick nick

```

### Ban
```

!ban nick

```

---

# Proteções automáticas

## Anti-Flood

Se um usuário enviar muitas mensagens rapidamente:

```

KICK nick :Flood detectado

```

---

## Anti-Spam de links

Se alguém enviar muitos links:

```

KICK nick :Spam de links

```

---

# Boas-vindas automáticas

Quando alguém entra no canal:

```

🌿 Bem-vindo ao #Acre, nick! Amazônia brasileira.

```

---

# Logs do canal

Todas as mensagens são salvas em:

```

logs/acre.log

```

Exemplo:

```

walbarellos: !dado
AcreBot: walbarellos rolou 5

```

---

# Banco de dados

O bot usa **SQLite**.

Arquivo criado automaticamente:

```

bot.db

```

Tabelas:

### karma
```

nick
score

```

### commands
```

name
response

````

---

# Instalação

Requisitos:

- Python 3
- acesso ao IRC

Clone ou copie o bot.

Rodar:

```bash
python acrebot.py
````

O bot irá:

1. conectar na rede Rizon
2. entrar em **#Acre**
3. começar a responder comandos

---

# Estrutura do projeto

```
acrebot/
│
├─ acrebot.py
├─ bot.db
├─ logs/
│   └─ acre.log
└─ README.md
```

---

# Rede IRC

Servidor usado:

```
irc.rizon.life
```

Canal:

```
#Acre
```

---

# Administradores

Admins configurados no código:

```
ADMINS = ["walbarellos"]
```

Eles podem usar comandos de moderação e criar comandos.

---

# Futuras melhorias

Possíveis evoluções do bot:

* sistema de plugins
* painel web
* economia do canal
* trivia da Amazônia
* integração com IA
* estatísticas avançadas do canal
* anti-raid inteligente

---

# Licença

Uso livre para estudo, modificação e melhorias.

---

🌿 **AcreBot — um bot simples para fortalecer a comunidade do #Acre no IRC.**

```
```
