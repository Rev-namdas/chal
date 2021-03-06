from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from addstock.models import stockModel, productsModel, sellStockModel, remainingModel
from datetime import datetime
from datetime import timedelta
import xhtml2pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse


@login_required
def addstock(request):
    products = productsModel.objects.all()

    if request.method == 'POST':
        stockedby = request.POST['stockedby']
        rice = request.POST['rice']
        amount = request.POST['amount']
        bosta = request.POST['bosta']

        stocks = stockModel(stockedby=stockedby, rice=rice, amount=amount, bosta=bosta, time = datetime.now())

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

        sell = sellStockModel(customer = name, rice = products.product, amount = amount, bosta = bosta, time = datetime.now(), price = price)
        
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

    totalamount = 0
    totalbosta  = 0

    if request.method == 'POST':
        fromdate    = request.POST['date1']
        todate      = request.POST['date2']
        if fromdate:
            startingdate    = fromdate
        else:
            startingdate    = "2020-01-01"

        if todate:
            newtodate       = datetime.strptime(todate, '%Y-%m-%d').date()
            finishingdate   = newtodate + timedelta(days=1)
        else:
            finishingdate   = "2050-01-01"
        
        

    sells = sellStockModel.objects.filter(time__range=[startingdate, finishingdate]).order_by('time')

    for each in sells:
        totalamount += each.amount
        totalbosta  += each.bosta

    return render(request, 'report.html', 
        {'sells' : sells, 'totalamount' : totalamount, 'totalbosta' : totalbosta})


def productwisereport(request):
    rtotalamount = 0
    rtotalbosta  = 0
    ctotalamount = 0
    ctotalbosta  = 0

    if request.method == 'POST':
        searched = request.POST['search']
    else:
        searched = ''

    sellsrice       = sellStockModel.objects.filter(rice__contains = searched).order_by('time')
    sellscustomer   = sellStockModel.objects.filter(customer__contains = searched).order_by('time')


    if sellsrice:
        for each in sellsrice:
            rtotalamount += each.amount
            rtotalbosta  += each.bosta
        return render(request, 'productwisereport.html',
            {'sellsrice' : sellsrice, 'rtotalamount' : rtotalamount, 'rtotalbosta' : rtotalbosta})

    if sellscustomer:
        for each in sellscustomer:
            ctotalamount += each.amount
            ctotalbosta  += each.bosta
        return render(request, 'productwisereport.html',
            {'sellscustomer' : sellscustomer, 'ctotalamount' : ctotalamount, 'ctotalbosta' : ctotalbosta})



def customerprofile(request, cid):
    customer = sellStockModel.objects.get(pk=cid)

    sells = sellStockModel.objects.filter(customer__contains = customer.customer).order_by('time')

    startingdate    = "2020-01-01"
    finishingdate   = "2050-01-01"

    totalamount = 0
    totalbosta  = 0

    for each in sells:
        totalamount += each.amount
        totalbosta  += each.bosta

    if request.method == 'POST':
        totalamount = 0
        totalbosta  = 0

        fromdate    = request.POST['date1']
        todate      = request.POST['date2']
        if fromdate:
            startingdate    = fromdate
        else:
            startingdate    = "2020-01-01"

        if todate:
            newtodate       = datetime.strptime(todate, '%Y-%m-%d').date()
            finishingdate   = newtodate + timedelta(days=1)
        else:
            finishingdate   = "2050-01-01"
        
        

        newsells = sells.filter(time__range=[startingdate, finishingdate]).order_by('time')

        for each in newsells:
            totalamount += each.amount
            totalbosta  += each.bosta
            
        return render(request, 'customerprofile.html', 
            {'sells' : newsells, 'totalamount' : totalamount, 'totalbosta' : totalbosta})

    return render(request, 'customerprofile.html',
            {'sells' : sells, 'totalamount' : totalamount, 'totalbosta' : totalbosta})
            

def reportpdf(request):

    totalamount = 0
    totalbosta  = 0

    sells = sellStockModel.objects.all().order_by('time')

    for each in sells:
        totalamount += each.amount
        totalbosta  += each.bosta

    data = {
        'sells' : sells,
        'totalamount' : totalamount,
        'totalbosta' : totalbosta
    }

    template = get_template('reportpdf.html')
    dataa = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(dataa.encode("UTF-8")), response)

    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")


def customerpdf(request, cusid):
    
    customer = sellStockModel.objects.get(pk=cusid)
    sells = sellStockModel.objects.filter(customer__contains = customer.customer).order_by('time')

    totalamount = 0
    totalbosta  = 0

    for each in sells:
        totalamount += each.amount
        totalbosta  += each.bosta

    data = {
        'sells' : sells,
        'totalamount' : totalamount,
        'totalbosta' : totalbosta
    }

    template = get_template('customerprofilepdf.html')
    dataa = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(dataa.encode("UTF-8")), response)

    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")