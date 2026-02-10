document.addEventListener('DOMContentLoaded', function() {
    // A URL deve ser definida globalmente ou passada de alguma forma, 
    // mas para manter limpo, vamos assumir que o script é carregado depois que a variável é definida
    // ou usar um atributo data no elemento do gráfico.
    
    const canvas = document.getElementById('vendasChart');
    if (!canvas) return;

    const url = canvas.dataset.url;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Vendas Mensais (R$)',
                        data: data.data,
                        borderColor: '#00d2ff',
                        backgroundColor: 'rgba(0, 210, 255, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: '#e2e8f0' }
                        }
                    },
                    scales: {
                        y: {
                            grid: { color: 'rgba(255, 255, 255, 0.05)' },
                            ticks: { color: '#94a3b8' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: '#94a3b8' }
                        }
                    }
                }
            });
        });
});
