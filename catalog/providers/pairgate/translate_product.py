import re
from .fetch_product import collect_products
from monitoring.services import Monitoring
from monitoring.models import Alert
from .validator import is_positive_decimal, is_string_valid, is_positive_integer

def structured_products(discoveries):
    products = {}
    seen_ids = {}

    products_list, failed_tracks = collect_products(discoveries)

    for item in products_list:

        provider = item["discovery"]["provider_name"]
        plan_type = item["discovery"]["plan_type"]

        if not provider:
            Monitoring.alert(
                alert_type=Alert.Type.PROVIDER_RESPONSE_UNEXPECTED,
                description="A provider is missing"
            )
            failed_tracks.append(item)
            continue

        product_payload = item["products"]

        if not product_payload:
            failed_tracks.append(item)
            Monitoring.alert(
                alert_type=Alert.Type.PROVIDER_RESPONSE_UNEXPECTED,
                description="provider returned Empty data set"
            )
            continue
            

        if not isinstance(product_payload, dict):
            Monitoring.alert(
                alert_type=Alert.Type.PROVIDER_RESPONSE_UNEXPECTED,
                description="product type not a dictionary"
            )
            failed_tracks.append(item)
            continue
            

        product_content = product_payload.get("data", {})
        if not isinstance(product_content, dict):
            Monitoring.alert(
                alert_type=Alert.Type.PROVIDER_CONTRACT_CHANGED,
                description="expect dictionary "
            )
            failed_tracks.append(item)
            continue
        provider_plans = product_content.get(provider, [])

        if not isinstance(provider_plans, list):
            Monitoring.alert(
                alert_type=Alert.Type.PROVIDER_RESPONSE_UNEXPECTED,
                description="providers plan changed from  expected contract"
            )
            failed_tracks.append(item)
            continue



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

            if not plan or not isinstance(plan, dict):
                Monitoring.alert(
                    alert_type=Alert.Type.PROVIDER_RESPONSE_UNEXPECTED,
                    description=f"unexpected plan type"
                )
                failed_tracks.append(plan)
                continue

            plan_id = plan["plan_id"]
            if not plan_id:
                Monitoring.alert(
                    alert_type=Alert.Type.PROVIDER_RESPONSE_UNEXPECTED,
                    description="invalid plan",
                )
                failed_tracks.append(plan)
                continue

            if plan_id in seen_ids[provider][plan_type]:
                continue

            products[provider][plan_type].append(plan)
            seen_ids[provider][plan_type].add(plan_id)

    return products, failed_tracks



# parser patterns ______________

AMOUNT_PATTERN = re.compile(
    r"^\s*(?P<amount>\d+(?:\.\d+)?\s*(?:MB|GB|TB))\b",
    re.IGNORECASE,
)

# normalizing amount
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



# perform monitoring documentation
def record_monitoring(product):
    Monitoring.alert(
        alert_type=Alert.Type.PROVIDER_RESPONSE_UNEXPECTED,
        description=f"provider's expected contract change -> {product['name']}",
    )

    

def translate_products(discoveries):
    # elite data products bucket
    products_list=[]
    

    structured_data, failed_tracks = structured_products(discoveries)  

    for provider_name, plan in structured_data.items():
        

        for plan_type, products in plan.items():


            for product in products:
                expected_keys = ["plan_id", "name", "price", "duration"]
            
                
                if not all(key in product for key in expected_keys):
                    Monitoring.alert(
                        alert_type=Alert.Type.PROVIDER_CONTRACT_CHANGED,
                        description="providers response unexpectedly.",
                        severity=Alert.Severity.CRITICAL
                    )
                    continue


                if not is_string_valid(product["name"]):
                    record_monitoring(product)
                    continue
                normalized_name = normalize_product_name(product["name"])

                if not is_string_valid(product["plan_id"]):
                    record_monitoring(product)
                    continue

                if not is_positive_decimal(product["price"]):
                    record_monitoring(product)
                    continue

                if not is_positive_integer(product["duration"]):
                    record_monitoring(product)
                    continue


                products_list.append({
                    "supplier_name" : product["name"] ,
                    "provider_plan_id": product["plan_id"],
                    "supplier_plan_type": plan_type,
                    "amount": normalized_name["amount"],
                    "duration": product["duration"],
                    "provider_price": product["price"],
                    "provider_name": provider_name,
                })

    return products_list, failed_tracks



