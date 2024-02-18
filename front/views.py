from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.utils.translation import activate
from django.views import View
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from django.conf import settings
import requests
import json


# Create your views here.
class LoginView(TemplateView):
    template_name = 'login.html'


class VerifyOtpView(TemplateView):
    template_name = 'verify_otp.html'


class SetPasswordView(TemplateView):
    template_name = 'set_password.html'


class RegisterView(TemplateView):
    template_name = 'register.html'


class ProductListView(TemplateView):
    template_name = 'products_list.html'


class ProductDetailView(View):
    template_name = 'products_detail.html'

    def get(self, request, id):
        return render(request, self.template_name, {'id': id})


class CartView(TemplateView):
    template_name = 'cart.html'


class BlogListView(TemplateView):
    template_name = 'blogs.html'


cached_template_blog_list_view = cache_page(60 * 60 * 10)(BlogListView.as_view())


class BlogDetailView(View):
    template_name = 'blog_detail.html'

    def get(self, request, id):
        return render(request, self.template_name, {'id': id})


cached_template_blog_detail_view = cache_page(60 * 60 * 10)(BlogDetailView.as_view())


class HomeView(TemplateView):
    template_name = 'index.html'


cached_template_home_view = cache_page(60 * 60 * 5)(HomeView.as_view())


class ProfileView(TemplateView):
    template_name = 'profile.html'

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CompareView(TemplateView):
    template_name = 'compare.html'


class OrderDetailView(View):
    template_name = 'order_detail.html'

    def get(self, request, id):
        return render(request, self.template_name, {'id': id})


def send_request(request, amount):

    description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
    CallbackURL = 'http://127.0.0.1:8000/verify/'

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    print(data)
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            print('response: ', response)
            if response['Status'] == 100:
                return HttpResponse('OK')
            else:
                return {'status': False, 'code': str(response['Status'])}
        return HttpResponse('Not OK')

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(request, amount, authority):

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response


def set_language(request):
    if request.method == 'POST':
        language_code = request.POST.get('language_code')
        request.session['language_code'] = language_code
        settings.LANGUAGE_CODE = language_code
        activate(language_code)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
