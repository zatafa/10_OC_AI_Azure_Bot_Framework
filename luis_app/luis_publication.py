from luis_config import DefaultConfig
import utils.create_luis as cl

# Settings
app_version = '0.1'
CONFIG = DefaultConfig()

# Instantiate clients
print('Instantiate client(s)...')
print('---------------------------------------')
client, _ = cl.instantiate_client(CONFIG)
print()

# Publish LUIS app
print ('Publishing application...')
print('---------------------------------------')
cl.publish_app(client, CONFIG.LUIS_APP_ID, app_version)
print()