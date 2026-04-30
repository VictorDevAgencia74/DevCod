class SalesAnalysisService:
    @staticmethod
    def get_sales_analysis():
        months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        revenue = [320, 345, 372, 360, 392, 410, 430, 462, 498, 520, 610, 712]
        orders = [820, 790, 860, 840, 910, 960, 1020, 1060, 1120, 1180, 1390, 1505]
        avg_ticket = [round((r * 1000) / o) for r, o in zip(revenue, orders)]

        channel_table = [
            {"channel": "Orgânico", "revenue": "R$ 1,92M", "orders": 10420, "cac": "R$ 18"},
            {"channel": "Pago", "revenue": "R$ 1,54M", "orders": 6380, "cac": "R$ 39"},
            {"channel": "Parcerias", "revenue": "R$ 0,88M", "orders": 3210, "cac": "R$ 22"},
            {"channel": "Upsell", "revenue": "R$ 0,48M", "orders": 1090, "cac": "R$ 7"}
        ]

        return {
            "summary": {
                "revenue_text": "R$ 4,82M",
                "growth_text": "+18% vs. ano anterior",
                "ticket_text": "R$ 189",
                "conversion_text": "3,7%",
                "seasonality_text": "Q4"
            },
            "insights": [
                "Receita concentrada em Assinaturas e Serviços, com variação mensal previsível.",
                "Ticket médio cresce quando o cliente compra bundles ou planos complementares.",
                "Campanhas pagas têm maior conversão, mas CAC sensível a sazonalidade.",
                "Priorizar retenção e expansão da base ativa para aumentar LTV."
            ],
            "chart": {
                "months": months,
                "revenue": revenue,
                "orders": orders,
                "avg_ticket": avg_ticket,
                "mix_labels": ["Assinaturas", "Serviços", "Licenças"],
                "mix_values": [42, 33, 25]
            },
            "channel_table": channel_table,
            "checks": [
                {"test": "Outliers (IQR)", "objective": "Remover distorções no ticket", "result": "2,1%"},
                {"test": "Correlação", "objective": "Ticket vs. pedidos", "result": "r = -0,34"},
                {"test": "Sazonalidade", "objective": "Tendência e sazonalidade", "result": "Q4"}
            ],
            "recommendations": [
                "Otimizar campanhas pagas por janela (pré-Q4) e reduzir CAC por busca orgânica.",
                "Criar bundles estratégicos para elevar ticket médio sem reduzir conversão.",
                "Implementar alertas automáticos para anomalias de receita e queda de volume." 
            ]
        }
