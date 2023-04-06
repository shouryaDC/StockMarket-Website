from django.shortcuts import render , redirect
from .forms import StockForm
from quotes.models import Stock
from django.contrib import messages

# Create your views here.
#serves as a browser request for home page
def home(request):
    import requests
    import json

    if request.method == 'POST':
       ticker = request.POST['ticker_symbol']
        # pk_129ac10c68464919a6da11b53962d77b
       api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/"+ticker+"?token=pk_129ac10c68464919a6da11b53962d77b")
        
       
       api = json.loads(api_request.content)
       if api == [None]:
           api = "Error"
       return render(request,'home.html', {'api': api})
    else:
        return render(request,'home.html', {'ticker': "Enter a ticker symbol above"})
   
    #pointing to home.html in template directory 
def about(request):
    return render(request, 'about.html',{})

def add_stock(request):
    import requests
    import json
    if request.method == 'POST':
       form = StockForm(request.POST or None)
       if form.is_valid():
           form.save()
           messages.success(request, ("Stock Has Been Added!"))
           return redirect('add_stock')
    else:
       ticker = Stock.objects.all()
       output = []
       for ticker_item in ticker:
           api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/"+str(ticker_item)+"?token=pk_129ac10c68464919a6da11b53962d77b")
           api = json.loads(api_request.content)
           output.append(api)
           if api == [None]:
             api = "Error"
       return render(request, 'add_stock.html', {'ticker': ticker,'output':output })
    
def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been Deleted!"))
    return redirect(delete_stock);

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker':ticker})