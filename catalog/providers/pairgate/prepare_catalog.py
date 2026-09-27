from .pricing import pricing


def prepare_catalog(products):

    products_list = []

    data, missing_products = pricing(products)


    for product in data:
        products_list.append({
            "provider_plan_id": product["provider_plan_id"],
            "provider_name" : product["provider_name"],
            "amount" : product["amount"],
            "price"  : product["selling_price"],
            "validity"  : product["duration"],
            "duration_category" : product["duration_category"],
            "plan_type_category" : product["plan_type_category"],
            "margin"  : product["margin"],
            "supplier_price" : product["provider_price"]

        })

    return products_list, missing_products

