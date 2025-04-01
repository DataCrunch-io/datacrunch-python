from typing import List, Union, Optional, Dict, Literal
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datacrunch.helpers import stringify_class_object_properties
from datacrunch.constants import Locations

INSTANCES_ENDPOINT = '/instances'

Contract = Literal['LONG_TERM', 'PAY_AS_YOU_GO', 'SPOT']
Pricing = Literal['DYNAMIC_PRICE', 'FIXED_PRICE']


@dataclass_json
@dataclass
class Instance:
    """An instance model class"""

    id: str
    instance_type: str
    price_per_hour: float
    hostname: str
    description: str
    ip: str
    status: str
    created_at: str
    ssh_key_ids: List[str]
    cpu: dict
    gpu: dict
    memory: dict
    storage: dict
    os_volume_id: str
    gpu_memory: dict
    location: str = Locations.FIN_01
    image: Optional[str] = None
    startup_script_id: Optional[str] = None
    is_spot: bool = False
    contract: Optional[Contract] = None
    pricing: Optional[Pricing] = None

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
        return [Instance.from_dict(instance_dict, infer_missing=True) for instance_dict in instances_dict]

    def get_by_id(self, id: str) -> Instance:
        """Get an instance with specified id.

        :param id: instance id
        :type id: str
        :return: instance details object
        :rtype: Instance
        """
        instance_dict = self._http_client.get(
            INSTANCES_ENDPOINT + f'/{id}').json()
        return Instance.from_dict(instance_dict, infer_missing=True)

    def create(self,
               instance_type: str,
               image: str,
               hostname: str,
               description: str,
               ssh_key_ids: list = [],
               location: str = Locations.FIN_01,
               startup_script_id: str = None,
               volumes: List[Dict] = None,
               existing_volumes: List[str] = None,
               os_volume: Dict = None,
               is_spot: bool = False,
               contract: Contract = None,
               pricing: Pricing = None,
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
        :param location: datacenter location, defaults to "FIN-01"
        :type location: str, optional
        :param startup_script_id: startup script id, defaults to None
        :type startup_script_id: str, optional
        :param volumes: List of volume data dictionaries to create alongside the instance
        :type volumes: List[Dict], optional
        :param existing_volumes: List of existing volume ids to attach to the instance
        :type existing_volumes: List[str], optional
        :param os_volume: OS volume details, defaults to None
        :type os_volume: Dict, optional
        :param is_spot: Is spot instance
        :type is_spot: bool, optional
        :param pricing: Pricing type
        :type pricing: str, optional
        :param contract: Contract type
        :type contract: str, optional
        :param coupon: coupon code
        :type coupon: str, optional
        :return: the new instance object
        :rtype: Instance
        """
        payload = {
            "instance_type": instance_type,
            "image": image,
            "ssh_key_ids": ssh_key_ids,
            "startup_script_id": startup_script_id,
            "hostname": hostname,
            "description": description,
            "location_code": location,
            "os_volume": os_volume,
            "volumes": volumes,
            "existing_volumes": existing_volumes,
            "is_spot": is_spot,
            "coupon": coupon,
        }
        if contract:
            payload['contract'] = contract
        if pricing:
            payload['pricing'] = pricing
        id = self._http_client.post(INSTANCES_ENDPOINT, json=payload).text
        return self.get_by_id(id)

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

    # TODO: use enum/const for location_code
    def is_available(self, instance_type: str, is_spot: bool = False, location_code: str = None) -> bool:
        """Returns True if a specific instance type is now available for deployment

        :param instance_type: instance type
        :type instance_type: str
        :param is_spot: Is spot instance
        :type is_spot: bool, optional
        :param location_code: datacenter location, defaults to "FIN-01"
        :type location_code: str, optional
        :return: True if available to deploy, False otherwise
        :rtype: bool
        """
        is_spot = str(is_spot).lower()
        query_params = {'isSpot': is_spot, 'location_code': location_code}
        url = f'/instance-availability/{instance_type}'
        return self._http_client.get(url, query_params).json()

    # TODO: use enum/const for location_code
    def get_availabilities(self, is_spot: bool = None, location_code: str = None) -> bool:
        """Returns a list of available instance types

        :param is_spot: Is spot instance
        :type is_spot: bool, optional
        :param location_code: datacenter location, defaults to "FIN-01"
        :type location_code: str, optional
        :return: list of available instance types in every location
        :rtype: list
        """
        is_spot = str(is_spot).lower() if is_spot is not None else None
        query_params = {'isSpot': is_spot, 'locationCode': location_code}
        return self._http_client.get('/instance-availability', params=query_params).json()
