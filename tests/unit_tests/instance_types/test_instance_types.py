import responses # https://github.com/getsentry/responses

from datacrunch.instance_types.instance_types import InstanceTypesService, InstanceType


def test_instance_types(http_client):
    # arrange - add response mock
    responses.add(
        responses.GET,
        http_client._base_url + "/instance-types",
        json=[
            {
                "id": "01cf5dc1-a5d2-4972-ae4e-d429115d055b",
                "cpu": {
                    "description": "48 CPU 3.5GHz",
                    "number_of_cores": 48
                },
                "gpu": {
                    "description": "8x NVidia Tesla V100",
                    "number_of_gpus": 8
                },
                "memory": {
                    "description": "192GB RAM",
                    "size_in_gigabytes": 192
                },
                "storage": {
                    "description": "1800GB NVME",
                    "size_in_gigabytes": 1800
                },
                "description": "Dedicated Bare metal Server",
                "pricePerHour": "5.00",
                "instance_type": "8V100.48M"
            }
        ],
        status=200
    )

    instance_types_service = InstanceTypesService(http_client)

    # act
    instance_types = instance_types_service.get()

    # assert
    assert type(instance_types) == list
    assert len(instance_types) == 1
    assert type(instance_types[0]) == InstanceType
    assert instance_types[0].id == '01cf5dc1-a5d2-4972-ae4e-d429115d055b'
    assert instance_types[0].description == "Dedicated Bare metal Server"
    assert instance_types[0].price_per_hour == 5.0
    assert instance_types[0].instance_type == "8V100.48M"
    assert type(instance_types[0].cpu) == dict
    assert type(instance_types[0].gpu) == dict
    assert type(instance_types[0].memory) == dict
    assert type(instance_types[0].storage) == dict
    assert instance_types[0].cpu['description'] == "48 CPU 3.5GHz"
    assert instance_types[0].gpu['description'] == "8x NVidia Tesla V100"
    assert instance_types[0].memory['description'] == "192GB RAM"
    assert instance_types[0].storage['description'] == "1800GB NVME"
    assert instance_types[0].cpu['number_of_cores'] == 48
    assert instance_types[0].gpu['number_of_gpus'] == 8
    assert instance_types[0].memory['size_in_gigabytes'] == 192
    assert instance_types[0].storage['size_in_gigabytes'] == 1800