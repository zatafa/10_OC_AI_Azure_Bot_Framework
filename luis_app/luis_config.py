import os

class DefaultConfig:
    """ LUIS Configuration """

    # AUTHORING_KEY = os.environ.get('authoringKey', 'ADD_YOUR_AUTHORING_KEY_HERE')
    AUTHORING_KEY = os.environ.get('authoringKey', 'c148a6812d514f27ad28c14ff7dcb0e1')
    
    # AUTHORING_ENDPOINT = os.environ.get('authoringEndpoint', 'ADD_YOUR_AUTHORING_ENDPOINT_HERE')
    AUTHORING_ENDPOINT = os.environ.get('authoringEndpoint', 'https://ourflymeluis-authoring.cognitiveservices.azure.com/')
    
    # PREDICTION_KEY = os.environ.get('PredictionKey', 'ADD_YOUR_PREDICTION_KEY_HERE')
    PREDICTION_KEY = os.environ.get('PredictionKey', 'b18763d5c96b48e1915efb6b93a635f2')

    # PREDICTION_ENDPOINT = os.environ.get('predictionEndpoint', 'ADD_YOUR_PREDICTION_ENDPOINT_HERE')
    PREDICTION_ENDPOINT = os.environ.get('predictionEndpoint', 'https://ourflymeluis.cognitiveservices.azure.com/')

    # After the creation of the APP
    LUIS_APP_ID = os.environ.get("LuisAppId", "afa9c5ea-2e07-4a91-b2a4-889813921718")
    LUIS_SLOT_NAME = 'Production'