
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

| File path                                     | Attribute | Description            | More Details                                                         |
|:----------------------------------------------|:----------|:-----------------------|:---------------------------------------------------------------------|
| plugins/googleSelfLocation/plugin.ini.example | key       | Google API Key         | [link](https://developers.google.com/places/web-service/get-api-key) |
| plugins/newsAPI/plugin.ini.example            | key       | NewsAPI API key        | [link](https://newsapi.org/register)                                 |
| plugins/openWeatherAPI/plugin.ini.example     | key       | OpenWeatherAPI API key | [link](https://openweathermap.org/appid#get)                         |
| plugins/timeZoneDB/plugin.ini.example         | key       | TimeZoneDB API key     | [link](https://timezonedb.com/api)                                   |
| preprocessing/component.ini.example           | key       | Google API key         | [link](https://developers.google.com/places/web-service/get-api-key) |
| interface/telegram_bot/telegram.ini.example   | token     | Telegram bot token     | [link](https://core.telegram.org/bots#creating-a-new-bot)            |


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

### Concepts

#### Client

Client is an object that represents external device that is connected to MEERA through websocket API. MEERA generates an `id` for each of such client which is used to identify the socket to be used to communicate with this device. Client also has a human friendly `name` attribute and `type` attribute (currently restricted to `mobile_app`, `web_app` or `telegram_bot`). See [this](https://github.com/AmeyKamat/MEERA/blob/master/client/model.py) for definition of client object.

#### Context

Each message that MEERA receives is represent by a Context object. This object contains information such as `message`, `clientId` of the client that sent the message, `nlpAnalysis` performed on the context, `conversationId` of the conversation the context belongs to, `previousContext` in the context chain of the conversation, `result` object generated by the plugins, `interaction` object generated by the plugins, etc. Each context is uniquely identified by a `contextId`.  See [this](https://github.com/AmeyKamat/MEERA/blob/master/context/model.py) for the object definition.

#### Conversation

Conversation is sequence of contexts from a particular client. Each conversation is uniquely identified by a `conversationId`.

#### NlpAnalysis

This object stores optput of each of the machine learning models. NlpAnalysis store `intent` of the message, `entities` extracted from the message and `confidence` associated with the intent. See [this](https://github.com/AmeyKamat/MEERA/blob/master/nlp/model.py) for the definition. 

#### Result

This object stores the output of plugin executors. Plugin developers can store all the information required to generate dialogue in this object.

#### Interaction

Interaction object is the output of plugin dialogue generators. it can contains following attributes that can be used in various scenarios in client devices subject to their implementation in client. Note that it is not mandated to implement all of these attributes on client. If a particular attribute is not implemented on client, value of that attribute should be ignored. For example, the telegram client shipped by default with MEERA only supports `text` attribute. However, plugins are expected to implement atleast `text` an `voice` the attributes below. 

| Attribute | Description                                                                       |
|-----------|-----------------------------------------------------------------------------------|
| text      | text that can be shown on the client                                              |
| voice     | text that can be passed to speech synthesis module in client                      |
| link      | hypertext link that be opened in in browser on client side                        |
| sound     | link to the sound clip that can be played in embeded media player on client       |
| video     | link to the video clip that can be played in embeded media player on client       |
| youtube   | link to the youotube video that can be played in embeded youtube player on client |


### Machine Learning Models

MEERA generates 4 models on `./meera.sh train` command. These are listed below:

| Model Name                       | Locatio                           |Type     | Function                             |
|----------------------------------|-----------------------------------|---------|--------------------------------------|
| `en.assistant.requestType.model` | `./nlp/models/request_type_model` | textcat | predicts if message is chat or skill |
| `en.assistant.chat.model`        | `./nlp/models/chat_model`         | textcat | generates response for chat message  |
| `en.assistant.entity.model`      | `./nlp/models/entities_model`     | ner     | extracts entities from skill message |
| `en.assistant.intent.model`      | `./nlp/models/intent_model`       | textcat | predicts intent of skill message     | 


### Developing a Plugin

MEERA performs tasks using plugins included. your plugin should be place in [this directory](https://github.com/AmeyKamat/MEERA/tree/master/plugins) for MEERA to load it. Plugins basically consist of 4 components as follows:

#### plugin.ini
 
`plugin.ini` is a property file that describes the plugin. It should have following structure

    [NameOfThePlugin]                            # This should match with the name of the executor and dialogue generator class
    intent = intentOnWhichPluginWillBeTriggered
    ... any other property you might load in executor or dialogue generator ...


#### executor.py

`executor.py` is class where message received by MEERA can be processed.

Following is the basic structure of executor.py
        
    # Any modules you want to import

    class NameOfThePlugin(object):                       # This should be same as plugin.ini file

        def __init__(self, config):
	        super(NameOfThePlugin, self).__init__()
	        self.config = config                         # config object provides all properties from plugin.ini as a dict

        def execute(self, context):
	        # process the context here. All attributes in context will be read only. any changes to context object will not be reflected
	        result = {}
	        # build result object
	        return result

If your plugin expects client location, you should first check in `self-location` key exists in `context.nlpAnalysis.entities` and if not raise `execution.exception.SelfLocationNotFoundException`. If the key exists, you will get following object as value of key `self-location` in `context.nlpAnalysis.entities`:

    {
        "latitude": ...
        "longitude": ...
    }

Also for every human friendly `date` and `location` entity identified, MEERA translates them to absolute date and latitude-longitude pair out-of-the-box respectively.

For a `date` entity, you will find following object in `context.nlpAnalysis.entities`

    { 
        "date": "yesterday",
        "parsedDate": ...
	} 

For `location` entity:

	{
        "location": "london",
        "latitude": ...,
        "longitude": ...
	}

#### dialogue.py

`dialogue.py` defines how you want to define response of MEERA for a plugin. Output of this class is interaction object. Following is basic structure of dialogue.py

    # Any modules you want to import

    class NameOfThePlugin(object):                      # This should be same as plugin.ini file

        def __init__(self, config):
	        super(NameOfThePlugin, self).__init__()
	        self.config = config                        # config object provides all properties from plugin.ini as a dict

        def generate(self, result):
	        # extract information from result. Result object is read-only.

	        return {
                "text": ...,
                "voice": ...,
                "link": ...
	        }

#### plugin.utterance

`plugin.utterance` defines examples of utterances that should trigger the plugin as well as guides on what entities to extract from these utterances. Each of the example should be on a new line an should contain an utterance, intent for that utterance and list of entities to be extracted.

Following is a structure of each record

    sentence|intent[|entity1,start_index,end_index|entity2,start_index,end_index...]

For example:

    where am i|self-location
    how far is mumbai from delhi|distance|source-location,11,17|destination-location,23,28

Once you have these all files is expected location, update [this plugins.ini file](https://github.com/AmeyKamat/MEERA/blob/master/plugins/plugins.ini) for binding the plugin to MEERA. 

### Communication with Clients

MEERA exposes a WebSocket API for communication with clients. This API consist for 5 different messages which are exchanged as json objects.

COMING SOON

### Debugging API

MEERA also exposes following REST endpoints for debugging purpose

#### GET /clients

`/clients` endpoint displays all the clients registered with MEERA.

##### Usage

    $ curl -sv -H "Accept: application/json" http://localhost:8000/clients | json_pp
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 8000 (#0)
    > GET /clients HTTP/1.1
    > Host: localhost:8000
    > User-Agent: curl/7.47.0
    > Accept: application/json
    > 
    < HTTP/1.1 200 OK
    < Date: Sun, 03 Mar 2019 14:43:01 GMT
    < Server: circuits.web/3.2
    < Content-Type: text/html; charset=utf-8
    < Content-Length: 92
    < 
    { [92 bytes data]
    * Connection #0 to host localhost left intact
    [
       {
          "name" : "telegram",
          "type" : "telegram_bot",
          "id" : "bff7d73b-7f27-4faa-bafb-fcee095d4f5a"
       }
    ]


#### GET /conversations

`/conversations` endpoints displays all the conversations in the memory.

##### Usage

    $ curl -sv -H "Accept: application/json" http://localhost:8000/conversations | json_pp
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 8000 (#0)
    > GET /conversations HTTP/1.1
    > Host: localhost:8000
    > User-Agent: curl/7.47.0
    > Accept: application/json
    > 
    < HTTP/1.1 200 OK
    < Date: Sun, 03 Mar 2019 14:50:49 GMT
    < Server: circuits.web/3.2
    < Content-Type: text/html; charset=utf-8
    < Content-Length: 114
    < 
    { [114 bytes data]
    * Connection #0 to host localhost left intact
    [
       {
          "contexts" : [
              "9e4aea6d-c790-4b42-a5bb-444fdb8453bc"
          ],
          "conversationId" : "ba286c55-cde8-4fb0-b10d-8db57bf9b00a"
       }
    ]

#### GET /context/{contextId}

`/context` endpoint diplays all the data aggregated during the lifetime of the context

##### Usage

    $ curl -sv -H "Accept: application/json" http://localhost:8000/context/9e4aea6d-c790-4b42-a5bb-444fdb8453bc | json_pp
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 8000 (#0)
    > GET /context/9e4aea6d-c790-4b42-a5bb-444fdb8453bc HTTP/1.1
    > Host: localhost:8000
    > User-Agent: curl/7.47.0
    > Accept: application/json
    > 
    < HTTP/1.1 200 OK
    < Date: Sun, 03 Mar 2019 14:54:35 GMT
    < Server: circuits.web/3.2
    < Content-Type: text/html; charset=utf-8
    < Content-Length: 423
    < 
    { [423 bytes data]
    * Connection #0 to host localhost left intact
    {
        "message" : "Hi",
        "nlpAnalysis" : {
            "confidence" : 4.53978718724102e-05,
            "requestType" : "chat",
            "category" : "Hello!"
        },
        "contextId" : "9e4aea6d-c790-4b42-a5bb-444fdb8453bc",
        "conversationId" : "ba286c55-cde8-4fb0-b10d-8db57bf9b00a",
        "interaction" : {
            "voice" : "Hello!",
            "text" : "Hello!"
        },
        "clientId" : "bff7d73b-7f27-4faa-bafb-fcee095d4f5a"
}


### Architecture

MEERA banks on various components that communicate with each other through exchange of events. Following figure shows various components of MEERA interacting with each other.
     
![MEERA Architecture](https://github.com/AmeyKamat/MEERA/blob/master/docs/architecture.png "MEERA Architecture")

Built with
----------

* [circuits](https://github.com/circuits/circuits/)
* [spacy](https://spacy.io/)
* [python-telegram-bot](https://python-telegram-bot.org/)

Contributions to MEERA
----------------------

### Issues

Feel free to submit an issue or request an enhancement [here](https://github.com/AmeyKamat/MEERA/issues). Ensure that you tag the issue as "Bug" or "Enhancement"

### Contribution

This project accepts pull requests from contributors. We usually follow "fork-and-pull" git workflow. If you are fixing an issue or developing an enhancement, please create an issue on [this page](https://github.com/AmeyKamat/MEERA/issues), before creating a pull request. Ensure that you tag the issue as "Bug" or "Enhancement".

This project follows [SemVer](https://semver.org/) for versioning.


About the Author
----------------

[Amey Kamat](http://www.ameykamat.in)

Feel free to drop your reviews at `amey@ameykamat.in`.


License
-------

![GitHub](https://img.shields.io/github/license/AmeyKamat/MEERA.svg)

© 2019 Amey Kamat

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.