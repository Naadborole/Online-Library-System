from django.shortcuts import render
from django.views.generic import View
from .forms import loginForm
from django.shortcuts import HttpResponse, redirect
from django.http import JsonResponse
from .forms import *
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

loggedIn = False
client = MongoClient(
    "mongodb+srv://Application:application1234@onlib.i34wm.mongodb.net/data?retryWrites=true&w=majority")
db = client.data


# Create your views here.
class mainPage(View):
    def get(self, request, email):
        return render(request, 'main.html', {'id': email})


class IndexView(View):
    def get(self, request):
        return render(request, 'midecontent.html')


class LoginForm(View):
    form_class = loginForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        users = db['Users']
        email = request.POST.get('email')
        password = request.POST.get('password')
        if self.authenticate(db, email, password):
            userdict = users.find_one({"email": email})
            return redirect('main/' + str(userdict['_id']) + "/")
        return HttpResponse('Failed')

    def authenticate(self, db, email, passwd):
        users = db['Users']
        userdict = users.find_one({"email": email})
        if userdict is None:
            return False
        if userdict['password'] == passwd:
            loggedIn = True
            return True
        return False


class SignUp(View):
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'SignUp.html', {'popup': False, 'form': form})

    def post(self, request):
        users = db['Users']
        message = ''
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        userdata = {'fname': fname, 'lname': lname, 'email': email, 'password': password,
                    'address': address}
        user = users.find_one({'email': email})
        if user is None:
            users.insert_one(userdata)
            message = "Successfully registered"
        else:
            message = "User already exists"

        return render(request, 'SignUp.html', {'popup': True, 'message': message})


class getList(View):
    def get(self, request, objid):
        lists = db['lists']
        users = db['Users']
        bookdb = db['books']
        email = users.find_one({"_id": ObjectId(objid)})
        email = email['email']
        listobj = lists.find_one({'email': email})
        books = listobj['books']
        templist = list()
        for i in books:
            templist.append(bookdb.find_one({"_id": i}))
        if listobj is None:
            return JsonResponse({"error": "Not found"})
        return JsonResponse(templist, safe=False)


class getuser(View):
    def get(self, request, id):
        users = db["Users"]
        userdata = users.find_one({"_id": ObjectId(id)})
        temp = dict()
        for i in userdata.keys():
            if i != "_id":
                temp[i] = userdata[i]
        return JsonResponse(temp)


class getCatalogue(View):
    def get(self, request):
        books = db['books']
        userdata = books.find({})
        userdata = list(userdata)
        return JsonResponse(userdata, safe=False)


class searchTitle(View):
    def get(self, request, title):
        books = db['books']
        userdata = books.find({"title": {"$regex": title, "$options": 'i'}})
        userdata = list(userdata)
        return JsonResponse(userdata, safe=False)


class getBook(View):
    def get(self, request, id, email):
        books = db['books']
        bookdata = books.find_one({"_id": id})
        if bookdata is None:
            return HttpResponse("404 Page not found")
        datapass = dict()
        datapass['bookid'] = id
        datapass['imglink'] = bookdata['cover']['medium']
        datapass['title'] = bookdata['title']
        datapass['description'] = bookdata['description']
        datapass['email'] = email
        lists = db['lists']
        listobj = lists.find_one({"email": email})
        arr = listobj['books']
        if id in arr:
            datapass['dis'] = "true"
        else:
            datapass['dis'] = "false"
        return render(request, 'bookview.html', datapass)


class addTolist(View):
    def get(self, request, email, id):
        books = db['books']
        lists = db['lists']
        bookdata = books.find_one({"_id": id})
        listdata = lists.find_one({"email": email})
        if bookdata is None or listdata is None:
            return JsonResponse({"Status": "Book was not added"})
        else:
            if id not in listdata['books']:
                templist = listdata['books']
                templist.append(id)
                lists.update_one({"email": email}, {"$set": {"books": templist}})
                return JsonResponse({"status": "Book was added"})
        return JsonResponse({"status": "Book already present"})
