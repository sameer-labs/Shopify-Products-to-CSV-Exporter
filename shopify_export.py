import os
import csv
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Shopify API credentials from environment variables
shop_name = os.getenv("Shopify_shop_name") # e.g. "Your-store"
access_token = os.getenv("Shopify_access_token") # Your private app token
api_version = "2024-01" # Shopify API version

base_url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}"

def fetch_products():
    all_products = []
    url = f"{base_url}/products.json"
     
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
     }
    
    params = {
        "limit": 250 # Maximum products per page (Shopify limit)
    }

    print("Fetching products from Shopify...")

    # Loop through pages until no more products are returned
    while url:
        response = requests.get(url, headers=headers, params=params)

        # Safety check
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        products = data.get("products", [])
        all_products.extend(products)

        print(f"Fetched {len(products)} products (Total: {len(all_products)})")

        # Check for next page link in response headers
        link_header = response.headers.get("Link", "")
        if 'rel="next"' in link_header:
            # Extract next page url from header
            next_link = [link.split(";")[0].strip("<>") for link in link_header.split(",") if 'rel="next"' in link]
            url = next_link[0] if next_link else None
            params = None
        else:
            url = None
    print(f"Total products fetched: {len(all_products)}\n")
    return all_products

def parse_products(raw_products):
    rows = []

    print("Parsing products data...")

    # Loop through each products
    for product in raw_products:
        products_id = product.get("id")
        title = product.get("title")
        vendor = product.get("vendor")
        status = product.get("status")

        # Each product can have multiple variants (size, colour, etc.)
        variants = product.get("variants", [])

        # Create a row for each variant
        for variant in variants:
            row = {
                "product_id": products_id,
                "title": title,
                "vendor": vendor,
                "sku": variant.get("sku", ""),
                "price": variant.get("price", "0.00"),
                "inventory_quantity": variant.get("inventory_quantity", 0),
                "status": status 
                }
            rows.append(row)

    print(f"Parsed {len(rows)} product variants\n")
    return rows

def save_csv(rows):

    # Create output directory (if it doesn't already exist)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Define output path
    output_file = output_dir / "shopify_products.csv" 

    # Define CSV column headers
    fieldnames = [
        "product_id",
        "title",
        "vendor",
        "sku",
        "price",
        "inventory_quantity",
        "status"   
    ]

    print(f"Writing CSV to {output_file}")

# Write data to CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Export complete! {len(rows)} rows written to {output_file}")

def main():
    # Validate that required environment variables are set
    if not shop_name or not access_token:
        print("Error: Missing Shopify_shop_name or Shopify_access_token in .env file")
        return
    
    print("=" * 50)
    print("Shopify Products → CSV Exporter")
    print("=" * 50 + "\n")

    # Step 1: Fetch products from Shopify API
    products = fetch_products()

    if not products:
        print("No product found or error occured")
        return

    # Step 2: Parse products into flat CSV rows
    rows = parse_products(products)

    # Step 3: Save to CSV file
    save_csv(rows)

if __name__ == "__main__":
    main()

