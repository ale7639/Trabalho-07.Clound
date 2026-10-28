# Estratégia de alta disponibilidade — Biblioteca

## Objetivo

Manter autenticação e consulta do catálogo disponíveis diante de falha de **uma instância** ou **uma zona**, sem intervenção manual demorada.

## Decisões

| Tema | Escolha | Justificativa |
|---|---|---|
| Escalabilidade | **Horizontal** (≥ 2 réplicas) | Redundância + capacity; JWT favorece stateless na API |
| Distribuição | **2 zonas** na região primária | Sobrevive a falha zonal |
| Entrada | Load balancer com health check em `/api/health` e `/login` | Só encaminha a destinos saudáveis |
| Dados | Banco **gerenciado** com failover automático + réplica | H2 em memória é ponto único e perde dados |
| Detecção | Probes + alertas de sintoma | Failover automático da app via LB; banco via mecanismo do provedor |
| Autoscaling | Mín. 2 · máx. definido · sinal CPU/RPS/latência | Evita saturação sem custo ilimitado |

## Remoção de pontos únicos de falha

```text
Antes (lab):  1 Pod + H2 memória     → qualquer reinício apaga dados / derruba tudo
Depois (HA):  LB → N instâncias/zonas → banco gerenciado + réplica + backups
```

## Resiliência na aplicação

- Timeouts em chamadas ao banco
- Retry limitado com backoff em erros transitórios
- Degradação graciosa: se escrita falhar, manter leitura via réplica quando seguro
- Circuit breaker para dependências futuras (ex.: serviço externo de e-mail)

## Failover

| Cenário | Detecção | Ação | Tempo-alvo |
|---|---|---|---|
| Instância unhealthy | Probe do LB | LB retira do pool; orquestrador recria | segundos |
| Zona A indisponível | Health / métricas | Tráfego só na Zona B | minutos |
| Primário do banco falha | Monitor do provedor | Failover para standby | minutos (conforme SLA do banco) |

## Testes mínimos de HA

1. Derrubar uma réplica e confirmar que `/login` segue OK  
2. Simular latência no banco e observar alerta de p95  
3. Validar que o LB não envia tráfego a Pod `READY 0/1`

## Custo × benefício

HA aumenta custo (réplicas, LB, banco gerenciado) e complexidade. Para o serviço Biblioteca acadêmico, **2 zonas + banco gerenciado** é o ponto de equilíbrio entre nota de resiliência e viabilidade.
