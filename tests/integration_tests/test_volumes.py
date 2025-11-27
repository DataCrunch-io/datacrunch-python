import os
import time

import pytest

from verda.constants import Locations, VolumeStatus, VolumeTypes
from verda import VerdaClient

IN_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS') == 'true'


NVMe = VolumeTypes.NVMe


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in Github Actions.")
@pytest.mark.withoutresponses
class TestVolumes:
    def test_get_volumes_from_trash(self, verda_client: VerdaClient):
        # create new volume
        volume = verda_client.volumes.create(type=NVMe, name='test_volume', size=100)

        # delete volume
        verda_client.volumes.delete(volume.id)

        # get volumes from trash
        volumes = verda_client.volumes.get_in_trash()

        # assert volume is in trash
        assert volume.id in [v.id for v in volumes]

        # cleaning: permanently delete the volume
        verda_client.volumes.delete(volume.id, is_permanent=True)

    def test_permanently_delete_detached_volumes(seld, verda_client):
        # create new volume
        volume = verda_client.volumes.create(type=NVMe, name='test_volume', size=100)

        # permanently delete the detached volume
        verda_client.volumes.delete(volume.id, is_permanent=True)

        # sleep for 2 seconds
        time.sleep(2)

        # make sure the volume is not in trash
        volumes = verda_client.volumes.get_in_trash()

        # assert volume is not in trash
        assert volume.id not in [v.id for v in volumes]

        # get the volume
        volume = verda_client.volumes.get_by_id(volume.id)

        # assert volume status is deleted
        assert volume.status == verda_client.constants.volume_status.DELETED

    def test_permanently_delete_a_deleted_volume_from_trash(self, verda_client):
        # create new volume
        volume = verda_client.volumes.create(type=NVMe, name='test_volume', size=100)

        # delete volume
        verda_client.volumes.delete(volume.id)

        # sleep for 2 seconds
        time.sleep(2)

        # permanently delete the volume
        verda_client.volumes.delete(volume.id, is_permanent=True)

        # get the volume
        volume = verda_client.volumes.get_by_id(volume.id)

        # assert volume status is deleted
        assert volume.status == verda_client.constants.volume_status.DELETED

        # make sure the volume is not in trash
        volumes = verda_client.volumes.get_in_trash()

        # assert volume is not in trash
        assert volume.id not in [v.id for v in volumes]

    def test_create_volume(self, verda_client):
        # create new volume
        volume = verda_client.volumes.create(
            type=NVMe, name='test_volume', size=100, location=Locations.FIN_01
        )

        # assert volume is created
        assert volume.id is not None
        assert volume.location == Locations.FIN_01
        assert volume.status == VolumeStatus.ORDERED or volume.status == VolumeStatus.DETACHED

        # cleaning: delete volume
        verda_client.volumes.delete(volume.id, is_permanent=True)
