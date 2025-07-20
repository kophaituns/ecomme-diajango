# Script tự động sửa đường dẫn ảnh sản phẩm về đúng chuẩn Django
# Chạy script này bằng lệnh: python fix_product_image_path.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from ecom.models import Product
from django.conf import settings

count = 0
for p in Product.objects.all():
    if p.product_image and not str(p.product_image).startswith('product_image/'):
        filename = os.path.basename(str(p.product_image))
        product_image_dir = os.path.join(settings.MEDIA_ROOT, 'product_image')
        file_path = os.path.join(product_image_dir, filename)
        # Nếu file đã nằm đúng thư mục
        if os.path.exists(file_path):
            p.product_image = 'product_image/' + filename
            p.save()
            count += 1
        # Nếu file nằm nhầm ở media/ thì di chuyển về đúng thư mục
        else:
            wrong_path = os.path.join(settings.MEDIA_ROOT, filename)
            if os.path.exists(wrong_path):
                # Tạo thư mục nếu chưa có
                os.makedirs(product_image_dir, exist_ok=True)
                os.rename(wrong_path, file_path)
                p.product_image = 'product_image/' + filename
                p.save()
                count += 1
                print(f"Đã di chuyển {filename} về đúng thư mục product_image/")
            else:
                print(f"Ảnh {filename} không tồn tại trong media/product_image hoặc media/, bỏ qua!")
print(f"Đã sửa {count} sản phẩm có đường dẫn ảnh sai!")
