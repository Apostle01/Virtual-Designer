from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Clothing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="clothes")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    available_stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="clothing/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class UserPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="uploads/", default="user_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)  # ✅ RESTORE THIS FIELD

    def __str__(self):
        return f"{self.user.username} - {self.photo.name}"


class TryOnHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_photo = models.ForeignKey(UserPhoto, on_delete=models.CASCADE)  # ✅ REMOVE default=1
    clothing = models.ForeignKey(Clothing, on_delete=models.CASCADE, null=True, blank=True)
    result_image = models.ImageField(upload_to='tryon_results/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Try-on: {self.user.username} - {self.clothing.name}"
