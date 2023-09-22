from django.shortcuts import render, redirect
from django.views import View
# from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, UserPasswordResetForm
from . import forms
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(View):
    form_class = forms.UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            print('valid')
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                # 'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password1'],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = forms.VerifyCodeForm
    template_name = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(
                    user_session['phone_number'],
                    None,
                    # user_session['email'],
                    user_session['full_name'],
                    user_session['password']
                )

                code_instance.delete()
                messages.success(request, 'you registered.', 'success')
                return redirect('book:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'با موفقیت خارج شدید', 'success')
        return redirect('book:home')


class UserLoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید', 'info')
                return redirect('book:home')
            messages.error(request, 'شماره تلفن یا پسورد اشتباه است!', 'warning')
        return render(request, self.template_name, {'form': form})


class UserPasswordResetView(View):
    form_class = forms.UserPasswordResetForm
    template_name = 'accounts/password_reset_phone.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_password_reset_info'] = {
                'phone_number': form.cleaned_data['phone']
            }
            messages.success(request, 'کد برای شما ارسال شد', 'success')
            return redirect('accounts:forgot_password_verify')
        return render(request, self.template_name, {'form': form})


class UserPasswordResetVerifyCodeView(View):
    form_class = forms.UserPasswordResetVerifyCodeForm
    template_name = 'accounts/password_reset_verify_code.html'

    def get(self, request):
        form = self.form_class
        user_session = request.session['user_password_reset_info']
        return render(request, self.template_name, {'form': form, 'phone_number':user_session['phone_number']})

    def post(self, request):
        user_session = request.session['user_password_reset_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                user = User.objects.get(phone_number=user_session['phone_number'])
                user.set_password(cd['password2'])
                user.save()

                code_instance.delete()
                messages.success(request, 'پسورد شما با موفقیت تغییر کرد', 'success')
                return redirect('accounts:user_login')
            else:
                messages.error(request, 'کد وارد شده صحیح نمی‌باشد', 'danger')
                return redirect('accounts:forgot_password')
        return render(request, self.template_name, {'form': form})
