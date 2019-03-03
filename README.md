
MEERA
=====
![GitHub (pre-)release](https://img.shields.io/github/release-pre/AmeyKamat/MEERA.svg)

**MEERA** or **Multifunctional Event-driven Expert in Real-time Assistance** is a general purpose open source Artificially Intelligent Bot framework. MEERA is designed to be used as general purpose bot with expandable skill set that can be extended using easy to use plugin framework.


Build Status
------------
[![Build Status](https://travis-ci.org/AmeyKamat/MEERA.svg?branch=master)](https://travis-ci.org/AmeyKamat/MEERA) ![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/AmeyKamat/MEERA.svg)

Features
--------
* Configurable on-board machine learning module
* Expandable skill set with extensive plugin framework
* Fully configurable dialogue engine
* Asynchronous event driven message passing

Supported Platform
------------------
* Linux (Tested on Ubuntu 16.04 LTS)
* Python 3.6 (Tested on Python 3.6.8)
* pip (Tested on pip 19.0.1)

External Dependencies
---------------------
See [requirements.txt](https://github.com/AmeyKamat/MEERA/blob/master/requirements.txt) file for more details.

Getting Started
---------------

### Installing MEERA

To install MEERA:

1. Clone this repository on local machine.
2. `cd` to project root folder.
3. Run `chmod +x meera.sh`
4. Run `./meera.sh install` to install all dependancies.
5. Run `./meera.sh train` to train ML models
6. Search and replace API keys in all *.ini.example files (See *Properties to be Replaced* below)
7. rename all `*.ini.example` files to `*.ini`
8. Run `./meera.sh start` to deploy the application.

#### Properties to be Replaced

| File path                                            | Attribute Name | Notes                        |
|------------------------------------------------------|----------------|------------------------------|
| plugins/googleSelfLocation/plugin.ini.example        | key            | Google API Key               |
| plugins/newsAPI/plugin.ini.example                   | key            | NewsAPI API key              |
| plugins/openWeatherAPI/plugin.ini.example            | key            | OpenWeatherAPI API key       |
| plugins/timeZoneDB/plugin.ini.example                | key            | TimeZoneDB API key           |
| preprocessing/component.ini.example                  | key            | Google API key               |
| interface/telegram_bot/telegram.ini.example          | token          | Telegram bot token           |


### Usage

Once MEERA is installed on your system, you can start using MEERA from command line utility. Following are the commands supported:

#### Supported Commands


    Usage: ./meera.sh [command [optional parameters...]]

    Supported commands:

    clean               : cleans the project directory
    install             : installs project
    lint                : checks for compile time errors
    train [iterations]  : trains ML models. Optional parameter: # of iterations. Default value is 50
    evaluate            : evaluates ML models
    test                : runs tests
    start               : starts the deployment
    help                : help on supported commands

Here is what each of the above commands do:

* **clean**

  deletes pycache folders, log directory virtual environemnt and generated models. Once you clean the project directory, you will need to repeat installation procedure, before next usage.

* **install**
  
  sets up virtual environment and installs dependencies.

* **lint**
  
  scans for any compile time errors in the python scripts.

* **train [iterations]**

  trains machine learning models based on `*.utterance` files in project directory. This command take optional parameter, number of iterations of training for each model. If no value is passed, default number of iterations are 50.

* **evaluate**
  
  evaluates each machine learning model based against data in `*.utterance` files.

* **test**
  
  runs tests in `/tests` folder.

* **start**

  deploys MEERA and starts telegram daemon.


This repository provides an implementation of telegram bot that can be used to interact with MEERA. One needs to [create a telegram bot](https://core.telegram.org/bots#creating-a-new-bot), and add the bot token to `interface/telegram_bot/telegram.ini.example` file for bot to function.


Developers Manual
-----------------

### Definitions

COMING SOON

### Communication with Clients

MEERA exposes a WebSocket API for communication with clients. This API consist for 5 different messages which are exchanged as json objects.

COMING SOON

### Debugging API

MEERA also exposes following REST endpoints for debugging purpose

1. **Client Endpoint**
   
        path: /clients
        response:
       	   [
               {
                   "id": ...,
                   "name": ...,
                   "type": ...,
               },
               ...
           ]

2. **Conversation Endpoint**

        path: /conversations
        response:
            [
                {
                    "conversationId": ...,
                    "contexts": [...]
                },
                ...
            ]

3. **Context Endpoint**
        
        path: /context/{contextId}
        response:
            {
                    // context object
            }

### Building a Plugin

COMING SOON

### Architecture

MEERA banks on various components that communicate with each other through exchange of events. Following figure shows various components of MEERA interacting with each other.
     
![MEERA Architecture](https://github.com/AmeyKamat/MEERA/blob/master/docs/architecture.png "MEERA Architecture")

Built with
----------

* [circuits](https://github.com/circuits/circuits/)
* [spacy](https://spacy.io/)
* [python-telegram-bot](https://python-telegram-bot.org/)

Contributions
-------------
This project accepts pull requests from contributors.

License
-------

![GitHub](https://img.shields.io/github/license/AmeyKamat/MEERA.svg)

© 2019 Amey Kamat

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




