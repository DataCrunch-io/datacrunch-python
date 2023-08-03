from typing import List

LOCATIONS_ENDPOINT = '/locations'


class LocationsService:
    """A service for interacting with the locations endpoint"""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self) -> List[dict]:
        """Get all locations
        """
        locations = self._http_client.get(LOCATIONS_ENDPOINT).json()
        return locations
