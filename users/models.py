from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse



class UserProfile(models.Model):
    SEX = ((None, 'Cinsiyet Seçiniz'), ('diger', 'DİGER'), ('erkek', 'ERKEK'), ('kadın', 'KADIN'))
    user = models.OneToOneField(User, null=True, blank=False, verbose_name='User', on_delete=models.PROTECT)
    bio = models.TextField(max_length=1000, verbose_name='Hakkımda', blank=True, null=True)
    profile_photo = models.ImageField(null=True, blank=True, verbose_name='Profil Fotograf')
    dogum_tarihi = models.DateField(null=True, blank=True, verbose_name='Dogum Tarihi')
    sex = models.CharField(choices=SEX, blank=True, null=True, max_length=6, verbose_name='Cinsiyet')

    class Meta:
        verbose_name_plural = 'Kullanici Profilleri'
    def get_screen_name(self):
        user = self.user
        if user.get_full_name():
            return user.get_full_name()
        return user.username

    def get_user_profile_url(self):
        url = reverse('userprofile', kwargs={'username': self.user.username})
        return url

    def __str__(self):
        return "%s Profile" % (self.get_screen_name())

    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return "/static/img/default.png"

    def user_full_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return None

