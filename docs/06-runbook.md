# Runbook resumido — Falha: taxa de erro elevada / login e catálogo indisponíveis

**Alerta associado:** `biblioteca-high-error-rate` (e/ou health DOWN)  
**Severidade típica:** Sev-2 → Sev-1 se total  

---

## 1. Sintoma

- Usuários não conseguem autenticar em `/login` ou `/api/auth/login`
- Consultas de livros/autores retornam 5xx
- Painel: taxa de erro &gt; 2% ou health vermelho

---

## 2. Verificações rápidas (≤ 5 min)

1. Abrir o **painel mínimo** — estado, erro, latência, deploy recente  
2. `GET /api/health` em cada instância / via LB  
3. Logs recentes filtrados por `level=ERROR` e `trace_id`  
4. Status do **banco** (conexões, failover, CPU/storage)  
5. Houve **deploy** nos últimos 30–60 minutos?  

---

## 3. Ações seguras (mitigação)

| Ordem | Condição | Ação |
|---:|---|---|
| 1 | Deploy recente correlacionado | **Rollback** para a versão anterior (plano T6) |
| 2 | Uma instância/zona só falha | Remover do LB / drenar; manter as saudáveis |
| 3 | Banco saturado ou failover | Verificar standby; reduzir carga; escalar leitura se aplicável |
| 4 | Saturação de app (CPU/RPS) | Subir réplicas dentro do máx. do autoscaling |
| 5 | Região primária inviável | Declarar incidente Sev-1 e seguir **DR warm standby** (`docs/05-rpo-rto-dr.md`) |

Evitar: reiniciar tudo sem diagnóstico; mudar config sensível sem registro; “fix” infinito.

---

## 4. Escalonamento

- **15 min** sem mitigação clara → acionar segundo plantonista / responsável de dados  
- **Indício de perda de região** → coordenador de DR  
- Comunicação: canal da equipe + status breve (“investigando / mitigando / recuperado”)

---

## 5. Reversão / estabilização

- Confirmar erro &lt; 1% e p95 &lt; 400 ms por **15 minutos**
- Manter freeze de deploy até error budget estável
- Registrar timeline do incidente

---

## 6. Comunicação (modelo curto)

> Incidente Biblioteca: impacto em login/catálogo. Mitigação: &lt;rollback|failover|scale&gt;. Próximo update em 15 min.

---

## 7. Pós-incidente (aprender)

- Causa raiz (1 parágrafo)
- O alerta foi cedo o bastante?
- O runbook faltou algum passo?
- Ação preventiva (teste, limite, gate de CI/CD)

---

## Anexo — Latência alta (alerta 2)

1. Traces das rotas lentas  
2. Latência do banco vs. app  
3. Se app: escalar / otimizar endpoint  
4. Se banco: índices, locks, failover, capacity  
5. Se pós-deploy: rollback  
