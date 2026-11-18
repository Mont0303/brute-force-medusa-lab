# 4. Checklist de Preparação do Laboratório e Entrega

Este guia organiza o passo a passo para quando você for executar a prática e publicar o repositório no GitHub.

---

## Opção A — Laboratório com Máquinas Virtuais (Clássico do Curso)

1. **Atacante**: VM com **Kali Linux** (`nmap`, `medusa`, `smbclient`, `wordlists`).
2. **Alvo**: VM vulnerável em rede isolada (*Host-Only* / Rede Interna), como **Metasploitable 2** (possui FTP, HTTP/DVWA e Samba) ou uma VM dedicada com **DVWA**.
3. **Verificação inicial**:
   - Confirmar que ambas as VMs estão na mesma sub-rede isolada (`ip a`).
   - Testar conectividade com `ping -c 3 <IP_ALVO>`.

## Opção B — Laboratório Local com Docker (Leve, na própria máquina)

Como `docker` e `docker-compose` já estão disponíveis neste sistema, você também pode futuramente subir containers isolados em uma rede Docker dedicada (`internal: true`) contendo:
- Um servidor FTP vulnerável (ex.: `vsftpd` de laboratório);
- Um container **DVWA** (`vulnerables/web-dvwa`);
- Um container **Samba** de teste;
- Um container **Kali Linux** (`kalilinux/kali-rolling`) com `nmap` e `medusa` instalados para atacar apenas essa rede interna.

---

## Checklist Antes de Entregar o Desafio

- [ ] Assistir a todas as vídeo-aulas do módulo.
- [ ] Executar o `nmap` contra o alvo isolado e salvar o print em `images/01-nmap-scan.png`.
- [ ] Testar o cenário **FTP** com Medusa e salvar o print em `images/02-medusa-ftp.png`.
- [ ] Testar o cenário **Web / DVWA** (documentando cookies/parâmetros ou comparação entre níveis *Low* e *High*) e salvar o print em `images/03-dvwa-login.png`.
- [ ] Testar o cenário **SMB** (`smbnt`) e salvar o print em `images/04-medusa-smb.png`.
- [ ] Preencher as seções `[A preencher após execução]` no [README.md](../README.md) com os resultados reais observados no seu ambiente.
- [ ] Revisar se nenhuma senha real pessoal ou dado sensível foi incluído nos arquivos.
- [ ] Criar um repositório **público** no GitHub, fazer `git push` e enviar o link no botão **"Entregar Projeto"**.
