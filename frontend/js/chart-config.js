// Глобальная настройка Chart.js
Chart.defaults.color = '#94a3b8'; // Цвет текста
Chart.defaults.borderColor = '#334155'; // Цвет сеток
Chart.defaults.font.family = 'Inter, sans-serif';

// Конфигурация графика временного ряда
const chartConfig = {
    type: 'line',
    data: {
        labels: [], // Временные метки (будут заполнены динамически)
        datasets: [{
            label: 'Температура (°C)',
            data: [], // Значения (будут заполнены динамически)
            borderColor: '#6366f1',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4, // Сглаживание линии
            pointRadius: 3,
            pointHoverRadius: 6,
            pointBackgroundColor: '#6366f1',
            pointBorderColor: '#fff',
            pointBorderWidth: 2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    padding: 15,
                    usePointStyle: true
                }
            },
            tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                titleColor: '#f1f5f9',
                bodyColor: '#94a3b8',
                borderColor: '#334155',
                borderWidth: 1,
                padding: 12,
                displayColors: true,
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + ' °C';
                    }
                }
            }
        },
        scales: {
            x: {
                grid: {
                    display: true,
                    color: '#1e293b'
                },
                ticks: {
                    maxRotation: 45,
                    minRotation: 0
                }
            },
            y: {
                beginAtZero: false,
                grid: {
                    display: true,
                    color: '#1e293b'
                },
                ticks: {
                    callback: function(value) {
                        return value.toFixed(1) + '°C';
                    }
                }
            }
        },
        animation: {
            duration: 750,
            easing: 'easeInOutQuart'
        }
    }
};

// Функция обновления графика
function updateChart(chart, newLabels, newData) {
    chart.data.labels = newLabels;
    chart.data.datasets[0].data = newData;
    chart.update('none'); // 'none' отключает анимацию при обновлении
}

// Функция очистки графика
function clearChart(chart) {
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update();
}
