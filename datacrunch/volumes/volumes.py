from typing import List, Union, Optional
from datacrunch.constants import VolumeActions
from datacrunch.helpers import stringify_class_object_properties

VOLUMES_ENDPOINT = '/volumes'


class Volume:
    """A volume model class"""

    def __init__(self,
                 id: str,
                 status: str,
                 name: str,
                 size: int,
                 type: str,
                 is_os_volume: bool,
                 created_at: str,
                 target: str = None,
                 location: str = "FIN1",
                 instance_id: str = None,
                 ssh_key_ids: List[str] = [],
                 ) -> None:
        """Initialize the volume object

        :param id: volume id
        :type id: str
        :param status: volume status
        :type status: str
        :param name: volume name
        :type name: str
        :param size: volume size in GB
        :type size: int
        :param type: volume type
        :type type: str
        :param is_os_volume: indication whether this is an operating systen volume
        :type is_os_volume: bool
        :param created_at: the time the volume was created (UTC)
        :type created_at: str
        :param target: target device e.g. vda
        :type target: str, optional
        :param location: datacenter location, defaults to "FIN1"
        :type location: str, optional
        :param instance_id: the instance id the volume is attached to, None if detached
        :type instance_id: str
        :param ssh_key_ids: list of ssh keys ids
        :type ssh_key_ids: List[str]
        """

        self._id = id
        self._status = status
        self._name = name
        self._size = size
        self._type = type
        self._is_os_volume = is_os_volume
        self._created_at = created_at
        self._target = target
        self._location = location
        self._instance_id = instance_id
        self._ssh_key_ids = ssh_key_ids

    @property
    def id(self) -> str:
        """Get the volume id

        :return: volume id
        :rtype: str
        """
        return self._id

    @property
    def status(self) -> str:
        """Get the volume status

        :return: volume status
        :rtype: str
        """
        return self._status

    @property
    def name(self) -> str:
        """Get the volume name

        :return: volume name
        :rtype: str
        """
        return self._name

    @property
    def size(self) -> int:
        """Get the volume size

        :return: volume size
        :rtype: int
        """
        return self._size

    @property
    def type(self) -> int:
        """Get the volume type

        :return: volume type
        :rtype: string
        """
        return self._type

    @property
    def is_os_volume(self) -> bool:
        """Return true iff the volume contains an operating system

        :return: true iff the volume contains an OS
        :rtype: bool
        """
        return self._is_os_volume

    @property
    def created_at(self) -> str:
        """Get the time when the volume was created (UTC)

        :return: time
        :rtype: str
        """
        return self._created_at

    @property
    def target(self) -> Optional[str]:
        """Get the target device

        :return: target device
        :rtype: str, optional
        """
        return self._target

    @property
    def location(self) -> str:
        """Get the volume datacenter location

        :return: datacenter location
        :rtype: str
        """
        return self._location

    @property
    def instance_id(self) -> Optional[str]:
        """Get the instance id the volume is attached to, if attached. Otherwise None

        :return: instance id if attached, None otherwise
        :rtype: str, optional
        """
        return self._instance_id

    @property
    def ssh_key_ids(self) -> List[str]:
        """Get the SSH key IDs of the instance

        :return: SSH key IDs
        :rtype: List[str]
        """
        return self._ssh_key_ids

    def __str__(self) -> str:
        """Returns a string of the json representation of the volume

        :return: json representation of the volume
        :rtype: str
        """
        return stringify_class_object_properties(self)

