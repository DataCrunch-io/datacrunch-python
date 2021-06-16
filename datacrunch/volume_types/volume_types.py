from typing import List

VOLUME_TYPES_ENDPOINT = '/volume-types'


class VolumeType:

    def __init__(self,
                 type: str,
                 price_per_month_per_gb: float) -> None:
        """Initialize a volume type object

        :param type: volume type name
        :type type: str
        :param price_per_month_per_gb: price per month per gb of storage
        :type price_per_month_per_gb: float
        """
        self._type = type
        self._price_per_month_per_gb = price_per_month_per_gb

    @property
    def type(self) -> str:
        """Get the volume type

        :return: volume type
        :rtype: str
        """
        return self._type

    @property
    def price_per_month_per_gb(self) -> str:
        """Get the volume price_per_month_per_gb

        :return: volume price_per_month_per_gb
        :rtype: str
        """
        return self._price_per_month_per_gb

    def __str__(self) -> str:
        """Prints the volume type

        :return: volume type string representation
        :rtype: str
        """
        return f'type: {self._type}\nprice_per_month_per_gb: ${self._price_per_month_per_gb}'


class VolumeTypesService:
    """A service for interacting with the volume-types endpoint"""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self) -> List[VolumeType]:
        """Get all volume types

        :return: list of volume type objects
        :rtype: List[VolumesType]
        """
        volume_types = self._http_client.get(VOLUME_TYPES_ENDPOINT).json()
        volume_type_objects = list(map(lambda volume_type: VolumeType(
            type=volume_type['type'],
            price_per_month_per_gb=volume_type['price']['price_per_month_per_gb'],
        ), volume_types))

        return volume_type_objects
