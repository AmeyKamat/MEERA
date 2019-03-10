from subprocess import Popen, PIPE
from time import sleep

import pytest

def test_deployment():

    args = ["python3.6", "./src/index.py"]
    deployment = Popen(args, stdout=PIPE)
    sleep(60)

    if deployment.poll() is not None:
        pytest.fail("Deployment failed")
    else:
        deployment.kill()
