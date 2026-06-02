import os
import sys
import django

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "multivendorecommerce.settings")
django.setup()

from flipazon.models import Usermodel, ProductModel, AddressModel

def seed():
    print("Seeding professional e-commerce details...")
    
    # 1. Update Sellers with Shop Details & UPI IDs
    sellers = Usermodel.objects.filter(role="seller")
    for i, seller in enumerate(sellers):
        # Seed Shop details
        if not seller.shop_name:
            if i % 2 == 0:
                seller.shop_name = "ElectroWorld India"
                seller.shop_description = "Your one-stop destination for high-end tech, accessories, and smartphones."
                seller.shop_address = "42, Brigade Road, Tech Zone, Bangalore, KA, 560025"
            else:
                seller.shop_name = "Vogue Styles & Co."
                seller.shop_description = "Curated premium fashion, apparel, footwear, and designer accessories."
                seller.shop_address = "Sector 5, HSR Layout, Fashion Hub, Bangalore, KA, 560102"
        
        # Seed UPI IDs
        if not seller.upi_id:
            if i % 2 == 0:
                seller.upi_id = "revanth@upi"
            else:
                seller.upi_id = "pavansai@upi"
                
        seller.save()
        print(f"Updated seller {seller.email} with shop {seller.shop_name} and UPI {seller.upi_id}")

    # 2. Update Customers with Shipping Addresses
    customers = Usermodel.objects.filter(role="customer")
    for customer in customers:
        if not AddressModel.objects.filter(customer=customer).exists():
            AddressModel.objects.create(
                customer=customer,
                address_line1="Apartment 4B, Blue Towers, Indiranagar",
                city="Bangalore",
                state="Karnataka",
                postal_code="560038",
                country="India"
            )
            AddressModel.objects.create(
                customer=customer,
                address_line1="G-9, Tech Enclave, Phase 3, Gachibowli",
                city="Hyderabad",
                state="Telangana",
                postal_code="500032",
                country="India"
            )
            print(f"Created two saved addresses for customer {customer.email}")

    # 3. Update Products with Professional Descriptions & 2 High-Quality Images (Unsplash)
    products = ProductModel.objects.all()
    for product in products:
        name_lower = product.pname.lower()
        type_lower = product.ptype.lower()
        
        # Default types
        product.pimage_type1 = 'link'
        product.pimage_type2 = 'link'
        
        # Determine product theme
        if "phone" in name_lower or "mobile" in name_lower:
            product.pdescription = "Experience next-generation performance with this premium smartphone. Featuring an ultra-clear screen, high-capacity battery, and advanced triple-camera system for taking stunning photos in any lighting conditions."
            product.pimage1_url = "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&auto=format&fit=crop&q=80"
            product.pimage2_url = "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80"
        elif "laptop" in name_lower or "computer" in name_lower or "mac" in name_lower:
            product.pdescription = "Engineered for creators and professionals. This high-performance laptop offers lightning-fast speeds, stunning display clarity, and all-day battery life, allowing you to tackle demanding tasks with ease."
            product.pimage1_url = "https://images.unsplash.com/photo-1496181130204-755241524eab?w=600&auto=format&fit=crop&q=80"
            product.pimage2_url = "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop&q=80"
        elif "shoe" in name_lower or "sneaker" in name_lower or "boot" in name_lower:
            product.pdescription = "Walk, run, or train in absolute comfort. These premium athletic sneakers feature responsive cushioning, mesh panels for maximum breathability, and a durable rubber outsole for superior grip."
            product.pimage1_url = "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80"
            product.pimage2_url = "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&auto=format&fit=crop&q=80"
        elif "head" in name_lower or "ear" in name_lower or "audio" in name_lower:
            product.pdescription = "Immerse yourself in pure studio sound quality. These active noise-canceling wireless headphones deliver crisp highs, deep bass, and comfortable memory-foam ear cups for extended listening sessions."
            product.pimage1_url = "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80"
            product.pimage2_url = "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600&auto=format&fit=crop&q=80"
        else:
            # Fallback based on type or generic category
            if "electronic" in type_lower or "tech" in type_lower:
                product.pdescription = "A premium tech product designed to make your daily life smarter and more efficient. Highly rated by customers and crafted with high-durability materials."
                product.pimage1_url = "https://images.unsplash.com/photo-1468436139062-f60a71c5c892?w=600&auto=format&fit=crop&q=80"
                product.pimage2_url = "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=600&auto=format&fit=crop&q=80"
            else:
                product.pdescription = "Add a touch of style to your collection with this high-quality product. Modern design, vibrant details, and crafted using sustainable materials built to last."
                product.pimage1_url = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80"
                product.pimage2_url = "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&auto=format&fit=crop&q=80"
                
        product.save()
        print(f"Updated product {product.pname} with description and images.")
        
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed()
