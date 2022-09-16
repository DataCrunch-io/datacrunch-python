from typing import List
from datacrunch.helpers import stringify_class_object_properties

IMAGES_ENDPOINT = '/images'


class Image:
    """An image model class"""

    def __init__(self, id: str, name: str, image_type: str, details: List[str]) -> None:
        """Initialize an image object

        :param id: image id
        :type id: str
        :param name: image name
        :type name: str
        :param image_type: image type, e.g. 'ubuntu-20.04-cuda-11.0'
        :type image_type: str
        :param details: image details
        :type details: List[str]
        """
        self._id = id
        self._name = name
        self._image_type = image_type
        self._details = details

    @property
    def id(self) -> str:
        """Get the image id

        :return: image id
        :rtype: str
        """
        return self._id

    @property
    def name(self) -> str:
        """Get the image name

        :return: image name
        :rtype: str
        """
        return self._name

    @property
    def image_type(self) -> str:
        """Get the image type

        :return: image type
        :rtype: str
        """
        return self._image_type

    @property
    def details(self) -> List[str]:
        """Get the image details

        :return: image details
        :rtype: List[str]
        """
        return self._details

    def __str__(self) -> str:
        """Returns a string of the json representation of the image

        :return: json representation of the image
        :rtype: str
        """
        return stringify_class_object_properties(self)


class ImagesService:
    """A service for interacting with the images endpoint"""

    def __init__(self, http_client) -> None:
        self._http_client = http_client

    def get(self) -> List[Image]:
        """Get the available instance images 

        :return: list of images objects
        :rtype: List[Image]
        """
        images = self._http_client.get(IMAGES_ENDPOINT).json()
        image_objects = list(map(lambda image: Image(
            image['id'], image['name'], image['image_type'], image['details']), images))
        return image_objects
