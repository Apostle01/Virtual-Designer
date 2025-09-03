from django.contrib import admin
from .models import Category, Clothing, UserPhoto, TryOnHistory


@admin.register(UserPhoto)
class UserPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uploaded_at')  # ✅ Now this works


@admin.register(TryOnHistory)
class TryOnHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clothing', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(Clothing)
class ClothingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'available_stock')
