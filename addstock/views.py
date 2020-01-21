from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from addstock.models import stockModel, productsModel, sellStockModel, remainingModel
import datetime

# Create your views here.

@login_required
def addstock(request):
    products = productsModel.objects.all()

    if request.method == 'POST':
        stockedby = request.POST['stockedby']
        rice = request.POST['rice']
        amount = request.POST['amount']
        bosta = request.POST['bosta']

        stocks = stockModel(stockedby=stockedby, rice=rice, amount=amount, bosta=bosta, time = datetime.datetime.now())

        if stocks is not None:
            stocks.save()
            return redirect('stocks')


    return render(request, 'addstock.html', {'products' : products})

@login_required
def stocks(request):
    products = productsModel.objects.all()
    
    return render(request, 'stocks.html', {'products' : products})

@login_required
def stockresult(request, sid):
    products = productsModel.objects.get(pk=sid)
    stocks = stockModel.objects.all()
    remaining = remainingModel.objects.get(pk=sid)
    sells = sellStockModel.objects.all()

    totalamount = 0
    totalbosta = 0

    sellamount = 0
    sellbosta = 0
    sold = 0

    remainamount = 0
    remainbosta = 0

    for each in stocks:
        if each.rice == products.product:
            totalamount += each.amount
            totalbosta += each.bosta
            

    for each in sells:
        if each.rice == products.product:
            sellamount  += each.amount
            sellbosta   += each.bosta
            sold        += each.price

    products.productamount  = totalamount
    products.productbosta   = totalbosta

    products.save()

    remainamount    = totalamount - sellamount
    remainbosta     = totalbosta - sellbosta

    remaining.ramount = remainamount
    remaining.rbosta = remainbosta

    remaining.save()

    return render(request, 'stockresult.html', 
        {'products' : products, 'stocks' : stocks, 'remaining' : remaining, 'sells' : sells, 
        'sellamount' : sellamount, 'sellbosta' : sellbosta, 'sold' : sold})


def sellstock(request, sid):
    products = productsModel.objects.get(pk=sid)
    remain  = remainingModel.objects.get(pk=sid)

    if request.method == 'POST':
        name = request.POST['customer']
        amount = request.POST['amount']
        bosta = request.POST['bosta']
        price = request.POST['price']

        sell = sellStockModel(customer = name, rice = products.product, amount = amount, bosta = bosta, time = datetime.datetime.now(), price = price)
        
        if sell is not None:
            sell.save()
            
            products.productamount -= int(amount)
            products.productbosta  -= int(bosta)

            remaining = remainingModel(pk=sid, product = products.product, ramount = products.productamount, rbosta = products.productbosta)

            if remaining is not None:
                remaining.save()
                return redirect('stocks')

    return render(request, 'sellstock.html', {'products' : products, 'remain' : remain})


def sell(request):
    products = productsModel.objects.all()

    if request.method == 'POST':
        searched = request.POST['search']
    else:
        searched = ''

    searchedproducts = productsModel.objects.filter(product__contains = searched)

    return render(request, 'sell.html', {'products' : products, 'searchedproducts' : searchedproducts})


def addproduct(request):
    if request.method == 'POST':
        name = request.POST['product']

        products    = productsModel(product = name)
        products.save()

        remaining   = remainingModel(product = name, ramount = 0, rbosta = 0)
        remaining.save()

        return redirect('stocks')


    return render(request, 'addproduct.html')


# def sellstock(request, sid):
#     products = productsModel.objects.get(pk=sid)
#     remain  = remainingModel.objects.get(pk=sid)

#     if request.method == 'POST':
#         name = request.POST['customer']
#         amount = request.POST['amount']
#         bosta = request.POST['bosta']
#         price = request.POST['price']

#         sell = sellStockModel(customer = name, rice = products.product, amount = amount, bosta = bosta, time = datetime.datetime.now(), price = price)
        
#         if sell is not None:
#             sell.save()
            
#             products.productamount -= int(amount)
#             products.productbosta  -= int(bosta)

#             remaining = remainingModel(pk=sid, product = products.product, ramount = products.productamount, rbosta = products.productbosta)

#             if remaining is not None:
#                 remaining.save()
#                 remaining.refresh_from_db()
#                 return redirect('stocks')

#     return render(request, 'sellstock.html', {'products' : products, 'remain' : remain})