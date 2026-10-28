# SLIs e SLOs — Biblioteca

## Operação crítica

Autenticação e consulta do catálogo (login + listagem de livros/autores).

## Experiência esperada

Em horário acadêmico/comercial, o estudante ou operador consegue:

1. Abrir `/login` e autenticar
2. Consultar livros/autores na interface ou via API com Bearer token
3. Receber resposta útil em menos de meio segundo na maioria das requisições

---

## SLIs (4 indicadores)

| # | SLI | Definição quantitativa | Sinal / fonte |
|---|---|---|---|
| 1 | **Disponibilidade do login** | Proporção de `GET /login` e `POST` de autenticação (web/API) com sucesso HTTP 2xx/3xx válido, excluindo 4xx de cliente | Métrica de sucesso no LB + app |
| 2 | **Taxa de sucesso da API de catálogo** | Proporção de requisições autenticadas a `/api/livros/**` e `/api/autores/**` sem erro 5xx | Métricas HTTP da aplicação |
| 3 | **Latência da consulta** | Percentil 95 da latência de consultas de catálogo e de `/login` | Histograma de latência |
| 4 | **Saúde do health check** | Proporção de sondas `GET /api/health` com status UP / HTTP 200 | Probe do LB + métrica dedicada |

> Os SLIs 1–3 refletem experiência do usuário. O SLI 4 é complementar para detecção rápida de falha total.

### Exclusões explícitas

- Tráfego inválido (4xx por credencial errada, token ausente, rota inexistente)
- Testes sintéticos de carga fora da janela (marcados com header/user-agent de probe, se aplicável)
- Janelas de manutenção anunciadas

---

## SLOs (2 objetivos)

| # | SLO | Meta | Janela | Error budget |
|---|---|---|---|---|
| A | **Disponibilidade combinada** | ≥ **99,9%** das requisições válidas de login + catálogo bem-sucedidas | 30 dias | ~43 minutos de falha/mês |
| B | **Latência** | **95%** das consultas de catálogo e aberturas de `/login` com latência **&lt; 400 ms** | 30 dias | 5% das req. podem exceder 400 ms |

### Como o error budget orienta decisões

- Consumo acelerado do orçamento → pausar deploys arriscados, priorizar confiabilidade
- Orçamento saudável → permitir mudanças com gates do T6
- Não se busca 100%: o custo seria desproporcional ao impacto acadêmico/demo

---

## Relação com o T6

O pipeline e o plano de rollback do T6 alimentam estes SLOs: promoção só ocorre se o deploy não queimar o error budget de forma anormal (sinal de degradação pós-deploy).
