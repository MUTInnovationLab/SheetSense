// Example chart data (can be dynamically generated from backend)
var ctx = document.getElementById('reportTrends').getContext('2d');
var reportTrends = new Chart(ctx, {
    type: 'line', // Change to 'bar' for bar chart
    data: {
        labels: ['Jan 1', 'Jan 5', 'Jan 10', 'Jan 12', 'Jan 15'],
        datasets: [{
            label: 'Number of Reports',
            data: [3, 2, 5, 6, 4], // Example data
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.2)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return 'Reports: ' + context.raw;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});