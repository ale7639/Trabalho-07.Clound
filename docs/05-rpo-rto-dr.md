# RPO, RTO e estratégia de DR — Biblioteca

## Classificação do impacto

Perda prolongada do catálogo e do login impede uso acadêmico/demo e cadastros.  
Dados de livros/autores/usuários têm valor operacional, mas não são transações financeiras — isso orienta RPO/RTO **moderados**, não “zero downtime global”.

---

## RPO — Recovery Point Objective

| Campo | Valor |
|---|---|
| **RPO** | **15 minutos** |
| Significado | Em um desastre, admite-se perder no máximo ~15 min de cadastros/alterações |
| Como atender | Snapshots / backup contínuo ou PITR do banco gerenciado com frequência ≤ 15 min; réplica assíncrona monitorada |
| Por que não 0 | RPO 0 exige sincronização síncrona multi-região (custo e latência altos demais para este serviço) |
| Por que não horas | Cadastros feitos em aula/demo seriam perdidos em volume inaceitável |

---

## RTO — Recovery Time Objective

| Campo | Valor |
|---|---|
| **RTO** | **1 hora** |
| Significado | Serviço de login + catálogo de volta em até 60 min após declaração de desastre |
| Como atender | Warm standby (ou piloto light) com imagens, IaC, DNS e runbook ensaiados |
| Por que não 5 min | Exigiria hot standby multi-região sempre ligado — custo fora do perfil acadêmico |
| Por que não 24 h | Interrompe aulas/demos por tempo demais; equipe consegue recuperar em ~1 h com plano testado |

```text
[dados perdidos ≤ 15 min] ---- desastre ---- [serviço restaurado ≤ 60 min]
         RPO                                      RTO
```

---

## Estratégia de DR escolhida: **Warm Standby**

| Estratégia | Uso neste trabalho |
|---|---|
| Backup e restore | Base mínima (atende RPO se restore couber no RTO — aqui é lento demais sozinho) |
| Pilot light | Núcleo mínimo na DR; escala na crise |
| **Warm standby** | **Escolhida:** ambiente reduzido sempre pronto na região secundária |
| Multi-site ativo/ativo | Descartada: complexidade e custo injustificados |

### Desenho warm standby

1. Região primária ativa (HA em 2 zonas)  
2. Região DR com capacidade reduzida (app + banco a partir de réplica/backup)  
3. DNS com failover manual ou automatizado após validação  
4. Backups isolados (outra conta/região) testados periodicamente  
5. Runbook e comunicação pré-definidos  

### Papéis na crise

- **Detectar** → alerta Sev-1 / health global  
- **Declarar desastre** → coordenador (critério: região primária irrecuperável em &lt; RTO)  
- **Ativar DR** → promover banco, subir capacidade, apontar DNS  
- **Validar** → `/login`, catálogo, health  
- **Comunicar** → status para equipe/professor  
- **Retornar** → failback planejado após estabilização  

---

## Testes de DR (obrigatórios no plano)

| Teste | Frequência sugerida | Métrica |
|---|---|---|
| Restore de snapshot em ambiente isolado | Mensal | Tempo real ≤ RTO; dados ≤ RPO |
| Failover de banco (staging) | Trimestral | Tempo de promoção |
| Simulação de ativação warm standby | Semestral | Checklist do runbook completo |

Backup **não testado** não conta como estratégia de DR.
