# Riscos e justificativas (critério T7)

| Risco | Impacto | Mitigação |
|---|---|---|
| Alertas demais (fadiga) | Ignorar incidente real | Só 3 alertas de sintoma com ação |
| HA sem banco externo | Dados e sessão inconsistentes | Banco gerenciado + réplica na proposta |
| DR nunca testado | RTO irreal | Testes mensais/trimestrais no plano |
| RPO agressivo demais | Custo alto | 15 min alinhado ao valor dos dados |
| Dependência de uma região | Queda total | Warm standby + DNS failover |
| Deploy queima error budget | Usuário impactado | Freeze + rollback (T6) acoplados aos alertas |

## Justificativa geral

A Biblioteca do laboratório demonstra o serviço; o T7 descreve como operá-la de forma **observável e recuperável**. As escolhas privilegiam sinais de experiência do usuário, HA zonal e DR com custo proporcional ao impacto acadêmico.
