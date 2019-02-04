from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=1000, help_text="Enter something about your bio")

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.user.id)])

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Blogger.objects.create(user=instance)
    instance.blogger.save()

class Blog(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=2000, help_text="Enter a brief description of the blog")
    date = models.DateField()
    author = models.ForeignKey('Blogger', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date"]

class Comment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    author = models.ForeignKey('Blogger', on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField(max_length=3000, help_text="Enter your comment for the blog")

    def __str__(self):
        return "{0} ({1}) Blog - {2}".format(self.author.user.username, self.date, self.blog.name)

    class Meta:
        ordering = ["date"]