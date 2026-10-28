# Roteiro de apresentação — T7 (4–6 minutos)

**Equipe:** Diego Santos (RA 14523) · Wallace Gabriel (RA 14542)  
**Serviço:** Biblioteca (mesmo do T6)

---

## 1. Abertura (30 s)

> Proposta de observabilidade, alta disponibilidade e DR para a Biblioteca: detectar sintoma, resistir a falha de instância/zona e recuperar com RPO/RTO explícitos.

Mostrar: diagrama em `diagramas/arquitetura.md`.

---

## 2. SLOs principais (45 s)

- Disponibilidade **99,9%** / 30 dias (login + catálogo)
- Latência **p95 &lt; 400 ms** / 30 dias
- Citar 3+ SLIs rapidamente (sucesso login, sucesso API, latência, health)

---

## 3. Painel e alertas (60 s)

- Painel: estado, volume, erro, latência, saturação, banco, deploys
- 3 alertas com ação: erro, latência, burn/health → runbook

---

## 4. HA (45 s)

- 2 zonas, ≥2 réplicas, LB com health
- Banco gerenciado (H2 não serve para HA)
- Failover de instância automático via LB

---

## 5. RPO/RTO + DR (60 s)

- **RPO 15 min** · **RTO 1 h**
- Estratégia: **warm standby**
- Backup isolado + testes periódicos

---

## 6. Runbook (30 s)

- Sintoma erro alto → verificar deploy → rollback / drenar instância / DR

---

## 7. Fechamento

> O plano é executável sob pressão: cada alerta tem ação e o DR tem números justificados.

---

## Perguntas frequentes

**Por que não multi-região ativo/ativo?** Custo/complexidade vs. impacto do serviço.  
**Por que abandonar H2 na proposta?** Memória = RPO efetivo zero só enquanto o processo vive; reinício perde tudo.  
**Como liga no T6?** Sinal de degradação e rollback alimentam os alertas e o error budget.
