import pytest
import responses  # https://github.com/getsentry/responses

from datacrunch.exceptions import APIException
from datacrunch.volumes.volumes import VolumesService, Volume
from datacrunch.constants import VolumeActions, VolumeStatus, ErrorCodes

INSTANCE_ID = "4fee633c-b119-4447-af9c-70ba17675fc5"

FIN1 = "FIN1"
NVME = "NVMe"
HDD = "HDD"
TARGET_VDA = "vda"

NMVE_VOL_ID = "cf995e26-ce69-4149-84a3-cdd1e100670f"
NVME_VOL_STATUS = VolumeStatus.ATTACHED
NVME_VOL_NAME = "Volume-nxC2tf9F"
NVME_VOL_SIZE = 50
NVME_VOL_CREATED_AT = "2021-06-02T12:56:49.582Z"

HDD_VOL_ID = "ea4edc62-9838-4b7c-bd5b-862f2efec675"
HDD_VOL_STATUS = VolumeStatus.DETACHED
HDD_VOL_NAME = "Volume-iHdL4ysR"
HDD_VOL_SIZE = 100
HDD_VOL_CREATED_AT = "2021-06-02T12:56:49.582Z"


PAYLOAD = [
    {
        "id": NMVE_VOL_ID,
        "status": NVME_VOL_STATUS,
        "instance_id": INSTANCE_ID,
        "name": NVME_VOL_NAME,
        "size": NVME_VOL_SIZE,
        "type": NVME,
        "location": FIN1,
        "is_os_volume": True,
        "created_at": NVME_VOL_CREATED_AT,
        "target": TARGET_VDA
    },
    {
        "id": HDD_VOL_ID,
        "status": HDD_VOL_STATUS,
        "instance_id": None,
        "name": HDD_VOL_NAME,
        "size": HDD_VOL_SIZE,
        "type": HDD,
        "location": FIN1,
        "is_os_volume": False,
        "created_at": HDD_VOL_CREATED_AT,
        "target": None
    }
]


class TestVolumesService:
    @pytest.fixture
    def volumes_service(self, http_client):
        return VolumesService(http_client)

    @pytest.fixture
    def endpoint(self, http_client):
        return http_client._base_url + "/volumes"

    def test_get_instances(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.GET,
            endpoint,
            json=PAYLOAD,
            status=200
        )

        # act
        volumes = volumes_service.get()
        volume_nvme = volumes[0]
        volume_hdd = volumes[1]

        # assert
        assert type(volumes) == list
        assert len(volumes) == 2
        assert type(volume_nvme) == Volume
        assert type(volume_hdd) == Volume
        assert volume_nvme.id == NMVE_VOL_ID
        assert volume_nvme.status == NVME_VOL_STATUS
        assert volume_nvme.instance_id == INSTANCE_ID
        assert volume_nvme.name == NVME_VOL_NAME
        assert volume_nvme.size == NVME_VOL_SIZE
        assert volume_nvme.type == NVME
        assert volume_nvme.location == FIN1
        assert volume_nvme.is_os_volume
        assert volume_nvme.created_at == NVME_VOL_CREATED_AT
        assert volume_nvme.target == TARGET_VDA

        assert volume_hdd.id == HDD_VOL_ID
        assert volume_hdd.status == HDD_VOL_STATUS
        assert volume_hdd.instance_id is None
        assert volume_hdd.name == HDD_VOL_NAME
        assert volume_hdd.size == HDD_VOL_SIZE
        assert volume_hdd.type == HDD
        assert volume_hdd.location == FIN1
        assert volume_hdd.is_os_volume is False
        assert volume_hdd.created_at == HDD_VOL_CREATED_AT
        assert volume_hdd.target is None

    def test_get_volumes_by_status_successful(self, volumes_service, endpoint):
        # TODO:
        return

    def test_get_volumes_by_status_failed(self, volumes_service, endpoint):
        # TODO:
        return

    def test_get_volume_by_id_successful(self, volumes_service, endpoint):
        # TODO:
        return

    def test_get_volume_by_id_failed(self, volumes_service, endpoint):
        # TODO:
        return

    def test_create_volume_successful(self, volumes_service, endpoint):
        # TODO:
        return

    def test_create_volume_failed(self, volumes_service, endpoint):
        # TODO:
        return

    def test_attach_volume_successful(self, volumes_service, endpoint):
        # TODO:
        return

    def test_attach_volume_failed(self, volumes_service, endpoint):
        # TODO:
        return

    def test_detach_volume_successful(self, volumes_service, endpoint):
        # TODO:
        return

    def test_detach_volume_failed(self, volumes_service, endpoint):
        # TODO:
        return

    def test_rename_volume_successful(self, volumes_service, endpoint):
        # TODO:
        return

    def test_rename_volume_failed(self, volumes_service, endpoint):
        # TODO:
        return

    def test_increase_volume_size_successful(self, volumes_service, endpoint):
        # TODO:
        return

    def test_increase_volume_size_failed(self, volumes_service, endpoint):
        # TODO:
        return

    def test_delete_volume_successful(self, volumes_service, endpoint):
        # TODO:
        return

    def test_delete_volume_failed(self, volumes_service, endpoint):
        # TODO:
        retur