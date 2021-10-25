# Import packages
import numpy as np
import time
import json
from luis_config import DefaultConfig
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials


######################### Instantiate LUIS Client ##########################
############################################################################
CONFIG = DefaultConfig()

# Instantiate clients
def instantiate_client(CONFIG):
    # Instantiate a LUIS Authoring client
    client = LUISAuthoringClient(
        CONFIG.AUTHORING_ENDPOINT,
        CognitiveServicesCredentials(CONFIG.AUTHORING_KEY))
    
    # Instantiate a LUIS Runtime Client
    clientRuntime = LUISRuntimeClient(
        CONFIG.PREDICTION_ENDPOINT,
        CognitiveServicesCredentials(CONFIG.PREDICTION_KEY))
    
    return client, clientRuntime

######################### Create LUIS application ##########################
############################################################################
def create_app(client):
    """Creation of LUIS Appication.
            Parameters: None
            Outputs: app_id (LUIS App ID), app_version(Luis App version)
    """
    # Set LUIS App details
    app_name = 'OurFlyMeLuisApp'
    app_version = '0.1'
    app_description = 'Flight booking App built with LUIS Python SDK.'
    app_culture  = 'en-us' 
    
    # Call the details
    app_id = client.apps.add(dict(
        name=app_name,
        initial_version_id=app_version,
        description=app_description,
        culture=app_culture))
    
    print('Created LUIS app {}\n  with ID {}'.format(app_name, app_id))
    return app_id, app_version


############################ Add LUIS intents ##############################
############################################################################
def add_intents(client, app_id, app_version):
    """Creation of intents.
            Parameters: app_id (LUIS App ID), app_version(Luis App version)
            Outputs: intents' ID
    """
    # Create intents list
    intents_list = ['BookFlight', 'Greetings']
    
    for intent in intents_list:
        intentId = client.model.add_intent(app_id, app_version, intent)
        print("{} ID {} added.".format(intent, intentId))


################### Add LUIS entities : OPTIONS AVAILABLE ##################
############################################################################
def create_and_add_entities(client, app_id, app_version):
    """ Creation of all entities (incl. prebuit entities and subentities).
            Parameters: app_id (LUIS App ID), app_version(Luis App version),
                        options to add prebuilt and sub- entities
            Outputs: entities' ID 
    """

# Here we create entities, pre-built entites and subentities
def add_entities_prebuilts(client, app_id, app_version):
   
    # Create a parent entity:
    city_ID = {'name': 'city'}

    # Define and add machine-learned entity to app
    origine_ID = client.model.add_entity(app_id, app_version,  name='or_city')
    print("Entity {} {} added.".format('or_city', origine_ID))

    destination_ID = client.model.add_entity(app_id, app_version, name='dst_city')
    print("Entity {} {} added.".format('dst_city', destination_ID))
    
    start_date_ID = client.model.add_entity(app_id, app_version, name='str_date')
    print("Entity {} {} added.".format('str_date', start_date_ID))
    
    end_date_ID = client.model.add_entity(app_id, app_version, name='end_date')
    print("Entity {} {} added.".format('end_date', end_date_ID))
    
    budget_ID = client.model.add_entity(app_id, app_version, name='budget')
    print("Entity {} {} added.".format('budget', budget_ID))
    
    # Add prebuilt entities
    datetime_ID = client.model.add_prebuilt(app_id, app_version, prebuilt_extractor_names=['datetimeV2'])
    print("Prebuit Entity {} {} added.".format('datetime', datetime_ID))
    

############ Create and add TRAIN utterances with valid format #############
############################################################################
def create_train_utterance(intent, utterance, *labels):
    """LUIS expects a specifif data format for TRAIN data:
        this function creates these formatted utterances.
            Parameters:
                intent: the intent for which the utterances are associated
                utterance: a batch of utterances
                labels: 
                    - key/value pair for entities 
                    - key/value pair for char start index (startCharIndex)
                    - key value pair for char end index (endCharIndex)
            Outputs:
                the formatted data, including :
                    - text, intentName, 
                    - a list of dictionary of entityLabels and char's indexes
    """

    text = utterance.lower()

    def label(name, value):
        value = value.lower()
        start = text.index(value)

        return dict(
            entityName=name,
            startCharIndex=start,
            endCharIndex=start + len(value))
    
    return dict(text=text, intentName=intent,
                entityLabels=[label(n, v) for (n, v) in labels])
    

def convert_as_utterances(data, intentCall='BookFlight', df='Train'):
    """Call data structure for 'Train' or 'Test'.
            Parameters: 
                dataframe, name of intent, train/test indication
            Outputs:
                my_data : transformed data
    """
    
    # Create an empty list
    utterances_data = []

    # To exclude entities with nan values from the list
    nan_list = ['nan', 'NaN', '', np.nan, None]

    # Iterate over the rows
    for index, row in data.iterrows():

        # Create a list of entities'tuple (key, value)
        entities = []
        if row.or_city not in nan_list:
            entities.append(('or_city', row.or_city))
        if row.dst_city not in nan_list:
            entities.append(('dst_city', row.dst_city))
        if row.str_date not in nan_list:
            entities.append(('str_date', row.str_date))
        if row.end_date not in nan_list:
            entities.append(('end_date', row.end_date))
        if row.budget not in nan_list:
            entities.append(('budget', row.budget))
    
        # Call the function to create the LUIS data in correct format
        if df == 'Train':
            output = create_train_utterance(intentCall,row.text,*entities)
        if df == 'Test':
            output = create_test_utterance(intentCall,row.text,*entities)
        
        # Save outputs in utterances_data
        utterances_data.append(output)

    print('Length Utterances data', len(utterances_data))

    # Format to JSON and save
    y = json.dumps(utterances_data)
    my_data = json.loads(y)

    return my_data

