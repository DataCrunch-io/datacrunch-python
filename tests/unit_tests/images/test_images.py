import responses # https://github.com/getsentry/responses

from datacrunch.images.images import ImagesService, Image


def test_images(http_client):
    # arrange - add response mock
    responses.add(
        responses.GET,
        http_client._base_url + "/images",
        json=[
            {
                "id": "0888da25-bb0d-41cc-a191-dccae45d96fd",
                "name": "Ubuntu 20.04 + CUDA 11.0",
                "details": [
                    "Ubuntu 20.04",
                    "CUDA 11.0"
                ],
                "image_type": "ubuntu-20.04-cuda-11.0"
            }
        ],
        status=200
    )

    image_service = ImagesService(http_client)

    # act
    images = image_service.get()

    # assert
    assert type(images) == list
    assert len(images) == 1
    assert type(images[0]) == Image
    assert images[0].id == '0888da25-bb0d-41cc-a191-dccae45d96fd'
    assert images[0].name == 'Ubuntu 20.04 + CUDA 11.0'
    assert images[0].image_type == 'ubuntu-20.04-cuda-11.0'
    assert type(images[0].details) == list
    assert images[0].details[0] == "Ubuntu 20.04"
    assert images[0].details[1] == "CUDA 11.0"