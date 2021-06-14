import responses  # https://github.com/getsentry/responses

from datacrunch.volume_types.volume_types import VolumeTypesService, VolumeType
from datacrunch.constants import VolumeTypes


USD = "usd"
NVMe_PRICE = 0.2
HDD_PRICE = 0.05


def test_volume_types(http_client):
    responses.add(
        responses.GET,
        http_client._base_url + "/volume-types",
        json=[
            {
                "type": VolumeTypes.NVMe,
                "price": {
                    "currency": USD,
                    "price_per_month_per_gb": NVMe_PRICE
                }
            },
            {
                "type": VolumeTypes.HDD,
                "price": {
                    "currency": USD,
                    "price_per_month_per_gb": HDD_PRICE
                }
            }
        ],
        status=200
    )

    volume_types_service = VolumeTypesService(http_client)

    # act
    volumes_types = volume_types_service.get()
    nvme_type = volumes_types[0]
    hdd_type = volumes_types[1]

    # assert
    assert type(volumes_types) == list
    assert len(volumes_types) == 2
    assert type(nvme_type) == VolumeType
    assert type(hdd_type) == VolumeType
    assert nvme_type.type == VolumeTypes.NVMe
    assert nvme_type.price_per_month_per_gb == NVMe_PRICE
    assert hdd_type.type == VolumeTypes.HDD
    assert hdd_type.price_per_month_per_gb == HDD_PRICE
