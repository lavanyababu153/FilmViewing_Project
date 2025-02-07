from django.db import models
from Admin_App.models import *
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Viewers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1) 
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    username=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    password=models.CharField(max_length=20)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comment_set')
    user = models.ForeignKey(Viewers, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Subscription_user(models.Model):
    plan=models.ForeignKey(Subscription_plan,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,default="inactive")
    user=models.ForeignKey(Viewers,on_delete=models.CASCADE)
    start_date=models.DateField()   
    end_date=models.DateField()
    payment_status = models.CharField(max_length=50, default="pending")
  

 

class User_like(models.Model):
    user=models.ForeignKey(Viewers,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    action=models.CharField(max_length=20)



class Favourite(models.Model):
    user = models.ForeignKey(Viewers, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('wallet', 'Wallet'),
    ]
    
    PAYMENT_STATUSES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey('Viewers', on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey('Subscription_user', on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 999.99
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUSES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True) 
    payment_date = models.DateTimeField(default=now)
   
    def __str__(self):
        return f"Payment #{self.id} by {self.user.username} - {self.status}"



    
 

