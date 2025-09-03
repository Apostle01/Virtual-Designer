# from rembg import remove
# from io import BytesIO
# from django.core.files.base import ContentFile
# from PIL import Image
# import os
# from django.conf import settings

# def generate_tryon_result(user_photo_path, dress_path):
#     user_img = Image.open(user_photo_path).convert("RGBA")
#     dress_img = Image.open(dress_path).convert("RGBA")
#     dress_img = dress_img.resize((user_img.width, user_img.height))
#     combined = Image.alpha_composite(user_img, dress_img)
#     result_path = os.path.join(settings.MEDIA_ROOT, "results", os.path.basename(user_photo_path))
#     combined.save(result_path, "PNG")
#     return os.path.join("results", os.path.basename(user_photo_path))

# def make_cutout(django_file) -> ContentFile:
#     """
#     Takes a Django File (uploaded image), returns a ContentFile of PNG with transparent background.
#     """
#     # Read original bytes
#     src_bytes = django_file.read()
#     # Run rembg
#     output_bytes = remove(src_bytes)  # returns PNG bytes with alpha
#     # Optionally ensure it's a valid PNG via PIL (and to manipulate size if ever needed)
#     with Image.open(BytesIO(output_bytes)) as im:
#         buf = BytesIO()
#         im.save(buf, format="PNG")
#         return ContentFile(buf.getvalue())
