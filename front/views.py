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


# cached_template_home_view = cache_page(60 * 15)(HomeView.as_view())


class ProfileView(TemplateView):
    template_name = 'profile.html'

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CompareView(TemplateView):
    template_name = 'compare.html'


class ChatView(TemplateView):
    template_name = 'chat.html'


class ChatAdminView(TemplateView):
    template_name = 'chatadmin.html'


class OrderDetailView(View):
    template_name = 'order_detail.html'

    def get(self, request, id):
        return render(request, self.template_name, {'id': id})


def set_language(request):
    if request.method == 'POST':
        language_code = request.POST.get('language_code')
        request.session['language_code'] = language_code
        settings.LANGUAGE_CODE = language_code
        activate(language_code)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
