"""mainsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from addstock import views as addstocks
from login import views as logins

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', logins.pagelock),
    path('', logins.login, name="login"),
    path('signup/', logins.signup, name="signup"),
    path('signin/', logins.signin, name="signin"),
    path('addstock/', addstocks.addstock, name="addstock"),
    path('logout/', logins.logout, name="logout"),
    path('stocks/', addstocks.stocks, name="stocks"),
    path('stockresult/<sid>', addstocks.stockresult, name="stockresult"),
    path('sellstock/<sid>', addstocks.sellstock, name="sellstock"),
    path('sell/', addstocks.sell, name="sell"),
    path('addproduct/', addstocks.addproduct, name="addproduct"),
    path('report/', addstocks.report, name="report")
]
