from django.contrib import messages
from django.shortcuts import render, redirect
from product.form import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully! Login to Continue")
            return redirect('/login')
    context = {'form': form}
    return render(request, "pages/register.html", context)

def loginPage(request):
    redirect_to = request.GET.get('next', '/')
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("/")
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect(redirect_to)
            else:
                messages.error(request, "Email or Password is invalid")
                return redirect('/login')
    return render(request, 'pages/login.html')

def logoutPage(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('user_location')
    return response