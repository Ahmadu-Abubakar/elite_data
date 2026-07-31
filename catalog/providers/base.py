from abc import ABC, abstractmethod


class BaseProvider(ABC):

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key


    @abstractmethod
    def get_products(self):
        """Fetch products from supplier."""
        pass

    @abstractmethod
    def purchase_data(self, payload):
        """Purchase data."""
        pass

    @abstractmethod
    def purchase_airtime(self, payload):
        """Purchase airtime."""
        pass

    @abstractmethod
    def transaction_status(self, provider_reference):
        """Check supplier transaction status."""
        pass