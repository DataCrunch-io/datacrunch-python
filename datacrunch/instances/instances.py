from typing import List, Union, Optional, Dict
from datacrunch.helpers import stringify_class_object_properties

INSTANCES_ENDPOINT = '/instances'


class Instance:
    """An instance model class"""

    def __init__(self,
                 id: str,
                 instance_type: str,
                 image: str,
                 price_per_hour: float,
                 hostname: str,
                 description: str,
                 ip: str,
                 status: str,
                 created_at: str,
                 ssh_key_ids: List[str],
                 cpu: dict,
                 gpu: dict,
                 memory: dict,
                 storage: dict,
                 os_volume_id: str,
                 gpu_memory: dict,
                 location: str = "FIN1",
                 startup_script_id: str = None,
                 is_spot: bool = False
                 ) -> None:
        """Initialize the instance object

        :param id: instance id
        :type id: str
        :param instance_type: instance type. e.g. '8V100.48M'
        :type instance_type: str
        :param image: instance image type. e.g. 'ubuntu-20.04-cuda-11.0'
        :type image: str
        :param price_per_hour: price per hour
        :type price_per_hour: float
        :param hostname: instance hostname
        :type hostname: str
        :param description: instance description
        :type description: str
        :param ip: instance ip address
        :type ip: str
        :param status: instance current status, might be out of date if changed
        :type status: str
        :param created_at: the time the instance was deployed (UTC)
        :type created_at: str
        :param ssh_key_ids: list of ssh keys ids
        :type ssh_key_ids: List[str]
        :param cpu: cpu details
        :type cpu: dict
        :param gpu: gpu details
        :type gpu: dict
        :param memory: memory details
        :type memory: dict
        :param storage: storate details
        :type storage: dict
        :param id: main OS volume id
        :type id: str
        :param memory: gpu memory details
        :type memory: dict
        :param location: datacenter location, defaults to "FIN1"
        :type location: str, optional
        :param startup_script_id: startup script id, defaults to None
        :type startup_script_id: str, optional
        :param is_spot: is this a spot instance, defaults to None
        :type is_spot: bool, optional
        """
        self._id = id
        self._instance_type = instance_type
        self._image = image
        self._price_per_hour = price_per_hour
        self._location = location
        self._hostname = hostname
        self._description = description
        self._ip = ip
        self._status = status
        self._created_at = created_at
        self._ssh_key_ids = ssh_key_ids
        self._startup_script_id = startup_script_id
        self._cpu = cpu
        self._gpu = gpu
        self._memory = memory
        self._storage = storage
        self._os_volume_id = os_volume_id
        self._gpu_memory = gpu_memory
        self._is_spot = is_spot

    @property
    def id(self) -> str:
        """Get the instance id

        :return: instance id
        :rtype: str
        """
        return self._id

    @property
    def instance_type(self) -> str:
        """Get the instance type

        :return: instance type
        :rtype: str
        """
        return self._instance_type

    @property
    def image(self) -> str:
        """Get the instance image type

        :return: instance image type
        :rtype: str
        """
        return self._image

    @property
    def price_per_hour(self) -> float:
        """Get the instance price per hour

        :return: price per hour
        :rtype: float
        """
        return self._price_per_hour

    @property
    def location(self) -> str:
        """Get the instance datacenter location

        :return: datacenter location
        :rtype: str
        """
        return self._location

    @property
    def hostname(self) -> str:
        """Get the instance hostname

        :return: hostname
        :rtype: str
        """
        return self._hostname

    @property
    def description(self) -> str:
        """Get the instance description

        :return: instance description
        :rtype: str
        """
        return self._description

    @property
    def ip(self) -> str:
        """Get the instance ip address

        :return: ip address
        :rtype: str
        """
        return self._ip

    @property
    def status(self) -> str:
        """Get the current instance status. might be out of date if changed.

        :return: instance status
        :rtype: str
        """
        return self._status

    @property
    def created_at(self) -> str:
        """Get the time when the instance was deployed (UTC)

        :return: time
        :rtype: str
        """
        return self._created_at

    @property
    def ssh_key_ids(self) -> List[str]:
        """Get the SSH key IDs of the instance

        :return: SSH key IDs
        :rtype: List[str]
        """
        return self._ssh_key_ids

    @property
    def startup_script_id(self) -> Union[str, None]:
        """Get the startup script ID or None if the is no script

        :return: startup script ID or None
        :rtype: Union[str, None]
        """
        return self._startup_script_id

    @property
    def cpu(self) -> dict:
        """Get the instance cpu details

        :return: cpu details
        :rtype: dict
        """
        return self._cpu

    @property
    def gpu(self) -> dict:
        """Get the instance gpu details

        :return: gpu details
        :rtype: dict
        """
        return self._gpu

    @property
    def memory(self) -> dict:
        """Get the instance memory details

        :return: memory details
        :rtype: dict
        """
        return self._memory

    @property
    def storage(self) -> dict:
        """Get the instance storage details

        :return: storage details
        :rtype: dict
        """
        return self._storage

    @property
    def os_volume_id(self) -> str:
        """Get the main os volume id

        :return: main os volume id
        :rtype: str
        """
        return self._os_volume_id

    @property
    def gpu_memory(self) -> dict:
        """Get the instance gpu_memory details

        :return: gpu_memory details
        :rtype: dict
        """
        return self._gpu_memory

    @property
    def is_spot(self) -> bool:
        """Is this a spot instance

        :return: is spot details
        :rtype: bool
        """
        return self._is_spot

    def __str__(self) -> str:
        """Returns a string of the json representation of the instance

        :return: json representation of the instance
        :rtype: str
        """
        return stringify_class_object_properties(self)

