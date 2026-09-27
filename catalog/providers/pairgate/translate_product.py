import re

from .fetch_product import collect_products


def structured_products(discoveries):
    products = {}
    seen_ids = {}

    products_list, missing_track = collect_products(discoveries)

    for item in products_list:

        provider = item["discovery"]["provider_name"]
        plan_type = item["discovery"]["plan_type"]

        product_payload = item["products"]
        product_content = product_payload.get("data", {})
        provider_plans = product_content.get(provider, [])

        # Create provider bucket
        if provider not in products:
            products[provider] = {}

        # Create plan-type bucket
        if plan_type not in products[provider]:
            products[provider][plan_type] = []

        # Create duplicate-tracking bucket
        if provider not in seen_ids:
            seen_ids[provider] = {}

        if plan_type not in seen_ids[provider]:
            seen_ids[provider][plan_type] = set()

        # Add unique products
        for plan in provider_plans:

            plan_id = plan["plan_id"]

            if plan_id in seen_ids[provider][plan_type]:
                continue

            products[provider][plan_type].append(plan)
            seen_ids[provider][plan_type].add(plan_id)

    return products, missing_track



# parser patterns ______________

AMOUNT_PATTERN = re.compile(
    r"^\s*(?P<amount>\d+(?:\.\d+)?\s*(?:MB|GB|TB))\b",
    re.IGNORECASE,
)

# normalizing amoubt
def normalize_product_name(name):
    normalized = {
        "amount": None,
    }

    amount_match = AMOUNT_PATTERN.search(name)
    if amount_match:
        normalized["amount"] = (
            amount_match.group("amount").replace(" ", "").upper()
        )

    return normalized

def translate_products(discoveries):
    # elite data products bucket
    products_list=[]
    

    structured_data, missing_tracks = structured_products(discoveries)  

    for provider_name, plan in structured_data.items():
        

        for plan_type, products in plan.items():


            for product in products:

                normalized_name = normalize_product_name(product["name"])

                products_list.append({
                    "supplier_name" : product["name"] ,
                    "provider_plan_id": product["plan_id"],
                    "supplier_plan_type": plan_type,
                    "amount": normalized_name["amount"],
                    "duration": product["duration"],
                    "provider_price": product["price"],
                    "provider_name": provider_name,
                })

    return products_list, missing_tracks






   