class VolumesService:
    """A service for interacting with the volumes endpoint"""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self, status: str = None) -> List[Volume]:
        """Get all of the client's non-deleted volumes, or volumes with specific status.

        :param status: optional, status of the volumes, defaults to None
        :type status: str, optional
        :return: list of volume details objects
        :rtype: List[Volume]
        """
        volumes_dict = self._http_client.get(
            VOLUMES_ENDPOINT, params={'status': status}).json()
        volumes = list(map(lambda volume_dict: Volume(
            id=volume_dict['id'],
            status=volume_dict['status'],
            name=volume_dict['name'],
            size=volume_dict['size'],
            type=volume_dict['type'],
            is_os_volume=volume_dict['is_os_volume'],
            created_at=volume_dict['created_at'],
            target=volume_dict['target'] if 'target' in volume_dict else None,
            location=volume_dict['location'],
            instance_id=volume_dict['instance_id'] if 'instance_id' in volume_dict else None,
            ssh_key_ids=volume_dict['ssh_key_ids'] if 'ssh_key_ids' in volume_dict else [],
        ), volumes_dict))
        return volumes

    def get_by_id(self, id: str) -> Volume:
        """Get a specific volume by its

        :param id: volume id
        :type id: str
        :return: Volume details object
        :rtype: Volume
        """
        volume_dict = self._http_client.get(
            VOLUMES_ENDPOINT + f'/{id}').json()
        volume = Volume(
            id=volume_dict['id'],
            status=volume_dict['status'],
            name=volume_dict['name'],
            size=volume_dict['size'],
            type=volume_dict['type'],
            is_os_volume=volume_dict['is_os_volume'],
            created_at=volume_dict['created_at'],
            target=volume_dict['target'] if 'target' in volume_dict else None,
            location=volume_dict['location'],
            instance_id=volume_dict['instance_id'] if 'instance_id' in volume_dict else None,
            ssh_key_ids=volume_dict['ssh_key_ids'] if 'ssh_key_ids' in volume_dict else [],
        )
        return volume

    def create(self,
               type: str,
               name: str,
               size: int,
               instance_id: str = None,
               location: str = "FIN1",
               ) -> Volume:
        """Create new volume

        :param type: volume type
        :type type: str
        :param name: volume name
        :type name: str
        :param size: volume size, in GB
        :type size: int
        :param instance_id: Instance id to be attached to, defaults to None
        :type instance_id: str, optional
        :param location: datacenter location, defaults to "FIN1"
        :type location: str, optional
        :return: the new volume object
        :rtype: Volume
        """
        payload = {
            "type": type,
            "name": name,
            "size": size,
            "instance_id": instance_id,
            "location": location
        }
        id = self._http_client.post(VOLUMES_ENDPOINT, json=payload).text
        volume = self.get_by_id(id)
        return volume

    def attach(self, id_list: Union[List[str], str], instance_id: str) -> None:
        """Attach multiple volumes or single volume to an instance
        Note: the instance needs to be shut-down (offline)

        :param id_list: list of volume ids, or a volume id
        :type id_list: Union[List[str], str]
        :param instance_id: instance id the volume(s) will be attached to
        :type instance_id: str
        """
        payload = {
            "id": id_list,
            "action": VolumeActions.ATTACH,
            "instance_id": instance_id
        }

        self._http_client.put(VOLUMES_ENDPOINT, json=payload)
        return

    def detach(self, id_list: Union[List[str], str]) -> None:
        """Detach multiple volumes or single volume from an instance(s)
        Note: the instances need to be shut-down (offline)

        :param id_list: list of volume ids, or a volume id
        :type id_list: Union[List[str], str]
        """
        payload = {
            "id": id_list,
            "action": VolumeActions.DETACH,
        }

        self._http_client.put(VOLUMES_ENDPOINT, json=payload)
        return

    def rename(self, id_list: Union[List[str], str], name: str) -> None:
        """Rename multiple volumes or single volume

        :param id_list: list of volume ids, or a volume id
        :type id_list: Union[List[str], str]
        :param name: new name
        :type name: str
        """
        payload = {
            "id": id_list,
            "action": VolumeActions.RENAME,
            "name": name
        }

        self._http_client.put(VOLUMES_ENDPOINT, json=payload)
        return

    def increase_size(self, id_list: Union[List[str], str], size: int) -> None:
        """Increase size of multiple volumes or single volume

        :param id_list: list of volume ids, or a volume id
        :type id_list: Union[List[str], str]
        :param size: new size in GB
        :type size: int
        """
        payload = {
            "id": id_list,
            "action": VolumeActions.INCREASE_SIZE,
            "size": size,
        }

        self._http_client.put(VOLUMES_ENDPOINT, json=payload)
        return

    def delete(self, id_list: Union[List[str], str]) -> None:
        """Delete multiple volumes or single volume
        Note: if attached to any instances, they need to be shut-down (offline)

        :param id_list: list of volume ids, or a volume id
        :type id_list: Union[List[str], str]
        """
        payload = {
            "id": id_list,
            "action": VolumeActions.DELETE,
        }

        self._http_client.put(VOLUMES_ENDPOINT, json=payload)
        return
