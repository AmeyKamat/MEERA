import os

from definitions import ROOT_DIR, ABS_PLUGINS_DIR

def get_skill_data(skill_raw_training_data):
    skill_data = []
    for line in skill_raw_training_data:
        skill_data.append({
            "sentence": get_sentence(line),
            "category": get_category(line, get_skill_categories(skill_raw_training_data)),
            "entities": get_entities(line)
        })

    return skill_data

def get_chat_data(chat_raw_training_data):
    chat_data = []
    for line in chat_raw_training_data:
        chat_data.append({
            "sentence": get_sentence(line),
            "category": get_category(line, get_chat_categories(chat_raw_training_data))
        })
    return chat_data

def get_request_type_resolution_data(skill_raw_training_data, chat_raw_training_data):
    request_type_resolution_data = []
    for line in skill_raw_training_data:
        request_type_resolution_data.append({
            "sentence": get_sentence(line),
            "category": {"chat": 0.0, "skill": 1.0}
        })
    for line in chat_raw_training_data:
        request_type_resolution_data.append({
            "sentence": get_sentence(line),
            "category": {"chat": 1.0, "skill": 0.0}
        })
    return request_type_resolution_data

def get_sentence(line):
    return line.split('|')[0].lower().strip()

def get_category(line, categories):
    category_counter = {}
    category = line.split('|')[1].strip()
    for defined_category in categories:
        if defined_category == category:
            category_counter[defined_category] = 1.0
        else:
            category_counter[defined_category] = 0.0
    return category_counter

def get_entities(line):
    entities = []
    record = line.split('|')
    if len(record) > 2:
        for index in range(2, len(record)):
            entity = record[index].strip()
            entities.append(
                (
                    int(entity.split(',')[1]),          # start index
                    int(entity.split(',')[2]),          # end index
                    entity.split(',')[0].strip()        # entity
                )
            )
    return entities

def get_entity_names(line):
    entities = []
    record = line.split('|')
    if len(record) > 2:
        for index in range(2, len(record)):
            entity = record[index]
            entities.append(entity.split(',')[0].strip())
    return entities

def get_skill_categories(skill_raw_training_data):
    return {line.split('|')[1].strip() for line in skill_raw_training_data}

def get_chat_categories(chat_raw_training_data):
    return {line.split('|')[1].strip() for line in chat_raw_training_data}

def get_entity_categories(skill_raw_training_data):
    entity_names = []
    for line in skill_raw_training_data:
        entity_names += get_entity_names(line)
    return set(entity_names)

def get_data():

    skill_raw_training_data = []
    chat_raw_training_data = []

    installed_plugins = [
        f.name for f in os.scandir(ABS_PLUGINS_DIR) if f.is_dir() and f.name != "__pycache__"
    ]

    for plugin in installed_plugins:
        file = open(os.path.join(ABS_PLUGINS_DIR, plugin, 'plugin.utterance'), "r")
        for line in file:
            skill_raw_training_data.append(line)

    file = open(os.path.join(ROOT_DIR, 'nlp', 'chat.utterance'))

    for line in file:
        chat_raw_training_data.append(line)

    return {
        "skill_data": get_skill_data(skill_raw_training_data),
        "chat_data": get_chat_data(chat_raw_training_data),
        "request_type_data": get_request_type_resolution_data(
            skill_raw_training_data, chat_raw_training_data),
        "intents": get_skill_categories(skill_raw_training_data),
        "chat_categories": get_chat_categories(chat_raw_training_data),
        "entities": get_entity_categories(skill_raw_training_data),
        "request_types": ["skill", "chat"]
    }
