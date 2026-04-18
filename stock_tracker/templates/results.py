<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ symbol }} - Results</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            background: #0d1117; color: white;}
            .card { background: #161b22;border: 1px solid #30363d; color: white ;}
            .badge-bull { background: #28a745;}
            .badge-bull { background: #dc3545;}
            h2 { color: #f0b429;}
            .news-card {border-left: 3px solid #f0b429; }
            .ai-box { background: #1c2a1c; border: 1px solid #28a745; border-radius: 10px; padding: 20px;}
            </style>
            </head>
            <body>
                <div class = "container mt-4"
                <a href="/" class="btn btn-outline-warning mb-3"><Back to Search</a>
                    
                    {% if error %}
                    <div class="alert alert-danger">{{ error }}</div>
                    {% else %}

                    <div class="card mb-4">
                        <h2>{{symbol}}</h2>
                        <h4> class = "text-success">${{latest_price}}</h4>
                        <p> class = "text-secondary">As of {{latest_date}}</p>
                    </div>

                    <div class="card mb-4">
                        <h5> class = "text-warning mb-3"> Price Trend (last 10 Days)</h5>
                        <canvas id="priceChart" height="100"></canvas>
                    </div>
                   

                    <div class = "ai-box mb-4">
                        <h5 class = "text-success mb-3">AI Trend Analysis</h5>
                    <p>{{ prediction }} </p>

                    </div>

                    <h5 class = "text-warning mb-3">Latest News</h5>
                    {% for article in news %}
                    <div class="card p-3 mb-2 news-card">
                        <a href="{{ article.url }}" target="_blank" class="text-warning text-decoration-none">
                            <strong>{{ article.title }}</strong>
                        </a>
                        <p class="text-secondary mt-1"> style = "font-size: 0.85rem;">
                            {{ article.source.name }} - {{ article.publishedAt|slice:":10" }}
                        </p>
                    </div>
                    {% endfor %}
                    <p class = "text-secondary mt-1"> No News Found.</p>
                    {% endif %}

                    {% endif %}
                </div>
                <script>
                    const labels = [{% for data, price in prices % }"{{ date }}",{% if not forloop.last %},{% endif %}, {% endfor %}].reverse();
                    const data = [{% for date, price in prices %}{{ price }},{% if not forloop.last %},{% endif %}, {% endfor %}].reverse();

                    new Chart(document.getElementById('priceChart'){
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: '{{ symbol }} Close Price',
                                data: data,
                                borderColor: '#f0b429',
                                backgroundColor: 'rgba(240, 180, 41, 0.2)',
                                tension: 0.4,
                                fill: true,
                                pointBackgroundColor: '#f0b429',

                            }]
                        },
                        options: {
                            plugins: {legend: {labels: {color: 'white'}}},
                            scales: {
                                x: { ticks: { color: '#aaa'}, grid: { color: '#30363d' }},
                                y: { ticks: { color: '#aaa'}, grid: { color: '#30363d' }}
                    }
                        }
                    });
                </script>
            </body>
</html>