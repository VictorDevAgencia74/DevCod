class ChurnAnalysisService:
    @staticmethod
    def get_churn_analysis():
        cohort_labels = ["M0", "M1", "M2", "M3", "M4", "M5"]
        cohort_jan = [0, 5.5, 6.8, 7.4, 7.9, 8.2]
        cohort_fev = [0, 4.8, 5.9, 6.6, 7.0, 7.3]

        return {
            "summary": {
                "churn_rate": "6,2%",
                "target_rate": "4,7%",
                "activation": "58%",
                "nps": "41"
            },
            "hypotheses": [
                "Baixo uso nas primeiras 2 semanas aumenta risco de churn.",
                "Planos mensais cancelam mais; foco em incentivo anual.",
                "Onboarding incompleto correlaciona com abandono precoce.",
                "Suporte reativo e falta de alertas aumentam o churn." 
            ],
            "chart": {
                "cohort_labels": cohort_labels,
                "cohorts": [
                    {"label": "Coorte Jan", "data": cohort_jan},
                    {"label": "Coorte Fev", "data": cohort_fev}
                ],
                "segment_labels": ["Baixo uso 30d", "Plano mensal", "Onboarding incompleto", "Suporte alto"],
                "segment_risk": [2.6, 1.8, 2.2, 1.4],
                "feature_labels": ["Inactive 30d", "Onboarding", "Plano mensal", "Tenure"],
                "feature_importance": [0.42, 0.28, 0.20, 0.10]
            },
            "model_metrics": [
                {"label": "AUC (ROC)", "value": "0,84"},
                {"label": "Precision (Top 20%)", "value": "0,62"},
                {"label": "Recall (Top 20%)", "value": "0,55"},
                {"label": "Lift (Top 20%)", "value": "2,3x"}
            ],
            "recommendations": [
                "Segmentar clientes de alto risco com campanhas específicas de ativação.",
                "Incentivar migração anual para reduzir churn em planos mensais.",
                "Implementar dashboard de alertas para inatividade e onboarding falho." 
            ]
        }
