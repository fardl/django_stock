#Copyright (c) 2024 Francisco Ramirez.

from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
	import requests
	import json

	#cr91ji9r01qmiu0b3vlgcr91ji9r01qmiu0b3vm0

	if request.method == 'POST':
		ticker = request.POST['ticker']
		url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/quotes"
		querystring = {"ticker":ticker}
		headers = {
			"x-rapidapi-key": "d35d11fbe1msh6e7a070c1d324cep1c2207jsn2a36c7654fcd",
			"x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
			}
		api_request = requests.get(url,headers=headers, params=querystring)
		try:
			#api = json.loads(api_request.content)
			api = api_request.json()
		except Exception as e:
		    api = "Error..."
		return render(request,'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker':'Enter a ticker symbol above..'})



def about(request):
	return render(request, 'about.html',{})  #Conecta y muestra la pagina.



def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ('Stock has been added'))
			return redirect('add_stock')

	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/quotes"
			querystring = {"ticker":ticker_item}
			headers = {
				"x-rapidapi-key": "d35d11fbe1msh6e7a070c1d324cep1c2207jsn2a36c7654fcd",
				"x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
				}
			api_request = requests.get(url,headers=headers, params=querystring)

			try:
				api = api_request.json()
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker':ticker, 'output':output, 'ticker':ticker, 'ticker_item':ticker_item})




def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted"))
	return redirect('add_stock')


#def delete_stock(request):
	