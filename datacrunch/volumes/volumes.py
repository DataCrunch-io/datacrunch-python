
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
                 target: str,
                 location: str = "FIN1",
                 instance_id: str = None,
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
        :type target: str
        :param location: datacenter location, defaults to "FIN1"
        :type location: str, optional
        :param instance_id: the instance id the volume is attached to, None if detached
        :type instance_id: str
        """

        self.id = id
        self.status = status
        self.name = name
        self.size = size
        self.type = type
        self.is_os_volume = is_os_volume
        self.created_at = created_at
        self.target = target
        self.location = location
        self.instance_id = instance_id
