# 2. Reconhecimento com Nmap e Auditoria com Medusa

## 2.1 Fase 1 — Reconhecimento com Nmap

Antes de testar credenciais, o auditor precisa confirmar **quais portas estão abertas** e **quais serviços e versões** estão respondendo no alvo.

```bash
# Varredura direcionada às portas dos 3 cenários (FTP, HTTP, SMB) com detecção de versão
nmap -sV -sC -p 21,80,139,445 <IP_DO_ALVO>
```

Explicação das flags:
- `-sV`: identifica a versão do serviço (ex.: `vsftpd 2.3.4`, `Apache httpd`, `Samba smbd`).
- `-sC`: executa scripts padrão do NSE (ex.: verifica `ftp-anon` para login anônimo no FTP ou enumeração básica SMB).
- `-p 21,80,139,445`: restringe às portas de interesse para manter o scan rápido e limpo.

---

## 2.2 Anatomia do Medusa

O **Medusa** ([documentação oficial](http://www.foofus.net/jmk/medusa/medusa.html)) é um auditor de login paralelo baseado em *pthreads* e módulos independentes (`.mod`).

Comandos de descoberta da própria ferramenta:

```bash
# Listar todos os módulos instalados
medusa -d

# Ver opções específicas de um módulo (ex.: smbnt ou web-form)
medusa -M smbnt -q
medusa -M web-form -q
```

Flags principais:

| Flag | Significado | Exemplo |
| :--- | :--- | :--- |
| `-h` / `-H` | Host único ou arquivo com lista de hosts | `-h 192.168.56.101` |
| `-u` / `-U` | Usuário único ou arquivo de usuários | `-U wordlists/usuarios.txt` |
| `-p` / `-P` | Senha única ou arquivo de senhas | `-P wordlists/senhas.txt` |
| `-C` | Arquivo combo no formato `host:usuario:senha` | `-C combo.txt` |
| `-M` | Módulo do serviço alvo (`ftp`, `http`, `web-form`, `smbnt`) | `-M ftp` |
| `-m` | Parâmetros específicos do módulo | `-m GROUP:LOCAL` |
| `-n` | Porta TCP customizada (quando diferente da padrão) | `-n 8080` |
| `-t` | Número de threads simultâneas por host | `-t 4` |
| `-f` | Para o ataque no host assim que encontrar a primeira credencial válida | `-f` |
| `-e` | Checagens extras: `n` (senha vazia), `s` (senha igual ao usuário) | `-e ns` |
| `-O` | Grava a saída em arquivo de log | `-O resultado.log` |

---

## 2.3 Cenário 1 — FTP (Porta 21)

### Como funciona o protocolo
O **FTP** (*File Transfer Protocol*) autentica com comandos `USER` e `PASS` em **texto claro** (sem criptografia), o que facilita tanto interceptação na rede quanto testes automatizados em serviços mal configurados.

### Comando base no Medusa

```bash
# Testando usuário específico com wordlist de senhas
medusa -h <IP_ALVO> -u msfadmin -P wordlists/senhas.txt -M ftp -t 4 -f

# Testando lista de usuários x lista de senhas + senha vazia/igual ao usuário
medusa -h <IP_ALVO> -U wordlists/usuarios.txt -P wordlists/senhas.txt -M ftp -e ns -t 4 -f
```

### Pontos para observar no laboratório
1. O servidor aceita login `anonymous` sem senha? (Verifique com `nmap --script ftp-anon -p 21 <IP_ALVO>`).
2. A conta `msfadmin` ou `ftpuser` aparece como `[SUCCESS]` na saída do Medusa?
3. Em ferramentas como Wireshark, todo o tráfego de autenticação aparece legível.

---

## 2.4 Cenário 2 — Web / DVWA (Porta 80)

### Diferença importante: `http` vs. `web-form`
Segundo a documentação oficial do Medusa:
- O módulo **`http`** testa autenticação a nível de protocolo HTTP (**Basic Auth**, **Digest** ou **NTLM/Windows Integrated**).
- O módulo **`web-form`** envia requisições **GET/POST** para formulários HTML de login (como a tela `/login.php` ou a seção `/vulnerabilities/brute/` do **DVWA**).

### O detalhe técnico do DVWA
No **DVWA** (*Damn Vulnerable Web Application*), existem dois contextos comuns de brute force:

1. **Página de ataque `/vulnerabilities/brute/` (nível `Low`)**:
   - Exige que o usuário já esteja autenticado com um cookie de sessão válido (`PHPSESSID=...` e `security=low`).
   - Envia parâmetros via `GET` (ex.: `username=...&password=...&Login=Login`).
   - Em níveis `Medium` e `High`, o DVWA adiciona **atraso na resposta** e **`user_token` (anti-CSRF)** que muda a cada requisição — o que impede ferramentas simples que não renovam o token a cada tentativa (bom ponto para documentar como defesa!).

2. **Autenticação HTTP Basic Auth (ou formulário `/login.php` sem token)**:
   - Se o alvo usar formulário POST sem token dinâmico, inspecione os nomes exatos dos campos no código HTML (`F12` -> Network -> payload do POST) e a mensagem de erro retornada pelo servidor (ex.: `Login failed` ou redirecionamento).

### Exemplo de uso com `web-form` (verifique as opções exatas do seu binário com `medusa -M web-form -q`)

```bash
# Inspecione primeiro os parâmetros exatos suportados pelo módulo web-form na sua versão do Medusa
medusa -M web-form -q
```

Exemplo típico de sintaxe do `web-form` (ajuste `FORM`, `USER-FIELD`, `PASS-FIELD` e `DENY-SIGNAL` conforme a resposta HTML real do seu DVWA e lembre-se de passar o cookie se estiver testando `/vulnerabilities/brute/`):

```bash
# Exemplo ilustrativo para formulário POST padrão sem CSRF token:
medusa -h <IP_ALVO> -u admin -P wordlists/senhas.txt -M web-form \
  -m FORM:"login.php" \
  -m FORM-DATA:"post?username=&password=&Login=Login" \
  -m DENY-SIGNAL:"Login failed"
```

> [!TIP]
> **Alternativa de estudo**: para o módulo `/vulnerabilities/brute/` do DVWA com `Cookie: PHPSESSID=<ID>; security=low`, muitas pessoas também comparam o **Medusa** (para formulários simples / HTTP Basic) com **Hydra** (`http-get-form` com header `H=Cookie:...`) ou **Burp Suite Intruder** (que lida nativamente com cookies e tokens CSRF via macro/pitchfork). Documentar essa limitação técnica do Medusa diante de tokens CSRF enriquece muito o seu relatório!

---

## 2.5 Cenário 3 — SMB (Portas 139 / 445)

### Como funciona o protocolo
O **SMB** (*Server Message Block*) / **Samba** permite compartilhamento de arquivos e impressoras em redes Windows e Linux. O módulo do Medusa para SMB é o **`smbnt`**, que testa a porta `445/tcp` por padrão e faz fallback para `139/tcp` (NetBIOS) se necessário.

### Parâmetros importantes do módulo `smbnt`
Conforme a documentação oficial:
- `GROUP:LOCAL` (padrão), `GROUP:DOMAIN` ou `GROUP:BOTH` — define se a autenticação é local ou contra controlador de domínio.
- `AUTH:NTLM` (padrão), `AUTH:LM`, `AUTH:LMv2` ou `AUTH:NTLMv2` — seleciona o método de desafio/resposta. Em servidores Samba/Windows modernos que recusam NTLMv1, `AUTH:NTLMv2` ou `AUTH:LMv2` pode ser necessário.
- `PASS:PASSWORD` (padrão) ou `PASS:HASH` — permite testar senhas em texto ou hashes NTLM (*Pass-the-Hash*).

### Comando base no Medusa

```bash
# Testando usuários e senhas contra SMB local na porta 445
medusa -h <IP_ALVO> -U wordlists/usuarios.txt -P wordlists/senhas.txt -M smbnt -m GROUP:LOCAL -t 4 -f

# Caso o servidor exija NTLMv2:
medusa -h <IP_ALVO> -U wordlists/usuarios.txt -P wordlists/senhas.txt -M smbnt -m AUTH:NTLMv2 -t 4 -f
```

### Validação pós-descoberta (apenas em laboratório)
Após identificar uma credencial válida no SMB, você pode confirmar o acesso aos compartilhamentos com:

```bash
smbclient -L //<IP_ALVO> -U <usuario>
```
