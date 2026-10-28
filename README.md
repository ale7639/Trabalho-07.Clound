# Trabalho 7 — Observabilidade, Alta Disponibilidade e DR

**Disciplina:** Cloud Computing e DevOps Avançado (UniALFA)  
**Tema:** Observabilidade, disponibilidade e recuperação  
**Valor:** até 1,0 ponto  
**Base (T6):** serviço **Biblioteca** (Spring Boot / Java 21)  
**Equipe:** Diego Santos (RA 14523) · Wallace Gabriel (RA 14542)  
**Repositório:** https://github.com/ale7639/Trabalho-07.Clound

---

## Entregáveis

| # | Entregável | Onde está |
|---|---|---|
| 1 | Diagrama da arquitetura | [`diagramas/arquitetura.md`](diagramas/arquitetura.md) |
| 2 | Três ou mais SLIs | [`docs/01-slis-slos.md`](docs/01-slis-slos.md) |
| 3 | Dois SLOs | [`docs/01-slis-slos.md`](docs/01-slis-slos.md) |
| 4 | Painel mínimo proposto | [`docs/02-painel.md`](docs/02-painel.md) |
| 5 | Três alertas com ação | [`docs/03-alertas.md`](docs/03-alertas.md) |
| 6 | Estratégia de alta disponibilidade | [`docs/04-alta-disponibilidade.md`](docs/04-alta-disponibilidade.md) |
| 7 | RPO e RTO justificados | [`docs/05-rpo-rto-dr.md`](docs/05-rpo-rto-dr.md) |
| 8 | Estratégia de DR | [`docs/05-rpo-rto-dr.md`](docs/05-rpo-rto-dr.md) |
| 9 | Runbook resumido de uma falha | [`docs/06-runbook.md`](docs/06-runbook.md) |
| — | PDF consolidado | [`entregas/T7_Observabilidade_HA_DR.pdf`](entregas/T7_Observabilidade_HA_DR.pdf) |
| — | Roteiro de apresentação | [`entregas/APRESENTACAO.md`](entregas/APRESENTACAO.md) |

---

## Operação crítica escolhida

**Consulta e autenticação do catálogo da Biblioteca**

- Login web (`/login`) e API (`/api/auth/login`)
- Consulta de livros e autores (web + API autenticada)
- Health check (`/api/health`)

Experiência esperada: o usuário autentica e consulta o catálogo com baixa latência e baixa taxa de erro, mesmo sob falha de uma zona ou de uma instância.

---

## Visão rápida

- **SLOs:** disponibilidade 99,9% (30 dias) e latência p95 &lt; 400 ms (30 dias)
- **HA:** 2 zonas, ≥2 réplicas atrás de LB, banco gerenciado com réplica
- **DR:** Warm standby em outra região · **RPO 15 min** · **RTO 1 h**
- **Stack de observação proposta:** métricas + logs estruturados + traces (ex.: Grafana/CloudWatch/OpenTelemetry)

---

## Enunciado

https://github.com/dpRanghetti/UniALFA/blob/master/Cloud%20Computing%20e%20DevOps%20Avan%C3%A7ado/aula_12_observabilidade_alta_disponibilidade_dr.md
