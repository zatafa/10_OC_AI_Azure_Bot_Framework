from luis_config import DefaultConfig
import utils.create_luis as cl

# Settings
CONFIG = DefaultConfig()

# Instantiate clients
print('Instantiate client(s)...')
print('---------------------------------------')
_, clientRuntime = cl.instantiate_client(CONFIG)
print()

# Predict
print('LUIS app prediction')
print('---------------------------------------')
text, top_intent, all_entities = cl.predict(clientRuntime, CONFIG)

print('Text: ', text)
print('Top Intent: ', top_intent)
for i in range(0, len(all_entities)):
    print(all_entities[i].type, ' : ', all_entities[i].entity)