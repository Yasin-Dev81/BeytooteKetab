from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.core.paginator import Paginator

from .models import PremiumOrder, PremiumPlan


class ProfileView(LoginRequiredMixin, View):
    template_name = 'order/profile.html'

    def setup(self, request, *args, **kwargs):
        self.orders = PremiumOrder.objects.filter(user=request.user)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        paginator = Paginator(self.orders, 25)
        page_number = request.GET.get("page")
        self.page_obj = paginator.get_page(page_number)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"orders": self.page_obj})


class PremiumPlansView(LoginRequiredMixin, generic.ListView):
    template_name = 'order/checkout.html'
    model = PremiumPlan
