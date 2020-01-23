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
    date = None

    totalamount = 0
    totalbosta = 0

    sellamount = 0
    sellbosta = 0
    sold = 0

    remainamount = 0
    remainbosta = 0
    
    if request.method == 'POST':
        date = request.POST.get('date')
        print(date[3:5])

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
        'sellamount' : sellamount, 'sellbosta' : sellbosta, 'sold' : sold, 'date' : date})


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


def report(request):
    startingdate    = "2020-01-01"
    finishingdate   = "2050-01-01"

    if request.method == 'POST':
        fromdate    = request.POST['fromdate']
        frommonth   = request.POST['frommonth']
        fromyear    = request.POST['fromyear']

        todate      = request.POST['todate']
        tomonth     = request.POST['tomonth']
        toyear      = request.POST['toyear']

        nfmonth = ''

        if frommonth == 'January':
            nfmonth = '01'
        elif frommonth == 'February':
            nfmonth = '02'
        elif frommonth == 'March':
            nfmonth = '03'
        elif frommonth == 'April':
            nfmonth = '04'
        elif frommonth == 'May':
            nfmonth = '05'
        elif frommonth == 'June':
            nfmonth = '06'
        elif frommonth == 'July':
            nfmonth = '07'
        elif frommonth == 'August':
            nfmonth = '08'
        elif frommonth == 'September':
            nfmonth = '09'
        elif frommonth == 'October':
            nfmonth = '10'
        elif frommonth == 'November':
            nfmonth = '11'
        elif frommonth == 'December':
            nfmonth = '12'


        ntmonth = ''

        if tomonth == 'January':
            ntmonth = '01'
        elif tomonth == 'February':
            ntmonth = '02'
        elif tomonth == 'March':
            ntmonth = '03'
        elif tomonth == 'April':
            ntmonth = '04'
        elif tomonth == 'May':
            ntmonth = '05'
        elif tomonth == 'June':
            ntmonth = '06'
        elif tomonth == 'July':
            ntmonth = '07'
        elif tomonth == 'August':
            ntmonth = '08'
        elif tomonth == 'September':
            ntmonth = '09'
        elif tomonth == 'October':
            ntmonth = '10'
        elif tomonth == 'November':
            ntmonth = '11'
        elif tomonth == 'December':
            ntmonth = '12'

        if fromyear and frommonth and fromdate:
            startingdate    = fromyear + "-" + nfmonth + "-" + fromdate
        else:
            startingdate    = "2020-01-01"

        if toyear and tomonth and todate:
            finishingdate   = toyear + "-" + ntmonth + "-" + str(int(todate) + 1)
        else:
            finishingdate   = "2050-01-01"
        
        

    sells = sellStockModel.objects.filter(time__range=[startingdate, finishingdate]).order_by('time')

    return render(request, 'report.html', {'sells' : sells})