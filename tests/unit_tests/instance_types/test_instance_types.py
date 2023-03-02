import responses  # https://github.com/getsentry/responses

from datacrunch.instance_types.instance_types import InstanceTypesService, InstanceType

TYPE_ID = "01cf5dc1-a5d2-4972-ae4e-d429115d055b"
CPU_DESCRIPTION = "48 CPU 3.5GHz"
NUMBER_OF_CORES = 48
GPU_DESCRIPTION = "8x NVidia Tesla V100"
NUMBER_OF_GPUS = 8
MEMORY_DESCRIPTION = "192GB RAM"
MEMORY_SIZE = 192
GPU_MEMORY_DESCRIPTION = "128GB VRAM"
GPU_MEMORY_SIZE = 128
STORAGE_DESCRIPTION = "1800GB NVME"
STORAGE_SIZE = 1800
INSTANCE_TYPE_DESCRIPTION = "Dedicated Bare metal Server"
PRICE_PER_HOUR = 5.0
INSTANCE_TYPE = "8V100.48M"


def test_instance_types(http_client):
    # arrange - add response mock
    responses.add(
        responses.GET,
        http_client._base_url + "/instance-types",
        json=[
            {
                "id": TYPE_ID,
                "cpu": {
                    "description": CPU_DESCRIPTION,
                    "number_of_cores": NUMBER_OF_CORES
                },
                "gpu": {
                    "description": GPU_DESCRIPTION,
                    "number_of_gpus": NUMBER_OF_GPUS
                },
                "memory": {
                    "description": MEMORY_DESCRIPTION,
                    "size_in_gigabytes": MEMORY_SIZE
                },
                "gpu_memory": {
                    "description": GPU_MEMORY_DESCRIPTION,
                    "size_in_gigabytes": GPU_MEMORY_SIZE
                },
                "storage": {
                    "description": STORAGE_DESCRIPTION,
                    "size_in_gigabytes": STORAGE_SIZE
                },
                "description": INSTANCE_TYPE_DESCRIPTION,
                "price_per_hour": "5.00",
                "instance_type": INSTANCE_TYPE
            }
        ],
        status=200
    )

    instance_types_service = InstanceTypesService(http_client)

    # act
    instance_types = instance_types_service.get()
    instance_type = instance_types[0]

    # assert
    assert type(instance_types) == list
    assert len(instance_types) == 1
    assert type(instance_type) == InstanceType
    assert instance_type.id == TYPE_ID
    assert instance_type.description == INSTANCE_TYPE_DESCRIPTION
    assert instance_type.price_per_hour == PRICE_PER_HOUR
    assert instance_type.instance_type == INSTANCE_TYPE
    assert type(instance_type.cpu) == dict
    assert type(instance_type.gpu) == dict
    assert type(instance_type.memory) == dict
    assert type(instance_type.storage) == dict
    assert instance_type.cpu['description'] == CPU_DESCRIPTION
    assert instance_type.gpu['description'] == GPU_DESCRIPTION
    assert instance_type.memory['description'] == MEMORY_DESCRIPTION
    assert instance_type.gpu_memory['description'] == GPU_MEMORY_DESCRIPTION
    assert instance_type.storage['description'] == STORAGE_DESCRIPTION
    assert instance_type.cpu['number_of_cores'] == NUMBER_OF_CORES
    assert instance_type.gpu['number_of_gpus'] == NUMBER_OF_GPUS
    assert instance_type.memory['size_in_gigabytes'] == MEMORY_SIZE
    assert instance_type.gpu_memory['size_in_gigabytes'] == GPU_MEMORY_SIZE
    assert instance_type.storage['size_in_gigabytes'] == STORAGE_SIZE
