#!/usr/bin/env python3
"""Gera o PDF consolidado do Trabalho 7."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path(__file__).resolve().parents[1] / "entregas" / "T7_Observabilidade_HA_DR.pdf"


def styles():
    base = getSampleStyleSheet()
    return {
        "cover": ParagraphStyle("cover", parent=base["Title"], fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=10),
        "sub": ParagraphStyle("sub", parent=base["Normal"], fontSize=10, leading=14, alignment=TA_CENTER, spaceAfter=6),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontSize=13, leading=16, textColor=colors.HexColor("#0f2744"), spaceBefore=12, spaceAfter=6),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontSize=11, leading=14, textColor=colors.HexColor("#1a3a5c"), spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("body", parent=base["Normal"], fontSize=9, leading=12, alignment=TA_JUSTIFY, spaceAfter=5),
        "small": ParagraphStyle("small", parent=base["Normal"], fontSize=8, leading=10, spaceAfter=3),
        "cell": ParagraphStyle("cell", parent=base["Normal"], fontSize=7.5, leading=9.5),
        "code": ParagraphStyle("code", parent=base["Code"], fontName="Courier", fontSize=7.5, leading=9.5, backColor=colors.HexColor("#f4f6f8"), spaceAfter=6),
    }


def P(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=6) for i in items],
        bulletType="bullet",
        leftIndent=12,
        spaceAfter=6,
    )


def table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2744")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa7b5")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2f6")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def build():
    s = styles()
    story = []

    story.append(Spacer(1, 2 * cm))
    story.append(P("Trabalho 7 — Observabilidade,<br/>Alta Disponibilidade e Recuperação de Desastres", s["cover"]))
    story.append(P("Serviço-base: Biblioteca (Spring Boot) — mesmo serviço do T6", s["sub"]))
    story.append(Spacer(1, 0.6 * cm))
    story.append(P("Cloud Computing e DevOps Avançado · UniALFA · Aula 12", s["sub"]))
    story.append(P("<b>Diego Santos</b> RA 14523 · <b>Wallace Gabriel</b> RA 14542", s["sub"]))
    story.append(Spacer(1, 0.8 * cm))
    story.append(P("https://github.com/ale7639/Trabalho-07.Clound", s["sub"]))
    story.append(PageBreak())

    story.append(P("1. Objetivo e escopo", s["h1"]))
    story.append(
        P(
            "Propor uma arquitetura observável e resiliente para a Biblioteca: SLIs/SLOs, painel, alertas com ação, "
            "alta disponibilidade, RPO/RTO, estratégia de DR e runbook. A operação crítica é autenticação e consulta do catálogo.",
            s["body"],
        )
    )

    story.append(P("2. Diagrama da arquitetura", s["h1"]))
    story.append(
        P(
            "Usuários → DNS → Load Balancer → instâncias da Biblioteca em Zona A e Zona B → banco gerenciado "
            "(primário + réplica) → backup isolado e região DR (warm standby). Observabilidade (métricas, logs, traces) "
            "alimenta alertas e runbooks. H2 em memória permanece apenas no laboratório; a proposta operacional usa banco externo.",
            s["body"],
        )
    )
    story.append(
        P(
            "DNS → LB → [Zona A app | Zona B app] → DB primário ↔ réplica → backups → região DR<br/>"
            "app/DB/LB → Observabilidade → Alertas/Runbooks",
            s["code"],
        )
    )

    story.append(P("3. SLIs (4) e SLOs (2)", s["h1"]))
    story.append(
        table(
            [
                [P("<b>SLI</b>", s["cell"]), P("<b>Definição</b>", s["cell"])],
                [P("Disponibilidade do login", s["cell"]), P("Sucesso de /login e autenticação API (exclui 4xx de cliente)", s["cell"])],
                [P("Sucesso da API de catálogo", s["cell"]), P("Requisições autenticadas a livros/autores sem 5xx", s["cell"])],
                [P("Latência da consulta", s["cell"]), P("p95 de catálogo e /login", s["cell"])],
                [P("Health check", s["cell"]), P("GET /api/health com HTTP 200 / UP", s["cell"])],
            ],
            [5 * cm, 12 * cm],
        )
    )
    story.append(Spacer(1, 0.25 * cm))
    story.append(
        table(
            [
                [P("<b>SLO</b>", s["cell"]), P("<b>Meta</b>", s["cell"]), P("<b>Janela</b>", s["cell"])],
                [P("Disponibilidade", s["cell"]), P("≥ 99,9% req. válidas com sucesso", s["cell"]), P("30 dias (~43 min de budget)", s["cell"])],
                [P("Latência", s["cell"]), P("95% das consultas &lt; 400 ms", s["cell"]), P("30 dias", s["cell"])],
            ],
            [4 * cm, 7.5 * cm, 5.5 * cm],
        )
    )

    story.append(P("4. Painel mínimo", s["h1"]))
    story.append(
        bullets(
            [
                "Estado atual (UP/DEGRADED/DOWN)",
                "Volume (RPS), taxa de erro, latência p50/p95/p99",
                "Saturação (CPU/memória) e dependências (banco)",
                "Marcadores de deploy e comparação temporal (D-7)",
                "Links para traces, logs e runbook",
            ],
            s["body"],
        )
    )

    story.append(P("5. Três alertas com ação", s["h1"]))
    story.append(
        table(
            [
                [P("<b>Alerta</b>", s["cell"]), P("<b>Condição</b>", s["cell"]), P("<b>Ação</b>", s["cell"])],
                [
                    P("Erro elevado", s["cell"]),
                    P("5xx &gt; 2% por 5 min", s["cell"]),
                    P("Painel → deploy? → rollback / drenar instância (runbook)", s["cell"]),
                ],
                [
                    P("Latência p95", s["cell"]),
                    P("p95 &gt; 400 ms por 10 min", s["cell"]),
                    P("Ver saturação e banco; escalar ou mitigar query; rollback se pós-deploy", s["cell"]),
                ],
                [
                    P("Burn / health DOWN", s["cell"]),
                    P("Burn &gt; 2× em 1 h ou health total falho 2 min", s["cell"]),
                    P("Freeze de deploy; mitigar; comunicar; ativar DR se região", s["cell"]),
                ],
            ],
            [3.5 * cm, 5.5 * cm, 8 * cm],
        )
    )

    story.append(PageBreak())
    story.append(P("6. Estratégia de alta disponibilidade", s["h1"]))
    story.append(
        bullets(
            [
                "Escalabilidade horizontal com mínimo 2 réplicas",
                "Duas zonas na região primária atrás de load balancer com health check",
                "Banco gerenciado com failover e réplica (substitui H2 em memória na proposta)",
                "Autoscaling com mínimo/máximo e sinais de CPU/RPS/latência",
                "Timeouts, retry limitado e degradação graciosa",
                "Testes: derrubar réplica, validar LB e alertas",
            ],
            s["body"],
        )
    )

    story.append(P("7. RPO, RTO e DR", s["h1"]))
    story.append(
        table(
            [
                [P("<b>Objetivo</b>", s["cell"]), P("<b>Valor</b>", s["cell"]), P("<b>Justificativa</b>", s["cell"])],
                [P("RPO", s["cell"]), P("15 minutos", s["cell"]), P("Cadastros recentes importam; RPO 0 é caro demais para o serviço", s["cell"])],
                [P("RTO", s["cell"]), P("1 hora", s["cell"]), P("Recuperação ensaiada com warm standby; hot multi-região injustificado", s["cell"])],
                [P("Estratégia DR", s["cell"]), P("Warm standby", s["cell"]), P("Ambiente reduzido pronto; DNS failover; backups isolados e testados", s["cell"])],
            ],
            [3.5 * cm, 3.5 * cm, 10 * cm],
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        P(
            "Backup sozinho não é DR. O plano inclui pessoas, comunicação, promoção de banco, validação de /login e catálogo, "
            "e testes periódicos de restore/failover.",
            s["body"],
        )
    )

    story.append(P("8. Runbook resumido (erro elevado)", s["h1"]))
    story.append(
        bullets(
            [
                "Sintoma: login/catálogo com 5xx ou health vermelho",
                "Verificar: painel, health, logs/traces, banco, deploy recente",
                "Mitigar: rollback se pós-deploy; drenar instância má; escalar; DR se região",
                "Escalar pessoas em 15 min sem mitigação; comunicar status",
                "Estabilizar quando erro &lt; 1% e p95 &lt; 400 ms por 15 min; postmortem curto",
            ],
            s["body"],
        )
    )

    story.append(P("9. Riscos principais", s["h1"]))
    story.append(
        bullets(
            [
                "Fadiga de alerta → apenas sintomas com ação",
                "HA com H2 → descartado na proposta-alvo",
                "DR sem teste → RTO irreal; testes no plano",
            ],
            s["body"],
        )
    )

    story.append(P("10. Referências", s["h1"]))
    story.append(
        bullets(
            [
                "Enunciado Aula 12 — UniALFA (observabilidade, HA e DR)",
                "Google SRE — SLIs, SLOs e error budgets",
                "Serviço Biblioteca — base do T6/T7",
            ],
            s["small"],
        )
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title="T7 Observabilidade HA DR — Biblioteca",
        author="Diego Santos; Wallace Gabriel",
    )
    doc.build(story)
    print(f"PDF: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
