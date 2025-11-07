from dataclasses import dataclass

from dataclasses_json import dataclass_json

INSTANCE_TYPES_ENDPOINT = '/instance-types'


@dataclass_json
@dataclass
class InstanceType:
    """Instance type.

    Attributes:
        id: instance type id.
        instance_type: instance type, e.g. '8V100.48M'.
        price_per_hour: instance type price per hour.
        spot_price_per_hour: instance type spot price per hour.
        description: instance type description.
        cpu: instance type cpu details.
        gpu: instance type gpu details.
        memory: instance type memory details.
        gpu_memory: instance type gpu memory details.
        storage: instance type storage details.
    """

    id: str
    instance_type: str
    price_per_hour: float
    spot_price_per_hour: float
    description: str
    cpu: dict
    gpu: dict
    memory: dict
    gpu_memory: dict
    storage: dict


class InstanceTypesService:
    """A service for interacting with the instance-types endpoint."""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self) -> list[InstanceType]:
        """Get all instance types.

        :return: list of instance type objects
        :rtype: list[InstanceType]
        """
        instance_types = self._http_client.get(INSTANCE_TYPES_ENDPOINT).json()
        instance_type_objects = [
            InstanceType(
                id=instance_type['id'],
                instance_type=instance_type['instance_type'],
                price_per_hour=float(instance_type['price_per_hour']),
                spot_price_per_hour=float(instance_type['spot_price']),
                description=instance_type['description'],
                cpu=instance_type['cpu'],
                gpu=instance_type['gpu'],
                memory=instance_type['memory'],
                gpu_memory=instance_type['gpu_memory'],
                storage=instance_type['storage'],
            )
            for instance_type in instance_types
        ]

        return instance_type_objects
