from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


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
