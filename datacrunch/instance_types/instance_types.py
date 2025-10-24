from typing import List, Literal

INSTANCE_TYPES_ENDPOINT = '/instance-types'

Currency = Literal['usd', 'eur']

class InstanceType:

    def __init__(self,
                 id: str,
                 instance_type: str,
                 price_per_hour: float,
                 spot_price_per_hour: float,
                 description: str,
                 cpu: dict,
                 gpu: dict,
                 memory: dict,
                 gpu_memory: dict,
                 storage: dict,
                 best_for: List[str],
                 deploy_warning: str | None,
                 model: str,
                 name: str,
                 p2p: str,
                 dynamic_price: float,
                 max_dynamic_price: float,
                 serverless_price: float,
                 serverless_spot_price: float,
                 currency: Currency,
                 manufacturer: str,
                 display_name: str | None) -> None:
        """Initialize an instance type object

        :param id: instance type id
        :type id: str
        :param instance_type: instance type. e.g. '8V100.48M'
        :type instance_type: str
        :param price_per_hour: price per hour
        :type price_per_hour: float
        :param spot_price_per_hour: spot price per hour
        :type spot_price_per_hour: float
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
        :param best_for: use cases for instance type
        :type best_for: list[str]
        :param deploy_warning: deploy warning
        :type deploy_warning: str | None
        :param model: gpu model
        :type model: str
        :param name: gpu model name
        :type name: str
        :param p2p: p2p details
        :type p2p: str
        :param dynamic_price: current dynamic price
        :type dynamic_price: float
        :param max_dynamic_price: ceiling value for dynamic price
        :type max_dynamic_price: float
        :param serverless_price: current serverless price
        :type serverless_price: float
        :param serverless_spot_price: current serverless spot price
        :type serverless_spot_price: float
        :param currency: currency type
        :type currency: str
        :param manufacturer: manufacturer
        :type manufacturer: str
        :param display_name: display name
        :type display_name: str | None
        """
        self._id = id
        self._instance_type = instance_type
        self._price_per_hour = float(price_per_hour)
        self._spot_price_per_hour = float(spot_price_per_hour)
        self._description = description
        self._cpu = cpu
        self._gpu = gpu
        self._memory = memory
        self._gpu_memory = gpu_memory
        self._storage = storage
        self._best_for = best_for
        self._deploy_warning = deploy_warning
        self._model = model
        self._name = name
        self._p2p = p2p
        self._dynamic_price = float(dynamic_price)
        self._max_dynamic_price = float(max_dynamic_price)
        self._serverless_price = float(serverless_price)
        self._serverless_spot_price = float(serverless_spot_price)
        self._currency = currency
        self._manufacturer = manufacturer
        self._display_name = display_name

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
    def spot_price_per_hour(self) -> float:
        """Get the instance spot price per hour

        :return: spot price per hour
        :rtype: float
        """
        return self._spot_price_per_hour

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
    
    @property
    def best_for(self) -> List[str]:
        """Get the instance type use cases

        :return: use cases for the instance type
        :rtype: list[str]
        """
        return self._best_for
    
    @property
    def deploy_warning(self) -> str:
        """Get the instance type deploy warning

        :return: deploy warning
        :rtype: str
        """
        return self._deploy_warning
    
    @property
    def model(self) -> str:
        """Get the instance type gpu model

        :return: gpu model
        :rtype: str
        """
        return self._model
    
    @property
    def name(self) -> str:
        """Get the instance type gpu model name

        :return: gpu model name
        :rtype: str
        """
        return self._name
    
    @property
    def p2p(self) -> str:
        """Get the instance type p2p details

        :return: p2p details
        :rtype: str
        """
        return self._p2p

    @property
    def dynamic_price(self) -> float:
        """Get the instance type's current dynamic price

        :return: current dynamic price
        :rtype: float
        """
        return self._dynamic_price

    @property
    def max_dynamic_price(self) -> float:
        """Get the instance type's ceiling value for dynamic price

        :return: ceiling value for dynamic price
        :rtype: float
        """
        return self._max_dynamic_price

    @property
    def serverless_price(self) -> float:
        """Get the instance type's current serverless price

        :return: current serverless price
        :rtype: float
        """
        return self._serverless_price

    @property
    def serverless_spot_price(self) -> float:
        """Get the instance type's current serverless spot price

        :return: current serverless spot price
        :rtype: float
        """
        return self._serverless_spot_price
    
    @property
    def currency(self) -> str:
        """Get the instance type currency type

        :return: currency type
        :rtype: str
        """
        return self._currency
    
    @property
    def manufacturer(self) -> str:
        """Get the instance type gpu manufacturer

        :return: gpu manufacturer
        :rtype: str
        """
        return self._manufacturer

    @property
    def display_name(self) -> str:
        """Get the instance type display name

        :return: display name
        :rtype: str
        """
        return self._display_name

    def __str__(self) -> str:
        """Prints the instance type

        :return: instance type string representation
        :rtype: str
        """
        return (f'id: {self._id}\n'
                f'instance type: {self._instance_type}\n'
                f'price_per_hour: ${self._price_per_hour}\n'
                f'spot_price_per_hour: ${self._spot_price_per_hour}\n'
                f'description: {self._description}\n'
                f'cpu: {self._cpu}\n'
                f'gpu: {self._gpu}\n'
                f'memory: {self._memory}\n'
                f'gpu_memory: {self._gpu_memory}\n'
                f'storage: {self._storage}\n'
                f'best_for: {self._best_for}\n'
                f'deploy_warning: {self._deploy_warning}\n'
                f'model: {self._model}\n'
                f'name: {self._name}\n'
                f'p2p: {self._p2p}\n'
                f'dynamic_price: {self._dynamic_price}\n'
                f'max_dynamic_price: {self._max_dynamic_price}\n'
                f'serverless_price: {self._serverless_price}\n'
                f'serverless_spot_price: {self._serverless_spot_price}\n'
                f'currency: {self._currency}\n'
                f'manufacturer: {self._manufacturer}\n'
                f'display_name: {self._display_name}\n'
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
            spot_price_per_hour=instance_type['spot_price'],
            description=instance_type['description'],
            cpu=instance_type['cpu'],
            gpu=instance_type['gpu'],
            memory=instance_type['memory'],
            gpu_memory=instance_type['gpu_memory'],
            storage=instance_type['storage'],
            best_for=instance_type['best_for'],
            deploy_warning=instance_type['deploy_warning'],
            model=instance_type['model'],
            name=instance_type['name'],
            p2p=instance_type['p2p'],
            dynamic_price=instance_type['dynamic_price'],
            max_dynamic_price=instance_type['max_dynamic_price'],
            serverless_price=instance_type['serverless_price'],
            serverless_spot_price=instance_type['serverless_spot_price'],
            currency=instance_type['currency'],
            manufacturer=instance_type['manufacturer'],
            display_name=instance_type['display_name']
        ), instance_types))

        return instance_type_objects
