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
SPOT_PRICE_PER_HOUR = 2.5
INSTANCE_TYPE = "8V100.48M"
SMALL_ML_MODELS = 'Small ML models'
MULTI_GPU_TRAINING = 'Multi-GPU training'
FP64_CALCULATIONS = 'FP64 calculations'
NVLINK = 'NVLINK'
DEPLOY_WARNING = 'This is a test'
MODEL = 'Tesla V100'
NAME = 'Tesla V100 16GB'
P2P = 'NVLink up to 50GB/s'
DYNAMIC_PRICE = 0.78
MAX_DYNAMIC_PRICE = 1.66
SERVERLESS_PRICE = 0.0
SERVERLESS_SPOT_PRICE = 0.0
CURRENCY = 'usd'
MANUFACTURER = 'NVIDIA'
DISPLAY_NAME = '8x Tesla V100'


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
                "spot_price": "2.50",
                "instance_type": INSTANCE_TYPE,
                "best_for": [
                    SMALL_ML_MODELS,
                    MULTI_GPU_TRAINING,
                    FP64_CALCULATIONS,
                    NVLINK
                ],
                "deploy_warning": DEPLOY_WARNING,
                "model": MODEL,
                "name": NAME,
                "p2p": P2P,
                "dynamic_price": DYNAMIC_PRICE,
                "max_dynamic_price": MAX_DYNAMIC_PRICE,
                "serverless_price": SERVERLESS_PRICE,
                "serverless_spot_price": SERVERLESS_SPOT_PRICE,
                "currency": CURRENCY,
                "manufacturer": MANUFACTURER,
                "display_name": DISPLAY_NAME
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
    assert instance_type.spot_price_per_hour == SPOT_PRICE_PER_HOUR
    assert instance_type.instance_type == INSTANCE_TYPE
    assert type(instance_type.cpu) == dict
    assert type(instance_type.gpu) == dict
    assert type(instance_type.memory) == dict
    assert type(instance_type.storage) == dict
    assert type(instance_type.best_for) == list
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
    assert instance_type.best_for[0] == SMALL_ML_MODELS
    assert instance_type.best_for[1] == MULTI_GPU_TRAINING
    assert instance_type.best_for[2] == FP64_CALCULATIONS
    assert instance_type.best_for[3] == NVLINK
    assert instance_type.deploy_warning == DEPLOY_WARNING
    assert instance_type.model == MODEL
    assert instance_type.name == NAME
    assert instance_type.p2p == P2P
    assert instance_type.dynamic_price == DYNAMIC_PRICE
    assert instance_type.max_dynamic_price == MAX_DYNAMIC_PRICE
    assert instance_type.serverless_price == SERVERLESS_PRICE
    assert instance_type.serverless_spot_price == SERVERLESS_SPOT_PRICE
    assert instance_type.currency == CURRENCY
    assert instance_type.manufacturer == MANUFACTURER
    assert instance_type.display_name == DISPLAY_NAME
