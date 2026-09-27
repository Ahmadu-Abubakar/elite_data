from .categorize_product import categorize_products
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR



# Hybrid Strategy

def hybrid_strategy(price):
    # converting incoming "price " to decimal
    price = Decimal(str(price))

    PRICING_PERCENTAGE = Decimal("0.15")
    MINIMUM_MARGIN = Decimal("25.00")

    price_percentage = price * PRICING_PERCENTAGE
    remainder = price_percentage %  1 


    if remainder >= Decimal('0.70'): 
        rounded_output = price_percentage.quantize(Decimal("1"), rounding=ROUND_CEILING)
    else:
        rounded_output = price_percentage.quantize(Decimal("1"), rounding=ROUND_FLOOR)

    margin = max(MINIMUM_MARGIN, rounded_output)

    final_price = price +  margin
    return {
        "selling_price" : final_price.quantize(Decimal("0.01")),
        "margin" : margin
    } 

# the pricing worker
def pricing(product_list):
    products, missing_products = categorize_products(product_list)

    for product in products:
        price = hybrid_strategy(product["provider_price"])
        product["margin"] = price["margin"]
        product["selling_price"] = price["selling_price"]

    return products, missing_products



