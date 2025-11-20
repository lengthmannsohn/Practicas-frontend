from django.db import models


class Professional(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    price_from = models.IntegerField(null=True, blank=True)
    price_to = models.IntegerField(null=True, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='free')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-plan', 'alias']

    def __str__(self):
        return self.alias


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
