# Painel mínimo proposto — Biblioteca

Ferramenta ilustrativa: **Grafana** (ou CloudWatch Dashboards / Datadog). O importante são os sinais, não a marca.

## Objetivo do painel

Em uma tela, o plantonista responde:

1. O serviço está saudável agora?
2. O usuário está sentindo erro ou lentidão?
3. Há saturação ou dependência falhando?
4. Houve deploy recente?

---

## Widgets obrigatórios

| # | Painel | O que mostra | Por quê |
|---|---|---|---|
| 1 | **Estado atual** | UP / DEGRADED / DOWN (agregado de health + erro) | Decisão imediata |
| 2 | **Volume (RPS)** | Reqisições/s de login e catálogo | Contextualiza os erros |
| 3 | **Taxa de erro** | % 5xx e falhas de autenticação servidor | SLI de sucesso |
| 4 | **Latência** | p50 / p95 / p99 de `/login` e catálogo | SLO de latência |
| 5 | **Saturação** | CPU, memória, threads / filas das instâncias | Explica causa |
| 6 | **Dependências** | Conexões/latência do banco; falhas de DNS/LB | Isola origem |
| 7 | **Eventos de deploy** | Marcadores de release no tempo | Correlação com regressão |
| 8 | **Comparação temporal** | Agora vs. mesma hora D-7 | Detecta anomalia relativa |

## Layout sugerido

```text
┌─────────────────┬─────────────────┬─────────────────┐
│ Estado atual    │ Volume (RPS)    │ Taxa de erro    │
├─────────────────┴─────────────────┴─────────────────┤
│ Latência p50 / p95 / p99  (+ linha do SLO 400 ms)   │
├───────────────────────────┬─────────────────────────┤
│ Saturação (CPU/mem)       │ Banco / dependências    │
├───────────────────────────┴─────────────────────────┤
│ Timeline com deploys + comparação D-7               │
└─────────────────────────────────────────────────────┘
  Links: traces · logs · runbook · error budget
```

## Links de investigação

- Do erro → explore de traces filtrado por `status=error`
- Do trace → logs com `trace_id` / `request_id`
- Do alerta → runbook correspondente em `docs/06-runbook.md`

## O que o painel deliberadamente não tem

- Dezenas de gráficos de microsserviços inexistentes
- Métricas de vanity sem ação
- Dados pessoais ou segredos JWT
