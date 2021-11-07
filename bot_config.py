#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Bot Configuration"""

    ############## Azure Bot Service ###############
    PORT = 3978
    # APP_ID = os.environ.get("MicrosoftAppId", "") 
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_ID = os.environ.get("MicrosoftAppId", "f5f366ba-253d-4e54-b69d-a476d2ba57cf") 
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "QZIj3-W6IKOI>nG_1KxmG_MvjN12$.kg")

    ############## LUIS Service ###############
    LUIS_APP_ID = os.environ.get("LuisAppId", "afa9c5ea-2e07-4a91-b2a4-889813921718")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "b18763d5c96b48e1915efb6b93a635f2")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "https://ourflymeluis.cognitiveservices.azure.com/")

    ############## App Insights Service ###############
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "4973dc3b-6cd5-4057-88d0-c19c8d3ca08b")
