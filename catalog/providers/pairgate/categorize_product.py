from .translate_product import translate_products


def categorize_products():
    # collect the data

    data = translate_products()


    # social keyword 
    SOCIAL_KEYWORDS = ["social", "whatsapp", "facebook", "instagram", "tiktok", "youtube"]




    for product in data: 
     # Plan Type Category ________________


        # name in lower case
        name_lower =  product["supplier_name"].lower()

        if "night" in name_lower:
            product["plan_type_category"] = "Night"
        elif "weekend" in name_lower: 
            product["plan_type_category"] = "Weekend"
        elif any(keyword in name_lower for keyword in SOCIAL_KEYWORDS):
            product["plan_type_category"] = "Social"
        elif "special" in name_lower:
            product["plan_type_category"] = "Special"
        else :
            product["plan_type_category"] = "Standard"


    # Duration Category___________

        # duration variable
        duration = product.get("duration", 0)

        if 1 <= duration <= 6:
            product["duration_category"] = "Daily"
        elif 7 <= duration <= 20:
            product["duration_category"] = "Weekly"
        elif 21 <= duration <= 40:
            product["duration_category"] = "Monthly"
        else :
            product["duration_category"] = "Long_term"

    return data

