import requests
from bs4 import BeautifulSoup

def get_price_from_amazon(product_set_number):
    url = f"https://www.amazon.com/s?k={product_set_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    price_span = soup.find("span", {"class": "a-price-whole"})
    if price_span:
        price_text = price_span.text.strip()
        price = float(price_text.replace(",", ""))
        return price
    return None

def get_price_from_target(product_set_number):
    url = f"https://www.target.com/s?searchTerm={product_set_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    price_span = soup.find("span", {"data-test": "product-price"})
    if price_span:
        # Remove $ sign
        price_text = price_span.text.strip()[1:]
        price = float(price_text.replace(",", ""))
        return price
    return None

def get_price_from_walmart(product_set_number):
    url = f"https://www.walmart.com/search/?query={product_set_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    price_span = soup.find("span", {"class": "price-characteristic"})
    if price_span:
        # Walmart has price in 'content' attribute apparently
        price_text = price_span["content"]
        price = float(price_text)
        return price
    return None

def get_price_from_macys(product_set_number):
    url = f"https://www.macys.com/shop/featured/{product_set_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    price_span = soup.find("span", {"class": "price"})
    if price_span:
        # Remove $ sign
        price_text = price_span.text.strip()[1:]
        price = float(price_text.replace(",", ""))
        return price
    return None

def get_price_from_bestbuy(product_set_number):
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={product_set_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    price_span = soup.find("div", {"class": "priceView-hero-price priceView-customer-price"})
    if price_span:
        # Remove $ sign
        price_text = price_span.find("span").text.strip()[1:]
        price = float(price_text.replace(",", ""))
        return price
    return None

def track_price(product_set_number, original_price):
    # Check each retailer for the product price
    amazon_price = get_price_from_amazon(product_set_number)
    target_price = get_price_from_target(product_set_number)
    walmart_price = get_price_from_walmart(product_set_number)
    macys_price = get_price_from_macys(product_set_number)
    bestbuy_price = get_price_from_bestbuy(product_set_number)

    print(f"\nPrice Check for Set Number {product_set_number}:")
    
    if amazon_price:
        print(f"Amazon: ${amazon_price} {'(Price Drop!)' if amazon_price < original_price else ''}")
    else:
        print("Amazon: Not available")

    if target_price:
        print(f"Target: ${target_price} {'(Price Drop!)' if target_price < original_price else ''}")
    else:
        print("Target: Not available")

    if walmart_price:
        print(f"Walmart: ${walmart_price} {'(Price Drop!)' if walmart_price < original_price else ''}")
    else:
        print("Walmart: Not available")

    if macys_price:
        print(f"Macy's: ${macys_price} {'(Price Drop!)' if macys_price < original_price else ''}")
    else:
        print("Macy's: Not available")

    if bestbuy_price:
        print(f"Best Buy: ${bestbuy_price} {'(Price Drop!)' if bestbuy_price < original_price else ''}")
    else:
        print("Best Buy: Not available")

# Input set number and original price
product_set_number = input("Enter the LEGO set number: ")
original_price = float(input("Enter the original price: "))

# Track price
track_price(product_set_number, original_price)