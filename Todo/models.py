from django.db import models


# Create your models here.


class Member(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.TextField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} | {self.username}'


class Task(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    text = models.TextField()
    priority = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} | {self.user} | {self.date}'
