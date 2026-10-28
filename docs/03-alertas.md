# Três alertas com ação — Biblioteca

Princípio: alertar por **sintoma sentido pelo usuário**, com ação clara e link ao runbook. Evitar fadiga.

---

## Alerta 1 — Taxa de erro elevada no catálogo/login

| Campo | Definição |
|---|---|
| **Nome** | `biblioteca-high-error-rate` |
| **Sintoma** | Usuário não autentica ou não consulta livros |
| **Condição** | Taxa de 5xx (login + catálogo) **> 2%** por **5 minutos** |
| **Severidade** | Sev-2 (alta) / Sev-1 se > 10% por 5 min |
| **Responsável** | Plantão de aplicação |
| **Ação imediata** | 1) Abrir painel · 2) Verificar deploy recente · 3) Seguir [runbook](06-runbook.md) (rollback se pós-deploy) |
| **Runbook** | `docs/06-runbook.md` — Falha de erro elevado |

---

## Alerta 2 — Latência degradada (quebra do SLO de latência)

| Campo | Definição |
|---|---|
| **Nome** | `biblioteca-latency-p95-breach` |
| **Sintoma** | Catálogo ou `/login` lentos |
| **Condição** | **p95 > 400 ms** por **10 minutos** (janela rolante) |
| **Severidade** | Sev-2 |
| **Responsável** | Plantão de aplicação + dados (se banco saturar) |
| **Ação imediata** | 1) Conferir saturação CPU/mem e latência do banco · 2) Traces das rotas lentas · 3) Escalar réplicas se carga; mitigar query/lock se banco |
| **Runbook** | Seção “Latência alta” no runbook |

---

## Alerta 3 — Consumo acelerado do error budget / health DOWN

| Campo | Definição |
|---|---|
| **Nome** | `biblioteca-error-budget-burn` / health crítico |
| **Sintoma** | Risco de estourar SLO 99,9% ou serviço indisponível |
| **Condição** | Burn rate **> 2×** do orçamento mensal em **1 h** **OU** `/api/health` falhando em **todas** as instâncias por **2 minutos** |
| **Severidade** | Sev-1 |
| **Responsável** | Plantão + coordenação (comunicação) |
| **Ação imediata** | 1) Congelar deploys · 2) Mitigar (failover LB / rollback / ativar DR se região) · 3) Comunicar stakeholders · 4) Abrir incidente |
| **Runbook** | Runbook + plano DR em `docs/05-rpo-rto-dr.md` |

---

## Complemento (não pagina sozinho)

CPU alta, disco ou tamanho de fila **explicam** causa, mas só disparam página se acompanharem sintoma de erro/latência/health.
