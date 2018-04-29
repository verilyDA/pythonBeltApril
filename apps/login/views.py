from django.shortcuts import render, redirect, HttpResponse
from .models import USER, QUOTES
import bcrypt
from django.contrib import messages

# Create your views here.
def index(req):
    data = USER.objects.all()
    context = {
        'data' : data
    }
    if 'id' in req.session:
        req.session.clear()
    else:
        req.session['id'] = ''
    return render(req, 'login/index.html', context)

def logout(req):
    req.session.clear()
    return redirect('/')

def login(req):
    errors = USER.objects.log_valid(req.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(req, error, extra_tags = tag)
        return redirect('/')
    req.session['id'] = USER.objects.get(email = req.POST['emailLog']).id
    return redirect('/main')


def main(req):
    if req.session['id'] == '':
        context = {
        'data': {'name': 'LIAR', 'id':"You broke in didn't you"}
        }
    else:
        context = {
            'data':USER.objects.get(id=req.session['id']),
            'allQuotes': QUOTES.objects.exclude(fave_by = USER.objects.get(id = req.session['id'])),
            'myQuotes': QUOTES.objects.filter(posted_by = USER.objects.get(id = req.session['id'])).filter(fave_by = USER.objects.get(id = req.session['id']))
        }
    return render(req, 'login/main.html', context)

def register(req):
    errors = USER.objects.registration_valid(req.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(req, error, extra_tags = tag)
        return redirect('/')
    else:
        USER.objects.create(password = req.POST['password'], name = req.POST['name'], alias = req.POST['alias'], email = req.POST['email'], DOB = req.POST['DOB'])
        req.session['id'] = USER.objects.get(email = req.POST['email']).id
        return redirect('/main')

def quote(req):
    errors = QUOTES.objects.quote_valid(req.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(req, error, extra_tags = tag)
    else:
        QUOTES.objects.create(author = req.POST['author'], desc = req.POST['desc'], posted_by = USER.objects.get(id= req.session['id']))
    return redirect('/main')

def fave(req, qid):
    QUOTES.objects.get(id = qid).fave_by.add(USER.objects.get(id = req.session['id']))
    return redirect('/main')

def unfave(req, qid):
    QUOTES.objects.get(id = qid).fave_by.remove(USER.objects.get(id = req.session['id']))
    return redirect('/main')

def userQuotes(req, uid):
    context = {
        'data':USER.objects.get(id = uid),
        'allQuotes': QUOTES.objects.filter(posted_by = USER.objects.get(id = uid)),
        'count': QUOTES.objects.filter(posted_by = USER.objects.get(id = uid)).count()
        }
    return render(req, 'login/userquotes.html', context)
