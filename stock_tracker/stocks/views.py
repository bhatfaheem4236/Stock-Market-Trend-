from django.shortcuts import render
import requests
from django.conf import settings


def get_stock_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY ,
        "outputsize": "compact"
    }
    r = requests.get(url, params=params)
    return r.json()


def get_news(symbol):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,
        "apiKey": settings.NEWS_API_KEY,
        "pageSize": 5,
        "language": "en",
        "sortBy" : "publishedAt"
    }
    r = requests.get(url, params=params)
    return r.json().get("articles", [])

def get_ai_prediction(symbol, prices):
    price_text = ", ".join([f"{d}: {p}" for d, p in prices])
    headers = {
        "Authorization": "Bearer " + settings.GROQ_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": "compound-beta",
        "messages": [{
            "role": "user",
            "content": "Analyze" + symbol + "stock. Recent prices: "+ price_text +"Give trend, key observation, short-term outlook. Max 150 words."
        }]
    }
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )
    result = r.json()
    if 'choices' in result:
        return result['choices'][0]['message']['content']
    else:
        return "AI analysis unavailable .Error: " + str(result.get('error',{}).get('message', 'Unknown'))

def home(request):
    return render(request, 'home.html')

def search_stocks(request):
    symbol = request.GET.get('symbol', '').upper()
    context = {'symbol': symbol}

    if not symbol:
        return render(request, 'result.html', context)
    
    stock_data = get_stock_data(symbol)
    time_series = stock_data.get("Time Series (Daily)" )

    if not time_series:
        context['error'] = "No data found for this symbol."
        return render(request, 'result.html', context)
    
    dates = sorted(time_series.keys(), reverse=True)[:5]
    prices = [(d, float(time_series[d]["4. close"])) for d in dates]

    news = get_news(symbol)

    prediction = get_ai_prediction(symbol, prices)

    context.update({
        'prices': prices,
        'news': news,
        'prediction': prediction,
        'latest_price': prices[0][1],
        'latest_date': prices[0][0],
    })
    return render(request, 'result.html', context)