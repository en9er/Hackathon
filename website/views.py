from django.shortcuts import render, redirect
from django.http import HttpResponse
from client.models import Client
from cheque.models import ReceiptCategory
from cheque.models import Receipt
from django.contrib.auth import authenticate, logout
from Hackathon.settings import BASE_DIR
from .forms import SendReq
from django.core.files.storage import FileSystemStorage
#from website import GoogleAPI
import os


def index(request):
    if request.user.id:
        if request.user.is_superuser:
            return redirect('requests')
        else:
            user = Client.objects.get(username=request.user.username)
            if request.method == 'POST':
                form = SendReq(request.POST, request.FILES)
                print(form)
                if form.is_valid():
                    file = request.FILES['file']
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
                    file.close()
                    uploaded_file_url = fs.url(filename)
                    cheque = form.save(commit=False)
                    cheque.owner = user
                    cheque.sum = request.POST['amount']
                    cheque.photo = uploaded_file_url
                    cheque.save()
                    return redirect('index')
                else:
                    return HttpResponse("invalid_form")
            else:
                context = {}
                if request.user.id:
                    user = Client.objects.get(username=request.user.username)
                    email = user.email
                    fullname = ""
                    if user.name:
                        fullname += user.name
                    if user.first_name:
                        fullname += user.first_name
                    categories = ReceiptCategory.objects.all()
                    context = {'fullname':fullname, 'categories':categories, 'email':email}
                return render(request, '../templates/website/index.html', context)
    else:
        return redirect('login')


def requests(request):
    context = {}
    req = Receipt.objects.all()
    count = req.count()
    if count != 0:
        context = {'request': req[0], 'count': count}
    else:
        context = {'count':count}
    return render(request, '../templates/website/request.html', context)


def reject(request):
    req = Receipt.objects.all()
    os.remove(req[0].photo[1:])
    GoogleAPI.SendGmail(req[0].owner.email, "Compensation Request", "Your compensation request has been rejected")
    req[0].delete()
    return redirect('requests')


def accept(request):
    req = Receipt.objects.all()
    list = []
    file = open(req[0].photo[1:], "r")
    list.append(file)
    fullname = ""
    if req[0].owner.name:
        fullname += req[0].owner.name
    if req[0].owner.first_name:
        fullname += req[0].owner.first_name
    amount = req[0].sum
    date = req[0].date.__str__()
    GoogleAPI.AddReceipt(mail=req[0].owner.email, name=fullname, date=date, amount=amount, files=list)
    file.close()
    os.remove(req[0].photo[1:])
    GoogleAPI.SendGmail(req[0].owner.email, "Compensation request", "Your compensation request has been accepted")
    req[0].delete()
    return redirect('requests')


def login(request):
        context = {'user':request.user}
        return render(request, '../templates/website/login.html', context)


def logout_view(request):
    user = request.user
    print(user)
    if user:
        logout(request)
    return redirect('index')


def RequestDetailView(request, slug):
    user = request.user
    needRequest = 0
    needSlug = request.path
    needSlug = needSlug.replace("/tasks/", '')
    needSlug = needSlug.replace('/', '')
    reqs = Receipt.objects.all()
    for req in reqs:
        if req.slug == needSlug:
            needRequest = req
            break
    return render(request, 'website/request.html', {'request': needRequest, 'user': user})
