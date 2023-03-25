from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey



class Kategoriler(models.Model):
    isim=models.CharField(max_length=15, verbose_name="Kategoriismi")

    class Meta:
        verbose_name_plural="Kategoriler"
    def __str__(self):
        return self.isim

class Blog(models.Model):
    title = models.CharField(max_length=100,blank=False,null=True, verbose_name="başlık giriniz",help_text="başlık bilgisi burada girilir")

    user = models.ForeignKey(User, default=1, null=True, verbose_name='User', related_name='blog',on_delete=models.CASCADE)
    icerik=RichTextField(null=True,blank=False,max_length=5000,verbose_name="içerik")
    created_date=models.DateField(auto_now_add=True,auto_now=False)
    kategori=models.ManyToManyField(to=Kategoriler)
    resim=models.ImageField(verbose_name="resim",null=True,default=None)

    class Meta:
        verbose_name_plural="gönderiler"
        ordering=["-id"]
    def __str__(self):
        return "%s %s"%(self.title,self.user)
    #gönderiye ait tüm yorumları çağıran fonksiyon
    def get_blog_comment(self):
        return self.comment.all()





class Comment(models.Model):
    user = models.ForeignKey(User, default=1, null=True, related_name='comment',on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,null=True,on_delete=models.CASCADE,related_name='comment')
    comment_date = models.DateTimeField(auto_now_add=True, null=True)
    icerik=models.TextField(verbose_name='yorum',blank=False,max_length=1000,null=True,)
    class Meta:
        verbose_name_plural="yorumlar"


    def __str__(self):
        return "%s %s" % (self.user,self.blog)


    def get_screen_name(self):
        if self.user.first_name:
            return "%s"%(self.user.get_full_name())
        return self.username
