# 1. Fundamentos Teóricos, Ética e Escopo

## 1.1 O que é um ataque de Força Bruta (Brute Force)?

Um ataque de **força bruta** consiste em testar sistematicamente múltiplas combinações de credenciais (usuário e senha) até encontrar uma combinação aceita pelo serviço alvo.

Na prática de auditoria de segurança, existem variações importantes:

| Técnica | Como funciona | Vantagem / Risco |
| :--- | :--- | :--- |
| **Brute Force puro (Exaustivo)** | Testa todas as combinações possíveis de caracteres (`a`, `b`, ..., `zzz999`). | Cobre qualquer senha, mas cresce exponencialmente e é inviável para senhas longas. |
| **Ataque de Dicionário** | Testa listas prévias de palavras, senhas vazadas ou termos comuns (*wordlists*). | Muito mais rápido que força bruta pura; explora padrões humanos previsíveis. |
| **Password Spraying** | Testa **poucas senhas comuns** contra **muitos usuários** (ex.: `Empresa@2026` em 200 contas). | Evita acionar bloqueio de conta (*Account Lockout*) por tentativas repetidas em um único usuário. |
| **Credential Stuffing** | Reutiliza pares `email:senha` vazados de outros serviços. | Explora o hábito de reutilizar a mesma senha em vários sites. |

---

## 1.2 Por que senhas fracas ainda acontecem?

1. **Previsibilidade humana**: datas de aniversário, nomes, sequências de teclado (`qwerty`, `123456`).
2. **Credenciais padrão (Default Credentials)**: serviços instalados com `admin:admin`, `msfadmin:msfadmin` ou `root:toor`.
3. **Ausência de controles compensatórios**: falta de MFA, ausência de *rate limiting* e falta de monitoramento de logs.

---

## 1.3 Ética, Legalidade e Ambiente Controlado

> [!CAUTION]
> Executar testes de força bruta contra sistemas de terceiros sem **autorização formal e escopo definido** é crime (no Brasil, enquadrável na Lei 12.737/2012 e Art. 154-A do Código Penal) e viola políticas de uso aceitável de provedores e redes.

Boas práticas em laboratório e auditoria autorizada:

- **Rede isolada**: utilize VMs em rede interna/*Host-Only* ou containers Docker isolados, sem expor alvos vulneráveis na internet.
- **Controle de threads**: excesso de paralelismo (`-t`) pode derrubar serviços frágeis (Negação de Serviço acidental) ou travar contas válidas.
- **Registro de evidências**: em pentests reais, documente horário, IP de origem/destino, comando executado e impacto observado.

---

## 1.4 Anatomia de uma Wordlist

Uma *wordlist* é um arquivo texto com uma entrada por linha. No Kali Linux, listas clássicas ficam em `/usr/share/wordlists/` (como `rockyou.txt.gz` ou listas em `/usr/share/seclists/`).

Boas práticas para estudos:
- Comece com listas **enxutas e direcionadas** ao cenário (`wordlists/usuarios.txt` e `wordlists/senhas.txt`) para entender o comportamento da ferramenta sem gerar tráfego desnecessário.
- Use ferramentas como `crunch` (geração por padrões), `cewl` (palavras extraídas de páginas web) ou scripts próprios (como [scripts/gerar_wordlist.py](../scripts/gerar_wordlist.py)) para criar listas sob medida.
