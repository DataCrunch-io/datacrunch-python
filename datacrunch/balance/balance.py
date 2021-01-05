from typing import Dict

BALANCE_ENDPOINT = '/balance'


class Balance:
    """A balance model class"""

    def __init__(self, amount: float, currency: str) -> None:
        """Initialize a new Balance object

        :param amount: Balance amount
        :type amount: float
        :param currency: currency code
        :type currency: str
        """
        self._amount = amount
        self._currency = currency

    @property
    def amount(self) -> float:
        """Get the balance amount

        :return: amount
        :rtype: float
        """
        return self._amount

    @property
    def currency(self) -> str:
        """Get the currency code

        :return: currency code
        :rtype: str
        """
        return self._currency


class BalanceService:
    """A service for interacting with the balance endpoint"""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self) -> Balance:
        """Get the client's current balance

        :return: Balance object containing the amount and currency.
        :rtype: Balance
        """
        balance = self._http_client.get(BALANCE_ENDPOINT).json()
        return Balance(balance["amount"], balance["currency"])
