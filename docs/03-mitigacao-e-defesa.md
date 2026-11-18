# 3. Medidas de Mitigação e Hardening (Visão Blue Team)

Compreender como o ataque funciona é apenas metade do aprendizado em cibersegurança; a outra metade é saber **detectar, impedir e reduzir o impacto**.

---

## 3.1 Controles Gerais Contra Força Bruta

1. **Autenticação Multifator (MFA)**: mesmo que uma senha fraca seja descoberta, o atacante não conclui o login sem o segundo fator.
2. **Política de Senhas Fortes**: priorizar tamanho (12+ caracteres / *passphrases*) e bloquear senhas presentes em listas de vazamentos conhecidos (NIST SP 800-63B).
3. **Rate Limiting e Fail2ban**: limitar requisições por IP/usuário em janelas curtas de tempo e banir temporariamente IPs com excesso de falhas (`401`/`530`/`STATUS_LOGON_FAILURE`).
4. **Monitoramento e Alertas (SIEM)**: correlacionar picos de eventos de falha de autenticação seguidos de um sucesso (indicativo clássico de brute force bem-sucedido).

---

## 3.2 Mitigação por Serviço

### FTP (Porta 21)
- **Substituir por SFTP (SSH) ou FTPS**: evita credenciais e dados trafegando em texto claro.
- **Desabilitar login anônimo**: no `vsftpd.conf`, garantir `anonymous_enable=NO`.
- **Restringir usuários e chroot**: limitar quais contas locais podem usar FTP e isolar diretórios.
- **Fail2ban**: habilitar a jail `[vsftpd]` para bloquear IPs após N tentativas inválidas.

### Aplicações Web / DVWA (Porta 80/443)
- **Tokens Anti-CSRF por requisição**: exatamente como o DVWA faz no nível *High* (`user_token`), dificulta scripts simples de repetição.
- **Atraso progressivo (*Exponential Backoff*) e CAPTCHA**: aumentar o tempo de resposta ou exigir desafio humano após 3–5 falhas.
- **Bloqueio por IP + conta com moderação**: evitar bloqueio permanente automático que possa ser abusado para Negação de Serviço (DoS) contra usuários legítimos.
- **HTTPS obrigatório + HttpOnly/Secure nos cookies**: impede captura de sessão (`PHPSESSID`) na rede.

### SMB / Samba (Portas 139 / 445)
- **Não expor SMB à internet**: bloquear TCP `139` e `445` no firewall de borda; permitir acesso apenas via rede interna segmentada ou VPN.
- **Desabilitar SMBv1 e NTLMv1/LM**: exigir SMBv2/SMBv3 e NTLMv2 (ou Kerberos em Active Directory), além de habilitar **SMB Signing**.
- **Account Lockout Policy**: configurar limite de tentativas inválidas com tempo de reset automático (ex.: 5 tentativas -> bloqueio de 15 minutos) e monitorar eventos Windows (`4625` falha / `4740` lockout) ou logs do Samba (`/var/log/samba/`).
- **Princípio do menor privilégio**: remover compartilhamentos desnecessários e restringir permissões de leitura/escrita por grupo.
