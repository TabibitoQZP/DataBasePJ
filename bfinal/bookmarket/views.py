from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages # to output change message

from .models import Profile, Book, Import, Bill

# Create your views here.

@login_required
def home(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        ifchange = False
        # print(request.POST)
        # change submit is valid
        if request.POST['submit'] == 'change':
            # change real name
            if request.POST['realname'] != '' and user_profile.realname != request.POST['realname']:
                ifchange = True
                user_profile.realname = request.POST['realname']
            # change gender
            if request.POST['man'] != 'null':
                if request.POST['man'] == '1' and user_profile.man != True:
                    ifchange = True
                    user_profile.man = True
                if request.POST['man'] == '0' and user_profile.man != False:
                    ifchange = True
                    user_profile.man = False
            # change birth
            if request.POST['birth'] != '' and user_profile.birth != request.POST['birth']:
                ifchange = True
                user_profile.birth = request.POST['birth']
            if ifchange:
                user_profile.save()
                messages.success(request, 'Changes applied successfully!')
            else:
                messages.info(request, 'Changes applied failed!')
            # access database again to keep the change enabled!
            user_profile = Profile.objects.get(user=request.user)
            return redirect('home')
    return render(request, 'bookmarket/home.html', {'profile': user_profile})

@login_required
def book(request):
    books = Book.objects.all()
    if request.method == 'POST':
        print(request.POST)
        # search engine.
        if request.POST['submit'] == 'search':
            # if search is null, then return all books.
            if request.POST['search'] == '':
                return render(request, 'bookmarket/book.html', {'books': books})
            # render the searched books, only match name and public
            book_isbn = books.filter(ISBN__contains=request.POST['search'])
            book_name = books.filter(name__contains=request.POST['search'])
            sum = book_isbn | book_name
            return render(request, 'bookmarket/book.html', {'books': sum})
        # change book info.
        elif request.POST['submit'] == 'bookchange':
            ifchange = False
            book_need_change = books.get(ISBN=request.POST['isbn'])
            if request.POST['name'] != '':
                ifchange = True
                book_need_change.name = request.POST['name']
            if request.POST['public'] != '':
                ifchange = True
                book_need_change.public = request.POST['public']
            if request.POST['author'] != '':
                ifchange = True
                book_need_change.author = request.POST['author']
            if request.POST['price'] != '':
                ifchange = True
                book_need_change.price = request.POST['price']
            if request.POST['amount'] != '':
                ifchange = True
                book_need_change.amount = request.POST['amount']
            if ifchange:
                book_need_change.save()
                messages.success(request, 'Changes applied successfully!')
            else:
                messages.info(request, 'Changes applied failed!')
            return redirect('book')
        # add new book.
        elif request.POST['submit'] == 'bookadd':
            ifadd = True
            for i in request.POST['isbn']:
                if i <= '0' or i >= '9':
                    ifadd = False
                    break
            if Book.objects.filter(ISBN=request.POST['isbn']).count() != 0:
                ifadd = False
            if ifadd:
                new_book = Book(request.POST['isbn'], request.POST['name'], request.POST['public'],
                request.POST['author'], request.POST['price'], request.POST['amount'])
                new_book.save()
                messages.success(request, 'Add new book successfully!')
            else:
                messages.info(request, 'Add new book failed!')
            return redirect('book')
        # add new import
        elif request.POST['submit'] == 'bookimport':
            new_import = Import()
            new_import.price = request.POST['price']
            new_import.amount = request.POST['amount']
            new_import.book = Book.objects.get(ISBN=request.POST['isbn'])
            new_import.save()
            messages.success(request, 'Add new import successfully. Please check and pay the bill in the "Import" page.')
        # sale books
        elif request.POST['submit'] == 'booksale':
            tmpbook = Book.objects.get(ISBN=request.POST['isbn'])
            if tmpbook.amount < int(request.POST['amount']):
                messages.info(request, 'Not enough books')
            else:
                tmpbook.amount = tmpbook.amount - int(request.POST['amount'])
                tmpbook.save()
                tmpbill = Bill()
                tmpbill.operator = Profile.objects.get(user = request.user)
                tmpbill.earn_cost = int(request.POST['amount']) * tmpbook.price
                tmpbill.save()
        else:
            return render(request, 'bookmarket/book.html', {'books': books})
    return render(request, 'bookmarket/book.html', {'books': books})

def imports(request):
    book_import = Import.objects.all().order_by('-date')
    if request.method == 'POST':
        print(request.POST)
        tmp_import = Import.objects.get(iid=int(request.POST['iid']))
        if request.POST['status'] == '1':
            print('bill decrease')
        elif request.POST['status'] == '2':
            print('book amount add')
        elif request.POST['status'] == '3':
            print('nothing happen')
        else:
            print('error code')
        tmp_import.status = int(request.POST['status'])
        tmp_import.save()
        return redirect('import')
    return render(request, 'bookmarket/import.html', {'imports': book_import})

def bill(request):
    bills = Bill.objects.all().order_by('-date')
    return render(request, 'bookmarket/bill.html', {'bills': bills})