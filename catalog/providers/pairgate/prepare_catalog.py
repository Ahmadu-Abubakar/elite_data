from .pricing import pricing


def prepare_catalog():

    products = []

    data = pricing()


    for product in data:
        products.append({
            "product_id": product["provider_plan_id"],
            "provider_name" : product["provider_name"],
            "amount" : product["amount"],
            "price"  : str(product["selling_price"]),
            "validity"  : product["duration"],
            "duration_category" : product["duration_category"],
            "plan_type_category" : product["plan_type_category"]
        })

    return products

