import os
import pytest
from datacrunch.datacrunch import DataCrunchClient

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in Github Actions.")
@pytest.mark.withoutresponses
class TestVolumes():

    def test_get_volumes_from_trash(self, datacrunch_client: DataCrunchClient):
        # create new volume
        volume = datacrunch_client.volumes.create(
            type=datacrunch_client.constants.volume_types.NVMe, name="test_volume", size=100)

        # delete volume
        datacrunch_client.volumes.delete(volume.id)

        # get volumes from trash
        volumes = datacrunch_client.volumes.get_in_trash()

        # assert volume is in trash
        assert volume.id in [v.id for v in volumes]

        # cleaning: permanently delete the volume
        datacrunch_client.volumes.delete(volume.id, is_permanent=True)

    def test_permanently_delete_detached_volumes(seld, datacrunch_client):
        # create new volume
        volume = datacrunch_client.volumes.create(
            type=datacrunch_client.constants.volume_types.NVMe, name="test_volume", size=100)

        # permanently delete the detached volume
        datacrunch_client.volumes.delete(volume.id, is_permanent=True)

        # make sure the volume is not in trash
        volumes = datacrunch_client.volumes.get_in_trash()

        # assert volume is not in trash
        assert volume.id not in [v.id for v in volumes]

        # get the volume
        volume = datacrunch_client.volumes.get_by_id(volume.id)

        # assert volume status is deleted
        assert volume.status == datacrunch_client.constants.volume_status.DELETED

    def test_permanently_delete_a_deleted_volume_from_trash(self, datacrunch_client):
        # create new volume
        volume = datacrunch_client.volumes.create(
            type=datacrunch_client.constants.volume_types.NVMe, name="test_volume", size=100)

        # delete volume
        datacrunch_client.volumes.delete(volume.id)

        # permanently delete the volume
        datacrunch_client.volumes.delete(volume.id, is_permanent=True)

        # get the volume
        volume = datacrunch_client.volumes.get_by_id(volume.id)

        # assert volume status is deleted
        assert volume.status == datacrunch_client.constants.volume_status.DELETED

        # make sure the volume is not in trash
        volumes = datacrunch_client.volumes.get_in_trash()

        # assert volume is not in trash
        assert volume.id not in [v.id for v in volumes]
