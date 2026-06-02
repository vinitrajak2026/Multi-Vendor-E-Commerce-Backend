from django.db import models


class Usermodel(models.Model):

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('seller','Seller'),
        ('customer','Customer')
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Seller Shop Details
    shop_name = models.CharField(max_length=150, blank=True, null=True)
    shop_description = models.TextField(blank=True, null=True)
    shop_address = models.TextField(blank=True, null=True)

    # UPI Billing Details
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    upi_qr_url = models.URLField(max_length=500, blank=True, null=True)
    upi_qr_file = models.ImageField(upload_to='upi_qrs/', blank=True, null=True)

    def get_upi_qr(self):
        if self.upi_qr_file:
            return self.upi_qr_file.url
        if self.upi_qr_url:
            return self.upi_qr_url
        upi = self.upi_id or "revanth@upi"
        return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=upi://pay?pa={upi}%26pn={self.name}%26cu=INR"


class ProductModel(models.Model):

    seller = models.ForeignKey(
        Usermodel,
        on_delete=models.CASCADE
    )

    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=100)
    ptype = models.CharField(max_length=100)
    pprice = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    pquantity = models.IntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Product visual and text details
    pdescription = models.TextField(default="No description available.")

    # Image 1 (Toggled link or file upload)
    pimage_type1 = models.CharField(max_length=10, default='link') # 'file' or 'link'
    pimage1_url = models.URLField(max_length=500, blank=True, null=True)
    pimage1_file = models.ImageField(upload_to='products/', blank=True, null=True)

    # Image 2 (Toggled link or file upload)
    pimage_type2 = models.CharField(max_length=10, default='link') # 'file' or 'link'
    pimage2_url = models.URLField(max_length=500, blank=True, null=True)
    pimage2_file = models.ImageField(upload_to='products/', blank=True, null=True)

    def get_image1(self):
        if self.pimage_type1 == 'file' and self.pimage1_file:
            return self.pimage1_file.url
        return self.pimage1_url or "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"

    def get_image2(self):
        if self.pimage_type2 == 'file' and self.pimage2_file:
            return self.pimage2_file.url
        return self.pimage2_url or "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600"


class WishlistModel(models.Model):

    customer = models.ForeignKey(
        Usermodel,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class CartModel(models.Model):

    customer = models.ForeignKey(
        Usermodel,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class AddressModel(models.Model):

    customer = models.ForeignKey(
        Usermodel,
        on_delete=models.CASCADE
    )
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="India")

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state} - {self.postal_code}"


class OrderModel(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    )

    customer = models.ForeignKey(
        Usermodel,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    ordered_at = models.DateTimeField(
        auto_now_add=True
    )

    # Shipping and Payment Details
    shipping_address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, default="Cash on Delivery")


class ReviewModel(models.Model):

    customer = models.ForeignKey(
        Usermodel,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(default=5)

    review = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

