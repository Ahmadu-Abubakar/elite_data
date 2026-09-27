from catalog.providers.pairgate.fetch_product import fetch
from catalog.exceptions import *
import logging
from dataclasses import dataclass


logger = logging.getLogger(__name__)

RETRY_POLICY = {
    "RATE_LIMITING": 3,
    "TIMEOUT": 3,
    "SERVER_ERROR": 1,
    "AUTHENTICATION_ERROR": 0,
}


class Retry:

    def __init__(self, failed_tracks):
        self.failed_tracks = failed_tracks

    def apply_retry_policy(self):
        succeeded = []
        exhausted = []

        for track in self.failed_tracks:

            failure_type = track["failure"]["type"]
            attempts = RETRY_POLICY.get(failure_type, 0)

            if attempts == 0:
                exhausted.append(track)
                continue

            discovery = {
                "provider_id": track["provider_id"],
                "provider_name": track["provider_name"],
                "plan_type": track["plan_type"],
                "service_type": track["service_type"],
            }

            for attempt in range(attempts):

                try:
                    products = fetch(discovery)

                    succeeded.append({
                        "track": track,
                        "products": products,
                    })

                    break

                except (
                    ProviderRatelimitingError,
                    ProviderTimeoutError,
                    ProviderHTTPError,
                    ProviderNetworkError,
                ) as e:

                    logger.warning(
                        f"Retry {attempt + 1}/{attempts} failed "
                        f"for {track['provider_name']} - "
                        f"{track['plan_type']}: {e}"
                    )

                    if attempt == attempts - 1:
                        exhausted.append(track)

        return RetryResult(
            succeeded=succeeded,
            exhausted=exhausted,
        )



@dataclass
class RetryResult:
    succeeded: list
    exhausted: list
        
