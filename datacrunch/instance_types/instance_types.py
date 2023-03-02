from typing import List

INSTANCE_TYPES_ENDPOINT = '/instance-types'


class InstanceType:

    def __init__(self,
                 id: str,
                 instance_type: str,
                 price_per_hour: float,
                 description: str,
                 cpu: dict,
                 gpu: dict,
                 memory: dict,
                 gpu_memory: dict,
                 storage: dict) -> None:
        """Initialize an instance type object

        :param id: instance type id
        :type id: str
        :param instance_type: instance type. e.g. '8V100.48M'
        :type instance_type: str
        :param price_per_hour: price per hour
        :type price_per_hour: float
        :param description: instance type description
        :type description: str
        :param cpu: cpu details
        :type cpu: dict
        :param gpu: gpu details
        :type gpu: dict
        :param memory: memory details
        :type memory: dict
        :param gpu_memory: gpu memory details
        :type gpu_memory: dict
        :param storage: storage details
        :type storage: dict
        """
        self._id = id
        self._instance_type = instance_type
        self._price_per_hour = float(price_per_hour)
        self._description = description
        self._cpu = cpu
        self._gpu = gpu
        self._memory = memory
        self._gpu_memory = gpu_memory
        self._storage = storage

    @property
    def id(self) -> str:
        """Get the instance type id

        :return: instance type id
        :rtype: str
        """
        return self._id

    @property
    def instance_type(self) -> str:
        """Get the instance type

        :return: instance type. e.g. '8V100.48M'
        :rtype: str
        """
        return self._instance_type

    @property
    def price_per_hour(self) -> float:
        """Get the instance type price per hour

        :return: price per hour
        :rtype: float
        """
        return self._price_per_hour

    @property
    def description(self) -> str:
        """Get the instance type description

        :return: instance type description
        :rtype: str
        """
        return self._description

    @property
    def cpu(self) -> dict:
        """Get the instance type cpu details

        :return: cpu details
        :rtype: dict
        """
        return self._cpu

    @property
    def gpu(self) -> dict:
        """Get the instance type gpu details

        :return: gpu details
        :rtype: dict
        """
        return self._gpu

    @property
    def memory(self) -> dict:
        """Get the instance type memory details

        :return: memory details
        :rtype: dict
        """
        return self._memory

    @property
    def gpu_memory(self) -> dict:
        """Get the instance type gpu_memory details

        :return: gpu_memory details
        :rtype: dict
        """
        return self._gpu_memory

    @property
    def storage(self) -> dict:
        """Get the instance type storage details

        :return: storage details
        :rtype: dict
        """
        return self._storage

    def __str__(self) -> str:
        """Prints the instance type

        :return: instance type string representation
        :rtype: str
        """
        return (f'id: {self._id}\n'
                f'instance type: {self._instance_type}\n'
                f'price_per_hour: ${self._price_per_hour}\n'
                f'description: {self._description}\n'
                f'cpu: {self._cpu}\n'
                f'gpu: {self._gpu}\n'
                f'memory :{self._memory}\n'
                f'gpu_memory :{self._gpu_memory}\n'
                f'storage :{self._storage}\n'
                )


class InstanceTypesService:
    """A service for interacting with the instance-types endpoint"""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self) -> List[InstanceType]:
        """Get all instance types

        :return: list of instance type objects
        :rtype: List[InstanceType]
        """
        instance_types = self._http_client.get(INSTANCE_TYPES_ENDPOINT).json()
        instance_type_objects = list(map(lambda instance_type: InstanceType(
            id=instance_type['id'],
            instance_type=instance_type['instance_type'],
            price_per_hour=instance_type['price_per_hour'],
            description=instance_type['description'],
            cpu=instance_type['cpu'],
            gpu=instance_type['gpu'],
            memory=instance_type['memory'],
            gpu_memory=instance_type['gpu_memory'],
            storage=instance_type['storage']
        ), instance_types))

        return instance_type_objects
