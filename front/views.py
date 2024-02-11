from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
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


class HomeView(TemplateView):
    template_name = 'index.html'


class ProfileView(TemplateView):
    template_name = 'profile.html'


class CompareView(TemplateView):
    template_name = 'compare.html'


class OrderDetailView(View):
    template_name = 'order_detail.html'

    def get(self, request, id):
        return render(request, self.template_name, {'id': id})


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
print(ZP_API_VERIFY, ZP_API_STARTPAY, ZP_API_REQUEST)
amount = 1000
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
phone = '09353220545'  # Optional

CallbackURL = 'http://127.0.0.1:8000/verify/'


def send_request(request):
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
        # print('here 1')

        if response.status_code == 200:
            response = response.json()
            # print('here 2')
            print('response: ', response)
            if response['Status'] == 100:
                # print('here 3')
                print({'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                       'authority': response['Authority']})
                verify(request, response['Authority'])
                return HttpResponse('OK')
                # print('here 4')
            else:
                # print('here 5')
                return {'status': False, 'code': str(response['Status'])}
        print(response)
        return HttpResponse('Not OK')

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(request, authority):
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
            print({'status': True, 'RefID': response['RefID']})
            return {'status': True, 'RefID': response['RefID']}
        else:
            print({'status': False, 'code': str(response['Status'])})
            return {'status': False, 'code': str(response['Status'])}
    print(response)
    return response
