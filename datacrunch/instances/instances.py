from typing import List, Union

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
                 location: str = "FIN1",
                 startup_script_id: str = None
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
        :param status: instance current status, might be out of date if changed.
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
        :param location: datacenter location, defaults to "FIN1"
        :type location: str, optional
        :param startup_script_id: startup script id, defaults to None
        :type startup_script_id: str, optional
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
            price_per_hour=instance_dict['price_per_hour'],
            location=instance_dict['location'],
            hostname=instance_dict['hostname'],
            description=instance_dict['description'],
            ip=instance_dict['ip'],
            status=instance_dict['status'],
            created_at=instance_dict['created_at'],
            ssh_key_ids=instance_dict['ssh_key_ids'],
            startup_script_id=instance_dict['startup_script_id'] if 'startup_script_id' in instance_dict else None,
            cpu=instance_dict['cpu'],
            gpu=instance_dict['gpu'],
            memory=instance_dict['memory'],
            storage=instance_dict['storage']
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
            price_per_hour=instance_dict['price_per_hour'],
            location=instance_dict['location'],
            hostname=instance_dict['hostname'],
            description=instance_dict['description'],
            ip=instance_dict['ip'],
            status=instance_dict['status'],
            created_at=instance_dict['created_at'],
            ssh_key_ids=instance_dict['ssh_key_ids'],
            startup_script_id=instance_dict['startup_script_id'] if 'startup_script_id' in instance_dict else None,
            cpu=instance_dict['cpu'],
            gpu=instance_dict['gpu'],
            memory=instance_dict['memory'],
            storage=instance_dict['storage']
        )
        return instance

    def create(self,
               instance_type: str,
               image: str,
               ssh_key_ids: list,
               hostname: str,
               description: str,
               location: str = "FIN1",
               startup_script_id: str = None) -> Instance:
        """Creates (deploys) a new instance

        :param instance_type: instance type. e.g. '8V100.48M'
        :type instance_type: str
        :param image: instance image type. e.g. 'ubuntu-20.04-cuda-11.0'
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
            "location": location
        }
        id = self._http_client.post(INSTANCES_ENDPOINT, json=payload).text
        instance = self.get_by_id(id)
        return instance

    def action(self, id_list: Union[List[str], str], action: str) -> None:
        """Performs an action on a list of instances / single instance

        :param id_list: list of instance ids, or an instance id
        :type id_list: Union[List[str], str]
        :param action: the action to perform
        :type action: str
        """
        if type(id_list) is str:
            id_list = [id_list]

        payload = {
            "id": id_list,
            "action": action
        }

        self._http_client.post(INSTANCES_ENDPOINT + '/action', json=payload)
        return

    def is_available(self, instance_type: str) -> bool:
        """Returns True if a specific instance type is now available for deployment

        :param instance_type: instance type
        :type instance_type: str
        :return: True if available to deploy, False otherwise
        :rtype: bool
        """
        return self._http_client.get(INSTANCES_ENDPOINT + f'/availability/{instance_type}').json()
