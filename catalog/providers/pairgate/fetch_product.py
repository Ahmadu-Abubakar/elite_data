from catalog.exceptions import *
import requests
from django.conf import settings
import logging
logger=logging.getLogger(__name__)
from .discover_products import discover_available_products

def fetch(discovery):
        url = f"{settings.PAIRGATE_BASE_URL}/data-plans"
        secret_key = settings.PAIRGATE_SECRET_KEY


        headers = {
            "Authorization" : f"Bearer {secret_key}",
            "Cache-Control" : "no-cache",
            "Content-Type"  : "application/json"
        }


        params={
            # PairGate currently expects provider_name under the provider_id parameter.
            # If PairGate changes to UUIDs later, only this mapping needs updating.
            "provider_id" : discovery["provider_name"],
            "plan_type"  : discovery["plan_type"]
        }


        try:

            response = requests.get(url, headers=headers, params=params, timeout=15)

            if response.status_code in (401, 403):
                raise ProviderAuthenticationError (
                    "Invalid PairGate API key or unauthorized access "
                )

            response.raise_for_status()
           

        except requests.exceptions.Timeout as e:
            raise ProviderNetworkError(
                'The request to PairGate timed out. '
            )  from e
        except requests.exceptions.ConnectionError:
            raise ProviderNetworkError (
               " Failed to connect pairgate sever. Check internet/DNS"
            ) 
        except requests.exceptions.HTTPError as e:
            raise ProviderHTTPError(
                message=f"PairGate returned an HTTP error: {e}",
                status_code=response.status_code,
                response_body=response.text
            )

        except requests.exceptions.RequestException as e:
            raise ProviderNetworkError (
                f"An unexpected networking error occurred: {e}"
            )

        try :
            data = response.json()
        except ValueError:
            raise ProviderDataValidationError(
                "Failed to parse response payload as valid JSON."
            )

        if not data:
            logger.debug(
                "PairGate response with an empty product's List"
            )
            raise ProviderEmptyResponse (
                "PairGate returned an empty response with no products."
            )
        return data


def collect_products():
    discoveries = discover_available_products()
    
    raw_catalog = []
    
    for discovery in discoveries:
        try:
          
            api_response = fetch(discovery)

            raw_catalog.append({
                "discovery": {
                    "provider_name": discovery['provider_name'], 
                    "plan_type": discovery['plan_type']
                },
                "products": api_response
            })
        except (ProviderNetworkError, ProviderHTTPError, ProviderDataValidationError) as e:
            logger.error(f"Failed to fetch data for {discovery['provider_name']} - {discovery['plan_type']}: {e}")
            continue

    return raw_catalog

