import os
import pytest
from datacrunch.datacrunch import DataCrunchClient
from datacrunch.constants import Locations

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in Github Actions.")
@pytest.mark.withoutresponses
class TestInstances():

    def test_create_instance(self, datacrunch_client: DataCrunchClient):
        # get ssh key
        ssh_key = datacrunch_client.ssh_keys.get()[0]

        # create instance
        instance = datacrunch_client.instances.create(
            hostname="test-instance",
            location=Locations.FIN_01,
            instance_type='CPU.4V',
            description="test instance",
            image="ubuntu-18.04",
            ssh_key_ids=[ssh_key.id])

        # assert instance is created
        assert instance.id is not None
        assert instance.status == datacrunch_client.constants.instance_status.PROVISIONING

        # delete instance
        datacrunch_client.instances.action(instance.id, "delete")

        # permanently delete all volumes in trash
        trash = datacrunch_client.volumes.get_in_trash()
        for volume in trash:
            datacrunch_client.volumes.delete(volume.id, is_permanent=True)