class InstancesService:
    """A service for interacting with the instances endpoint"""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self, status: str = None) -> List[Instance]:
        """Get all of the client's non-deleted instances, or instances with specific status.

        :param status: optional, status of the instances, defaults to None
        :type status: str, optional
        :return: list of instance details objects
        :rtype: List[Instance]
        """
        instances_dict = self._http_client.get(
            INSTANCES_ENDPOINT, params={'status': status}).json()
        instances = list(map(lambda instance_dict: Instance(
            id=instance_dict['id'],
            instance_type=instance_dict['instance_type'],
            image=instance_dict['image'],
            price_per_hour=instance_dict['price_per_hour'] if 'price_per_hour' in instance_dict else None,
            location=instance_dict['location'],
            hostname=instance_dict['hostname'],
            description=instance_dict['description'],
            ip=instance_dict['ip'],
            status=instance_dict['status'],
            created_at=instance_dict['created_at'],
            ssh_key_ids=instance_dict['ssh_key_ids'] if 'ssh_key_ids' in instance_dict else [],
            startup_script_id=instance_dict['startup_script_id'] if 'startup_script_id' in instance_dict else None,
            cpu=instance_dict['cpu'],
            gpu=instance_dict['gpu'],
            memory=instance_dict['memory'],
            storage=instance_dict['storage'],
            os_volume_id=instance_dict['os_volume_id'] if 'os_volume_id' in instance_dict else None,
            gpu_memory=instance_dict['gpu_memory'] if 'gpu_memory' in instance_dict else None,
            is_spot=instance_dict['is_spot'] if 'is_spot' in instance_dict else False
        ), instances_dict))
        return instances

    def get_by_id(self, id: str) -> Instance:
        """Get an instance with specified id.

        :param id: instance id
        :type id: str
        :return: instance details object
        :rtype: Instance
        """
        instance_dict = self._http_client.get(
            INSTANCES_ENDPOINT + f'/{id}').json()
        instance = Instance(
            id=instance_dict['id'],
            instance_type=instance_dict['instance_type'],
            image=instance_dict['image'],
            price_per_hour=instance_dict['price_per_hour'] if 'price_per_hour' in instance_dict else None,
            location=instance_dict['location'],
            hostname=instance_dict['hostname'],
            description=instance_dict['description'],
            ip=instance_dict['ip'],
            status=instance_dict['status'],
            created_at=instance_dict['created_at'],
            ssh_key_ids=instance_dict['ssh_key_ids'] if 'ssh_key_ids' in instance_dict else [],
            startup_script_id=instance_dict['startup_script_id'] if 'startup_script_id' in instance_dict else None,
            cpu=instance_dict['cpu'],
            gpu=instance_dict['gpu'],
            memory=instance_dict['memory'],
            storage=instance_dict['storage'],
            os_volume_id=instance_dict['os_volume_id'] if 'os_volume_id' in instance_dict else None,
            gpu_memory=instance_dict['gpu_memory'] if 'gpu_memory' in instance_dict else None,
            is_spot=instance_dict['is_spot'] if 'is_spot' in instance_dict else False
        )
        return instance

    def create(self,
               instance_type: str,
               image: str,
               hostname: str,
               description: str,
               ssh_key_ids: list = [],
               location: str = "FIN1",
               startup_script_id: str = None,
               volumes: List[Dict] = None,
               os_volume: Dict = None,
               is_spot: bool = False,
               coupon: str = None) -> Instance:
        """Creates (deploys) a new instance

        :param instance_type: instance type. e.g. '8V100.48M'
        :type instance_type: str
        :param image: instance image type. e.g. 'ubuntu-20.04-cuda-11.0', or existing OS volume id
        :type image: str
        :param ssh_key_ids: list of ssh key ids
        :type ssh_key_ids: list
        :param hostname: instance hostname
        :type hostname: str
        :param description: instance description
        :type description: str
        :param location: datacenter location, defaults to "FIN1"
        :type location: str, optional
        :param startup_script_id: startup script id, defaults to None
        :type startup_script_id: str, optional
        :param volumes: List of volume data dictionaries to create alongside the instance
        :type volumes: List[Dict], optional
        :param os_volume: OS volume details, defaults to None
        :type os_volume: Dict, optional
        :param is_spot: Is spot instance
        :type is_spot: bool, optional
        :param coupon: coupon code
        :type coupon: str, optional
        :return: the new instance object
        :rtype: id
        """
        payload = {
            "instance_type": instance_type,
            "image": image,
            "ssh_key_ids": ssh_key_ids,
            "startup_script_id": startup_script_id,
            "hostname": hostname,
            "description": description,
            "location": location,
            "os_volume": os_volume,
            "volumes": volumes,
            "is_spot": is_spot,
            "coupon": coupon
        }
        id = self._http_client.post(INSTANCES_ENDPOINT, json=payload).text
        instance = self.get_by_id(id)
        return instance

    def action(self, id_list: Union[List[str], str], action: str, volume_ids: Optional[List[str]] = None) -> None:
        """Performs an action on a list of instances / single instance

        :param id_list: list of instance ids, or an instance id
        :type id_list: Union[List[str], str]
        :param action: the action to perform
        :type action: str
        :param volume_ids: the volume ids to delete
        :type volume_ids: Optional[List[str]]
        """
        if type(id_list) is str:
            id_list = [id_list]

        payload = {
            "id": id_list,
            "action": action,
            "volume_ids": volume_ids
        }

        self._http_client.put(INSTANCES_ENDPOINT, json=payload)
        return

    def is_available(self, instance_type: str, is_spot: bool = None) -> bool:
        """Returns True if a specific instance type is now available for deployment

        :param instance_type: instance type
        :type instance_type: str
        :param is_spot: Is spot instance
        :type is_spot: bool, optional
        :return: True if available to deploy, False otherwise
        :rtype: bool
        """
        query_param = '?isSpot=true' if is_spot else ''
        url = f'/instance-availability/{instance_type}{query_param}'
        return self._http_client.get(url).json()