def get_other_utterances():
    """Creates utterances examples with NO entityLabels
    """

    # Define for Greetings Intent
    greetings_labeled_intent = [
        {'text':'Hello', 'intentName':'Greetings'},
        {'text':'Hello there', 'intentName':'Greetings'},
        {'text':'Hello bot', 'intentName':'Greetings'},
        {'text':'Hi', 'intentName':'Greetings'},
        {'text':'Hi there', 'intentName':'Greetings'},
        {'text':'Good morning', 'intentName':'Greetings'},
        {'text':'Good afternoon', 'intentName':'Greetings'},
        {'text':'Good evening', 'intentName':'Greetings'},
        {'text':'Hey', 'intentName':'Greetings'},
        {'text':'Hey there', 'intentName':'Greetings'},
        {'text':'Yo', 'intentName':'Greetings'},
    ]

    # Define for None Intent
    none_labeled_intent = [
        {'text':"My buddy and I want to have the best time of our lives",
        'intentName':'None'},
        {'text':"My name is Stephen King and I want to book a quiet getaway",
        'intentName':'None'},
        {'text':"I'm looking for a place to get away with my best friend",
        'intentName':'None'},
        {'text':"I am in dire need of a vacation",
        'intentName':'None'},
        {'text':"Do you think you can give an amazing package?",
        'intentName':'None'},
        {'text':"I would like to book a hotel in Paris",
        'intentName':'None'},
        {'text':"Book me a restaurant",
        'intentName':'None'},
    ]

    return greetings_labeled_intent, none_labeled_intent

def add_utterances_to_luis(client, app_id, app_version, my_data):
  # Collect utterances data
  utterances = my_data
  
  # Add the utterances in batch
  # You may add 100 (max.) number of example utterances
  # for any number of intents in one call.
  client.examples.batch(app_id, app_version, utterances)


############################# Train LUIS App ###############################
############################################################################
def train_app(client, app_id, app_version):
    """Train the LUIS app when all the utterances are uploaded.
            Parameters:
                app_id : LUIS App ID
                app_version : Luis App version
            Outputs:
                None (the trained status can be checked on LUIS portal)
    """
    client.train.train_version(app_id, app_version)
    waiting = True
    
    while waiting:
        info = client.train.get_status(app_id, app_version)
        
        # get_status returns a list of training statuses, one for each model
        # Loop through them and make sure all are done
        waiting = any(
            map(
                lambda x: 'Queued' == x.details.status or 'InProgress' == x.details.status, info))
        
        if waiting:
            print ("Waiting 30 seconds for training to complete...")
            time.sleep(30)

        else:
            print('Trained')
            waiting = False


############################ Publish LUIS App ##############################
############################################################################

def publish_app(client, app_id, app_version):
    """Publish LUIS application.
            Parameters:
                app_id : LUIS App ID
                app_version : Luis App version
            Outputs:
                None
                (On LUIS portal : endpoint URL )
    """
    # Mark the app as public so we can query it using any prediction endpoint
    client.apps.update_settings(app_id, is_public=True)
    
    responseEndpointInfo = client.apps.publish(
        app_id, 
        app_version,
        is_staging=False)

    print('Application published. Endpoint URL: ', 
          responseEndpointInfo.endpoint_url)


################# Create TEST utterances with valid format #################
############################################################################    
def create_test_utterance(intent, utterance, *labels):
    """LUIS expects a specifif data format for TEST data:
        this function creates these formatted utterances.
            Parameters:
                intent: the intent for which the utterances are associated
                utterance: a batch of utterances
                labels: 
                    - key/value pair for entities 
                    - key/value pair for char start position (startPos)
                    - key value pair for char end position (endPos)
            Outputs:
                the formatted data, including :
                    - text, intent, 
                    - a list of dictionary of entities and char's positions
    """

    text = utterance.lower()

    def label(name, value):
        value = value.lower()
        start = text.index(value)
        return dict(entity=name, startPos=start,
                    endPos=start + len(value))

    return dict(text=text, intent=intent,
                entities=[label(n, v) for (n, v) in labels])


############################ PREDICT with LUIS #############################
############################################################################
def predict(clientRuntime, CONFIG):
    """ Test LUIS prediction capabilities
    """
    request = {
        'query':'book a flight from Tunis to Toronto between 22 October 2021 to 5 November 2021, for a budget of $3500'
        }
    
    # The slot name parameter must be specified (staging or production)
    # For version 0.2.0, use "resolve" method
    # For version 0.7.0, use "get_slot_prediction" method
    response = clientRuntime.prediction.resolve(
        CONFIG.LUIS_APP_ID, query=request)

    text = response.query
    top_intent = response.top_scoring_intent.intent
    all_entities = response.entities
    
    return text, top_intent, all_entities