from typing import List

SSHKEYS_ENDPOINT = '/sshkeys'


class SSHKey:
    """An SSH key model class"""

    def __init__(self, id: str, name: str, public_key: str) -> None:
        """Initialize a new SSH key object

        :param id: SSH key id
        :type id: str
        :param name: SSH key name
        :type name: str
        :param public_key: SSH key public key
        :type public_key: str
        """
        self._id = id
        self._name = name
        self._public_key = public_key

    @property
    def id(self) -> str:
        """Get the SSH key id

        :return: SSH key id
        :rtype: str
        """
        return self._id

    @property
    def name(self) -> str:
        """Get the SSH key name

        :return: SSH key name
        :rtype: str
        """
        return self._name

    @property
    def public_key(self) -> str:
        """Get the SSH key public key value

        :return: public SSH key
        :rtype: str
        """
        return self._public_key


class SSHKeysService:
    """A service for interacting with the SSH keys endpoint"""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self) -> List[SSHKey]:
        """Get all of the client's SSH keys

        :return: list of SSH keys objects
        :rtype: List[SSHKey]
        """
        keys = self._http_client.get(SSHKEYS_ENDPOINT).json()
        keys_object_list = list(map(lambda key: SSHKey(
            key['id'], key['name'], key['key']), keys))

        return keys_object_list

    def get_by_id(self, id: str) -> SSHKey:
        """Get a specific SSH key by id.

        :param id: SSH key id
        :type id: str
        :return: SSHKey object
        :rtype: SSHKey
        """
        key_dict = self._http_client.get(SSHKEYS_ENDPOINT + f'/{id}').json()[0]
        key_object = SSHKey(key_dict['id'], key_dict['name'], key_dict['key'])
        return key_object

    def delete(self, id_list: List[str]) -> None:
        """Delete multiple SSH keys by id

        :param id_list: list of SSH keys ids
        :type id_list: List[str]
        """
        payload = {"keys": id_list}
        self._http_client.delete(SSHKEYS_ENDPOINT, json=payload)
        return

    def delete_by_id(self, id: str) -> None:
        """Delete a single SSH key by id

        :param id: SSH key id
        :type id: str
        """
        self._http_client.delete(SSHKEYS_ENDPOINT + f'/{id}')
        return

    def create(self, name: str, key: str) -> SSHKey:
        """Create a new SSH key

        :param name: SSH key name
        :type name: str
        :param key: public SSH key value
        :type key: str
        :return: new SSH key object
        :rtype: SSHKey
        """
        payload = {"name": name, "key": key}
        id = self._http_client.post(SSHKEYS_ENDPOINT, json=payload).text
        return SSHKey(id, name, key)
