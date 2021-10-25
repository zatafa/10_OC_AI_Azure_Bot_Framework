#  Import the libraries
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

def load_and_transform_data(data_path):
    """ Import the Frames JSON file:
        1) extract the 1st input of the user;
        2) filter only on the expected 5 items to track;
        3) clean the data (bad values and duplicates).
    """
    
    # Load the JSON file as a Pandas DataFrame
    df = pd.read_json(data_path)

    # Create an empty list to save the result
    result = []

    # Iterate on rows
    for turns in df['turns']:
        # Create an empty dictionary
        new_row = {}

        # Update the dictionary with the 1st input of the user
        new_row.update({'text':turns[0].get('text')})
    
        # Filter on labels > acts for each user's text
        for element in turns[0].get('labels').get('acts'):
        
            # Filter on args in labels > acts
            for item in element.get('args'):
          
                # Retrieve all key/value pairs
                new_row.update({item.get('key'):item.get('val')})

        result.append(new_row)

    # Convert the list to DataFrame 
    final_df= pd.DataFrame.from_records(result)

    # Keep only useful columns
    final_df = final_df[['text', 'or_city', 'dst_city', 'str_date', 'end_date', 'budget']]
    
    # Check char length in 'Text' column
    # LUIS has limitation of char length for utterances: <500
    char_count = final_df['text'].str.len()
    print('Char Length --> Min: {} / Max: {}'.format(char_count.min(), char_count.max()))

    # Replace all -1 value by NaN value
    final_df = final_df.replace('-1', np.NaN)
    
    # Drop duplicate values
    final_df = final_df.drop_duplicates()

    # Create DF for BookFlight intent
    bookflight_df =  final_df[~(
        final_df.or_city.isna() &
        final_df.dst_city.isna() &
        final_df.str_date.isna() &
        final_df.end_date.isna() &
        final_df.budget.isna())]

    # Display shape and 5 first rows
    print('DataFrame shape', bookflight_df.shape)
    # bookflight_df.head()

    return bookflight_df


def train_test_data(bookflight_df):
    """ Create train and test sets
    """
    split_df, prod_df = train_test_split(
        bookflight_df,
        test_size=24,
        random_state=42)
    
    train_df, test_df = train_test_split(
        split_df,
        test_size=200,
        random_state=42)


    # Save to CSV
    train_df.to_csv('luis_app/data/train_df.csv', index=None)
    test_df.to_csv('luis_app/data/test_df.csv', index=None)
    prod_df.to_csv('luis_app/data/prod_df.csv', index=None)

    return train_df, test_df