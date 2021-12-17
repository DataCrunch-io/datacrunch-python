import pytest
import responses  # https://github.com/getsentry/responses

from datacrunch.exceptions import APIException
from datacrunch.volumes.volumes import VolumesService, Volume
from datacrunch.constants import VolumeStatus, VolumeTypes, VolumeActions, ErrorCodes

INVALID_REQUEST = ErrorCodes.INVALID_REQUEST
INVALID_REQUEST_MESSAGE = 'Your existence is invalid'

INSTANCE_ID = "4fee633c-b119-4447-af9c-70ba17675fc5"

FIN1 = "FIN1"
NVME = "NVMe"
HDD = "HDD"
TARGET_VDA = "vda"
SSH_KEY_ID = '12345dc1-a5d2-4972-ae4e-d429115d055b'

NVME_VOL_ID = "cf995e26-ce69-4149-84a3-cdd1e100670f"
NVME_VOL_STATUS = VolumeStatus.ATTACHED
NVME_VOL_NAME = "Volume-nxC2tf9F"
NVME_VOL_SIZE = 50
NVME_VOL_CREATED_AT = "2021-06-02T12:56:49.582Z"


HDD_VOL_ID = "ea4edc62-9838-4b7c-bd5b-862f2efec675"
HDD_VOL_STATUS = VolumeStatus.DETACHED
HDD_VOL_NAME = "Volume-iHdL4ysR"
HDD_VOL_SIZE = 100
HDD_VOL_CREATED_AT = "2021-06-02T12:56:49.582Z"

NVME_VOLUME = {
    "id": NVME_VOL_ID,
    "status": NVME_VOL_STATUS,
    "instance_id": INSTANCE_ID,
    "name": NVME_VOL_NAME,
    "size": NVME_VOL_SIZE,
    "type": NVME,
    "location": FIN1,
    "is_os_volume": True,
    "created_at": NVME_VOL_CREATED_AT,
    "target": TARGET_VDA,
    "ssh_key_ids": SSH_KEY_ID
}

HDD_VOLUME = {
    "id": HDD_VOL_ID,
    "status": HDD_VOL_STATUS,
    "instance_id": None,
    "name": HDD_VOL_NAME,
    "size": HDD_VOL_SIZE,
    "type": HDD,
    "location": FIN1,
    "is_os_volume": False,
    "created_at": HDD_VOL_CREATED_AT,
    "target": None,
    "ssh_key_ids": []
}

