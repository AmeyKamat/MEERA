#!/usr/bin/env python3.6

import sys
from subprocess import Popen, PIPE
from time import sleep

import pytest

def test_deployment():
    
    args = ["./index.py"]
    meeraDeployment = Popen(args, env={'PYTHONPATH': ':'.join(sys.path)}, stdout=PIPE)
    sleep(60)

    if meeraDeployment.poll() is not None:
        pytest.fail("Deployment failed")
    else:
        meeraDeployment.kill()