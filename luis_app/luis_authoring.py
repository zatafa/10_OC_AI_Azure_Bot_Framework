""" This script :
    1) Load the data and transform it to be usable by LUIS ;
    2) Create LUIS app with all its components;
    3) Train LUIS
    'NOTE' : Batch Testing is done on LUIS portal (luis.ai)
"""

import json
from luis_config import DefaultConfig
import utils.create_data as cd
import utils.create_luis as cl


# Load data
data_path = 'luis_app/data/frames.json'
final_df = cd.load_and_transform_data(data_path)


# Split data
train_df, test_df = cd.train_test_data(final_df)
print('Loading data...')
print('---------------------------------------')
print('Train shape: ', train_df.shape)
print('Test shape: ', test_df.shape)
print()


# Instantiate clients
print('Instantiate client(s)...')
print('---------------------------------------')
CONFIG = DefaultConfig()
client, clientRuntime = cl.instantiate_client(CONFIG)
print('Instantiate client(s): DONE!')
print()


# Create LUIS application
print('Creating application...')
print('---------------------------------------')
app_id, app_version = cl.create_app(client)
print()


# Add intents
print ('Adding intents to application...')
print('---------------------------------------')
cl.add_intents(client, app_id, app_version)
print()


# Add entities
print ('Adding entities to application...')
print('---------------------------------------')
cl.add_entities_prebuilts(client, app_id, app_version)
print()


# Create utterances
print('Call data to convert as utterance')
print('---------------------------------------')
bookFlight_utterance = cl.convert_as_utterances(train_df, intentCall='BookFlight', df='Train')
greetings_utterance, none_utterance = cl.get_other_utterances()
all_utterance = bookFlight_utterance + greetings_utterance + none_utterance
with open('luis_app/data/my_train.json', 'w+') as f:
    json.dump(all_utterance, f) # Save the data
print()


# Add utterances
print ('Adding utterances to application...')
print('---------------------------------------')
for i in range(0, len(all_utterance), 100):
    j = (i + 100)
    if j > len(all_utterance):
        j = len(all_utterance)
    cl.add_utterances_to_luis(client, app_id, app_version, all_utterance[i:j])
print()


# Train LUIS app
print ('Training application...')
print('---------------------------------------')
cl.train_app(client, app_id, app_version)
print()


# Create TEST data
print('Creating TEST data...')
print('---------------------------------------')
test_utterance = cl.convert_as_utterances(test_df, intentCall='BookFlight', df='Test')
with open('luis_app/data/my_test.json', 'w+') as f:
    json.dump(test_utterance, f) # Save the data