PAYLOAD = [NVME_VOLUME, HDD_VOLUME]


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
        assert volume_nvme.id == NVME_VOL_ID
        assert volume_nvme.status == NVME_VOL_STATUS
        assert volume_nvme.instance_id == INSTANCE_ID
        assert volume_nvme.name == NVME_VOL_NAME
        assert volume_nvme.size == NVME_VOL_SIZE
        assert volume_nvme.type == NVME
        assert volume_nvme.location == FIN1
        assert volume_nvme.is_os_volume
        assert volume_nvme.created_at == NVME_VOL_CREATED_AT
        assert volume_nvme.target == TARGET_VDA
        assert volume_nvme.ssh_key_ids == SSH_KEY_ID

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
        assert volume_hdd.ssh_key_ids == []

    def test_get_volumes_by_status_successful(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.GET,
            endpoint + "?status=" + VolumeStatus.ATTACHED,
            json=[NVME_VOLUME],
            status=200
        )

        # act
        volumes = volumes_service.get(status=VolumeStatus.ATTACHED)
        volume_nvme = volumes[0]

        # assert
        assert type(volumes) == list
        assert len(volumes) == 1
        assert type(volume_nvme) == Volume
        assert volume_nvme.id == NVME_VOL_ID
        assert volume_nvme.status == NVME_VOL_STATUS
        assert volume_nvme.instance_id == INSTANCE_ID
        assert volume_nvme.name == NVME_VOL_NAME
        assert volume_nvme.size == NVME_VOL_SIZE
        assert volume_nvme.type == NVME
        assert volume_nvme.location == FIN1
        assert volume_nvme.is_os_volume
        assert volume_nvme.created_at == NVME_VOL_CREATED_AT
        assert volume_nvme.target == TARGET_VDA

    def test_get_volumes_by_status_failed(self, volumes_service, endpoint):
        url = endpoint + "?status=flummoxed"
        responses.add(
            responses.GET,
            url,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            volumes_service.get(status='flummoxed')

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(url, 1) is True

    def test_get_volume_by_id_successful(self, volumes_service, endpoint):
        # arrange - add response mock
        url = endpoint + "/" + NVME_VOL_ID
        responses.add(
            responses.GET,
            url,
            json=NVME_VOLUME,
            status=200
        )

        # act
        volume_nvme = volumes_service.get_by_id(NVME_VOL_ID)

        # assert
        assert type(volume_nvme) == Volume
        assert volume_nvme.id == NVME_VOL_ID
        assert volume_nvme.status == NVME_VOL_STATUS
        assert volume_nvme.instance_id == INSTANCE_ID
        assert volume_nvme.name == NVME_VOL_NAME
        assert volume_nvme.size == NVME_VOL_SIZE
        assert volume_nvme.type == NVME
        assert volume_nvme.location == FIN1
        assert volume_nvme.is_os_volume
        assert volume_nvme.created_at == NVME_VOL_CREATED_AT
        assert volume_nvme.target == TARGET_VDA

    def test_get_volume_by_id_failed(self, volumes_service, endpoint):
        # arrange - add response mock
        url = endpoint + "/x"
        responses.add(
            responses.GET,
            url,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            volumes_service.get_by_id('x')

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(url, 1) is True

    def test_create_volume_successful(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            endpoint,
            body=NVME_VOL_ID,
            status=202
        )
        responses.add(
            responses.GET,
            endpoint + "/" + NVME_VOL_ID,
            json=NVME_VOLUME,
            status=200
        )

        # act
        volume = volumes_service.create(VolumeTypes.NVMe, NVME_VOL_NAME, NVME_VOL_SIZE)

        # assert
        assert volume.id == NVME_VOL_ID

    def test_create_volume_failed(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            volumes_service.create(VolumeTypes.NVMe, NVME_VOL_NAME, 100000000000000000000000)

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True

    def test_attach_volume_successful(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            status=202,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.ATTACH,
                    "instance_id": INSTANCE_ID
                })
            ]
        )

        # act
        result = volumes_service.attach(NVME_VOL_ID, INSTANCE_ID)

        # assert
        assert result is None
        assert responses.assert_call_count(endpoint, 1) is True

    def test_attach_volume_failed(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.ATTACH,
                    "instance_id": INSTANCE_ID
                })
            ]
        )

        # act
        with pytest.raises(APIException) as excinfo:
            volumes_service.attach(NVME_VOL_ID, INSTANCE_ID)

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True

    def test_detach_volume_successful(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            status=202,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.DETACH
                })
            ]
        )

        # act
        result = volumes_service.detach(NVME_VOL_ID)

        # assert
        assert result is None
        assert responses.assert_call_count(endpoint, 1) is True

    def test_detach_volume_failed(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.DETACH
                })
            ]
        )

        # act
        with pytest.raises(APIException) as excinfo:
            volumes_service.detach(NVME_VOL_ID)

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True

    def test_rename_volume_successful(self, volumes_service, endpoint):
        new_name = "bob"

        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            status=202,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.RENAME,
                    "name": new_name,
                })
            ]
        )

        # act
        result = volumes_service.rename(NVME_VOL_ID, new_name)

        # assert
        assert result is None
        assert responses.assert_call_count(endpoint, 1) is True

    def test_rename_volume_failed(self, volumes_service, endpoint):
        new_name = "bob"

        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.RENAME,
                    "name": new_name
                })
            ]
        )

        # act
        with pytest.raises(APIException) as excinfo:
            volumes_service.rename(NVME_VOL_ID, new_name)

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True

    def test_increase_volume_size_successful(self, volumes_service, endpoint):
        new_size = 100000000000000

        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            status=202,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.INCREASE_SIZE,
                    "size": new_size,
                })
            ]
        )

        # act
        result = volumes_service.increase_size(NVME_VOL_ID, new_size)

        # assert
        assert result is None
        assert responses.assert_call_count(endpoint, 1) is True

    def test_increase_volume_size_failed(self, volumes_service, endpoint):
        new_size = 100000000000000

        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.INCREASE_SIZE,
                    "size": new_size
                })
            ]
        )

        # act
        with pytest.raises(APIException) as excinfo:
            volumes_service.increase_size(NVME_VOL_ID, new_size)

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True

    def test_delete_volume_successful(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            status=202,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.DELETE
                })
            ]
        )

        # act
        result = volumes_service.delete(NVME_VOL_ID)

        # assert
        assert result is None
        assert responses.assert_call_count(endpoint, 1) is True

    def test_delete_volume_failed(self, volumes_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.PUT,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400,
            match=[
                responses.json_params_matcher({
                    "id": NVME_VOL_ID,
                    "action": VolumeActions.DELETE
                })
            ]
        )

        # act
        with pytest.raises(APIException) as excinfo:
            volumes_service.delete(NVME_VOL_ID)

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True
