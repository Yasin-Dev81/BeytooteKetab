from config.settings import MERCHANT, ZP_Description, CallbackURL
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse

import datetime
import requests
import json

from .models import PremiumOrder, PremiumPlan

ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"


class ProfileView(LoginRequiredMixin, View):
    template_name = 'order/profile.html'

    def setup(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            orders = PremiumOrder.objects.filter(user=request.user)
            paginator = Paginator(orders, 25)
            page_number = request.GET.get("page")
            self.page_obj = paginator.get_page(page_number)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"orders": self.page_obj})


class PremiumPlansView(LoginRequiredMixin, generic.ListView):
    template_name = 'order/premium_plan_list.html'
    model = PremiumPlan


class OrderCreateView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.plan = get_object_or_404(PremiumPlan, pk=kwargs['plan_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'order/accept_order.html', {'plan': self.plan})

    def post(self, request, *args, **kwargs):
        price = self.plan.price
        order = PremiumOrder.objects.create(
            user=request.user,
            plan=self.plan,
            paid_count=price
        )
        order.save()
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        messages.success(request, 'در حال انتفال به صفحه پرداخت هستید', 'success')
        return redirect(reverse('order:pay_order', args=(order.pk,)))


class ZPOrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(PremiumOrder, pk=order_id)

        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.paid_count,
            "callback_url": CallbackURL,
            "description": ZP_Description,
            "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
        }
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req = requests.post(
            url=ZP_API_REQUEST,
            data=json.dumps(req_data),
            headers=req_header
        )
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=req.json()['data']['authority']))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            messages.error(
                request,
                "مشکلی در انتقال به شبکه پرداخت به وجود آمده است لطفا دقایقی دیگر دوباره امتحان نمایید!",
                "danger"
            )
            order.delete()
            request.session['order_pay'] = {}
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return redirect(reverse("order:premium_plans"))


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = get_object_or_404(PremiumOrder, pk=order_id)
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json", "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.paid_count,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.paid = True
                    order.tracking_code = str(req.json()['data']['ref_id'])
                    order.save()
                    user = request.user
                    user.premium_expire_date = datetime.datetime.now() + order.plan.longtime
                    user.save()
                    # return HttpResponse('Transaction success.\nRefID: ' + str(req.json()['data']['ref_id']))
                    messages.success(request, "پرداخت موفقیت آمیز بود %s" % str(req.json()['data']['ref_id']))
                elif t_status == 101:
                    # return HttpResponse('Transaction submitted : ' + str(req.json()['data']['message']))
                    messages.success(request, "تراکنش ارسال شده %s" % str(req.json()['data']['message']))
                else:
                    # return HttpResponse('Transaction failed.\nStatus: ' + str(req.json()['data']['message']))
                    messages.error(request, "Transaction failed.\nStatus: " + str(req.json()['data']['message']),
                                   "danger")
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                messages.error(request, f"Error code: {e_code}, Error Message: {e_message}", "danger")
                # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            # return HttpResponse('Transaction failed or canceled by user')
            messages.error(request, "Transaction failed or canceled by user", "danger")
        return redirect(reverse('order:user_profile'))
