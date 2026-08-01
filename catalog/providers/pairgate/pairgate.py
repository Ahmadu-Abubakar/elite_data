from catalog.providers.base import BaseProvider
from django.conf import settings
import requests
from catalog.exceptions import (
    ProviderNetworkError,
    ProviderDataValidationError,
    ProviderAuthenticationError,
    ProviderEmptyResponse,
    ProviderHTTPError,
    ProviderTransactionFailed
)



class PairGateProvider(BaseProvider):

    def __init__(self, base_url, api_key):
        super().__init__(base_url, api_key)

    def get_products(self):
        url = getattr(settings, "PAIRGATE_BASE_URL", self.base_url)
        secret_key = getattr(settings, "PAIRGATE_SECRETE_KEY", self.api_key)


        headers = {
            "Authorization" : f"Bearer {secret_key}",
            "Cache-Control" : "no-cache",
            "Content-Type"  : "application/json"
        }


        try:

            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 401 or 403:
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
            raise ProviderEmptyResponse (
                "PairGate returned an empty response with no products."
            )

        if isinstance(data, dict) and "data" in data and not data["data"]:
            raise ProviderEmptyResponse("No data found in PairGate catalog.")

        return data

        
