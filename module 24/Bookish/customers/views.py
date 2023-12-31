from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserSignUpForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import View
from transactions.models import TransactionModel
from transactions.constants import BORROW
from django.contrib.auth.mixins import LoginRequiredMixin


class UserSignUpView(FormView):
    template_name = "customers/signup.html"
    success_url = reverse_lazy("home")
    form_class = UserSignUpForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Signed up successfully")
        return super().form_valid(form)


class UserSignInView(LoginView):
    template_name = "customers/signin.html"

    def get_success_url(self):
        messages.success(self.request, "Signed in successfully")
        return reverse_lazy("home")


# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         messages.success(self.request, "Logged out successfully")
#         return reverse_lazy("home")

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")



class UserProfileView(LoginRequiredMixin, View):
    template_name = "customers/profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        borrows = TransactionModel.objects.filter(
            transaction_type=BORROW, customer=self.request.user.customer)
        return render(request, self.template_name, {"form": form, "borrows": borrows})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Profile updated Successfully")
            return redirect("profile")
        return render(request, self.template_name, {"form": form})
