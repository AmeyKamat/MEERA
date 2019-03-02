import sys
from subprocess import Popen, PIPE
from time import sleep

import pytest

def test_deployment():
    
    args = ["python3.6", "./index.py"]
    meeraDeployment = Popen(args, stdout=PIPE)
    sleep(60)

    if meeraDeployment.poll() is not None:
        pytest.fail("Deployment failed")
    else:
        meeraDeployment.kill()