import os
from PIL import Image
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Clothing, Category, UserPhoto, TryOnHistory
from .forms import SignUpForm, PhotoUploadForm

def home(request):
    categories = Category.objects.all()
    clothes = Clothing.objects.all()
    return render(request, "virtual_try_on/home.html", {
        "categories": categories,
        "clothes": clothes
    })

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "virtual_try_on/signup.html", {"form": form})

def generate_tryon_result(user_photo, clothing):
    try:
        # Paths
        user_image_path = user_photo.photo.path
        clothing_path = clothing.image.path

        # Open images
        user_image = Image.open(user_image_path).convert("RGBA")
        clothing_image = Image.open(clothing_path).convert("RGBA")

        # Resize clothing image to fit user image width
        clothing_image = clothing_image.resize((user_image.width, int(user_image.height / 2)))

        # Position clothing
        position = (0, int(user_image.height / 2))
        combined = user_image.copy()
        combined.paste(clothing_image, position, clothing_image)

        # Save result
        result_dir = os.path.join(settings.MEDIA_ROOT, "tryon_results")
        os.makedirs(result_dir, exist_ok=True)

        result_filename = f"tryon_{user_photo.id}_{clothing.id}.png"
        result_path = os.path.join(result_dir, result_filename)
        combined.save(result_path, format="PNG")

        # Save history
        TryOnHistory.objects.create(
            user=user_photo.user,
            user_photo=user_photo,
            clothing=clothing,
            result_image=f"tryon_results/{result_filename}"
        )
        return True

    except Exception as e:
        print("Try-On Generation Error:", e)
        return False


@login_required
def dashboard(request):
    clothing_items = Clothing.objects.all()
    categories = Category.objects.all()
    user_photos = UserPhoto.objects.filter(user=request.user).order_by("-uploaded_at")
    tryon_history = TryOnHistory.objects.filter(user=request.user).order_by("-created_at")

    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_photo = form.save(commit=False)
            uploaded_photo.user = request.user
            uploaded_photo.save()

            # Get selected clothing
            clothing_id = request.POST.get("clothing")
            if clothing_id:
                clothing = get_object_or_404(Clothing, id=clothing_id)

                # Generate try-on result
                generate_tryon_result(uploaded_photo, clothing)

            return redirect("dashboard")
    else:
        form = PhotoUploadForm()

    context = {
        "form": form,
        "clothing_items": clothing_items,
        "categories": categories,
        "user_photos": user_photos,
        "tryon_history": tryon_history,
    }
    return render(request, "virtual_try_on/dashboard.html", context)

@login_required
def clothing_list(request):
    clothes = Clothing.objects.all()
    categories = Category.objects.all()
    return render(request, "virtual_try_on/clothing_list.html", {"clothes": clothes, "categories": categories})


@login_required
def try_on(request, clothing_id):
    clothing = get_object_or_404(Clothing, pk=clothing_id)
    user_photos = UserPhoto.objects.filter(user=request.user).order_by("-uploaded_at")
    
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # ✅ Save uploaded photo
            uploaded_photo = form.save(commit=False)
            uploaded_photo.user = request.user
            uploaded_photo.save()
            
            # ✅ Get selected clothing if provided in the form
            selected_clothing = form.cleaned_data.get("clothing", clothing)
            
            # ✅ Generate try-on result image (this automatically creates TryOnHistory)
            generate_tryon_result(uploaded_photo, selected_clothing)

            # ✅ Redirect to dashboard after successful upload
            return redirect("dashboard")
    else:
        # ✅ Pre-select clothing in the form
        form = PhotoUploadForm(initial={"clothing": clothing})

    return render(request, "virtual_try_on/try_on.html", {
        "form": form,
        "clothing": clothing,
        "user_photos": user_photos
    })
