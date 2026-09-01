from catalog.exceptions import *
import requests
from django.conf import settings
import logging
logger=logging.getLogger(__name__)

def discover_available_products():
        url = f"{settings.PAIRGATE_BASE_URL}/data-plans/categories"
        secret_key = settings.PAIRGATE_SECRET_KEY


        headers = {
            "Authorization" : f"Bearer {secret_key}",
            "Cache-Control" : "no-cache",
            "Content-Type"  : "application/json"
        }


        try:

            response = requests.get(url, headers=headers, timeout=15)

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

        product_list = data.get("data", [])

        if not product_list:
            logger.debug(
                "PairGate discovery returned no provider/category combinations."
            )
            raise ProviderEmptyResponse("No data found in PairGate catalog.")

        return product_list
# isinstance(data, dict) and "data" in data and not data["data"]
        