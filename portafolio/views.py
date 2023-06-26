from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DeleteView
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import SignUpForm, LoginForm, UserForm, ProfileForm, PasswordChangingForm
from .models import Profile, Skill
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.mail import send_mail
from django.conf import settings


class HomeView(ListView):
    template_name = 'home/home.html'
    model = Skill
    context_object_name = 'skills'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        #Cuerpo del correo
        body = f'Nombre: {name}\nEmail: {email}\nMensaje: {message}'
        #Envio del correo
        send_mail(
            'Nuevo mensaje de contacto',
            body,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False
        )
        return redirect('thanks')


class ThanksView(TemplateView):
    template_name = 'home/thanks.html'

class ProjectsDetailView(TemplateView):
    template_name = 'home/projects_detail.html'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'login/register.html'

    def form_valid(self, form):
        #Si es válido, guardar
        form.save()

        #Obtener username y password
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )

        #Solicitud de inicio de sesión
        login(self.request, user)
        return redirect('home')
    

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'login/login.html'

class UserUpdateView(LoginRequiredMixin, TemplateView):
    #Retornar al login si no esta autenticado
    login_url = 'login'
    #Formularios
    user_form = UserForm
    profile_form = ProfileForm

    def post(self, request):
        #Verificar si se añadió un archivo o se realizó una solicitud post
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            #Aplicar cambios
            user_form.save()
            profile_form.save()

            return redirect('home')

        #Enviar los formularios como contexto
        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )
        return render(request, 'profile/edit_profile.html', context)

    #Crear perfil si no lo tiene
    def get(self, request, *args, **kwargs):
        if Profile.objects.filter(user=request.user).exists() == False:
            Profile.objects.create(user=request.user)
        return self.post(request, *args, **kwargs)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'profile/delete_user.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)

class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    login_url = 'login'
    template_name = 'password/change_password.html'
    form_class = PasswordChangingForm
    success_url = reverse_lazy('home')
