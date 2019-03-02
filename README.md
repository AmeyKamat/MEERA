# M.E.E.R.A

[![Build Status](https://travis-ci.org/AmeyKamat/MEERA.svg?branch=master)](https://travis-ci.org/AmeyKamat/MEERA) ![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/AmeyKamat/MEERA.svg?style=plastic) [![Documentation Status](https://readthedocs.org/projects/meera/badge/?version=latest)](https://meera.readthedocs.io/en/latest/?badge=latest) 

![GitHub (pre-)release](https://img.shields.io/github/release-pre/AmeyKamat/MEERA.svg) ![GitHub](https://img.shields.io/github/license/AmeyKamat/MEERA.svg) 

![MEERA Logo](https://github.com/AmeyKamat/MEERA/blob/master/doc/logo.png "MEERA")

MEERA is a acronym for "Multifunctional Event-driven Expert in Real-time Assistance". It is an open source AI Bot framework. The machine learning module is entirely on board. MEERA can be easily integrated with any third party service by developing a plugin.

## System Requirements

* Linux (Tested on Ubuntu 16.04 LTS)
* Python 3.6 (Tested on Python 3.6.8)
* pip (Tested on pip 19.0.1)

## Usage

    Usage: ./meera.sh [command]

    Supported commands:

    clean				: cleans the project directory
    install				: installs project
    lint				: checks for compile time errors
    train [iterations]	: trains ML models. Optional parameter: # of iterations. Default value is 50
    evaluate			: evaluates ML models
    test				: runs tests
    start				: starts the deployment
    help				: help on supported commands

## Technology

* Event Driven Architecture: [Circuits](https://github.com/circuits/circuits/)
* Machine Learning Modelling: [Spacy](https://spacy.io/)

## Architecture
     
![MEERA Architecture](https://github.com/AmeyKamat/MEERA/blob/master/doc/architecture.png "MEERA Architecture")
