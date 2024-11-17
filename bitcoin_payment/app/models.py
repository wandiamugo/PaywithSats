from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    public_key = models.CharField(max_length=130, unique=True)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username

class ServiceProvider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bitcoin_address = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    access_url = models.URLField()

    def __str__(self):
        return self.title

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} for {self.content.title}"
