from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from users.forms import LoginForm, RegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.db.models import Count
from stock.models import Category, Stock
from cart.models import Orders


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('stock_list')
        else:
            messages.error(request, 'Ошибка регистрации, проверьте правильность введенных вами данных')
            return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Привет {user.username}, авторизация прошла успешно')
            return redirect('stock_list')
        else:
            messages.error(request, 'Ошибка авторизации, введите правильные имя пользователя и пароль')
            return redirect('stock_list')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('stock_list')


def user_profile(request):
    context = {
        'title': 'Профиль пользователя',
        'categories': Category.objects.annotate(cnt=Count('stock')).filter(cnt__gt=0),
# start app cart #######################################################################################################
        'cart_count': Stock.objects.filter(availability=True),
        'order': Orders.objects.all().filter(user=request.user.id)
# end app cart #########################################################################################################
    }
    return render(request, 'users/user_profile.html', context)


def user_profile_edit(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен')
            return redirect('user_profile')
        else:
            messages.error(request, 'Ошибка обновления номера телефона, введите в формате: 0xxxxxxxxx')
            return redirect('user_profile_edit')
    else:
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    context = {
        'p_form': p_form,
        'title': 'Редактирование профиля',
        'categories': Category.objects.annotate(cnt=Count('stock')).filter(cnt__gt=0),
# start app cart #######################################################################################################
        'cart_count': Stock.objects.filter(availability=True)
# end app cart #########################################################################################################
    }
    return render(request, 'users/user_profile_edit.html', context)
