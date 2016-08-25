from django.shortcuts import render_to_response, render
from models import Publisher, Author, Book
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from forms import ContactForm

# Create your views here.

def book_list(request):
    book_list = Book.objects.all().order_by('-title')
    return render_to_response('booklist.html', {'book_list': book_list})

# def search_form(request):
#     return render_to_response('search_form.html')

def search(request):
    errors = []
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        if len(q)>20:
            errors.append('Please enter at most 20 characters.')
            return render_to_response('search.html', {'errors': errors})
        else:
            book_list = Book.objects.filter(title__icontains=q)
            return render_to_response('booklist.html', {'book_list': book_list, 'query': q})
    elif 'q' in request.GET and not request.GET['q']:
        errors.append('Please enter a search term.')
        return render_to_response('search.html', {'errors': errors})
    else:
        return render_to_response('search.html', {'errors': errors})

# def contact(request):
#     errors = []
#     if request.method == 'POST':
#         pass
#         if not request.POST.get('subject', ''):
#             errors.append('Enter a subject')
#         if not request.POST.get('message', ''):
#             errors.append('Enter a message')
#         if request.POST.get('email') and '@' not in request.POST['email']:
#             errors.append('Enter a valid email address')
#         if not errors:
#             #send email
#             return HttpResponseRedirect('/contact/thanks/')
#     return render(request, 'contact.html', 
#         {'errors': errors, 
#         'subject': request.POST.get('subject', ''),
#         'message': request.POST.get('message', ''),
#         'email':   request.POST.get('email', ''),
#         })

# def contactform(request):
#     return render_to_response('contact_form.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(
                initial = {'subject': 'I love your site!'}
            )
    return render(request, 'contact.html', {'form': form})


def thanks(request):
    return render_to_response('thanks.html')