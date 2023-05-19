from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decouple import config
from django.core.mail import send_mail
#from cloudinary.models import CloudinaryField
#Para validar que el usuario no ponga una fecha posterior a la creacion del usuario
from django.core.validators import MaxValueValidator
from datetime import date

# Create your models here.

class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True,
        validators=[MaxValueValidator(date.today())]
        )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='users/images/', blank=True, null=True)
    #photo = CloudinaryField('image')

    def __str__(self):
        return self.user.username

#Señal a la base dde dats cuando se crea un nuevo usuario, envia un correo de bienvenida al usuario registrado#
#@receiver(post_save, sender=User)
#def email(sender, instance, created, **kwargs):
#    if created:
#        send_mail(
#            'Bienvenido a ABC BLOG',
#            str('Hola ' + instance.full_name + ', usted se ha registrado satisfactoriamente en el blog.'
#                                               '¡Es un placer que seas parte de nuestra familia!'),
#            config('EMAIL_HOST_USER'),
#            [instance.email]
#        )