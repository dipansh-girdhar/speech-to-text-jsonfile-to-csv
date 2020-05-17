import json
import pandas as pd 

def get_speech_text_list(speaker_labels, timestamps):
    '''
    Getting the speaker and the text associated with the speaker at that instant

    Parameters:
    ```````````
    speaker_labels:list[dict]
        List of speaker labels with confidence, final, from, speaker and to labels
    timestamps:list[list]
        List of text with word, from and to timestamps
    
    Returns:
    ````````
    speaker_list:list[list]
        list of list wth each inner list containing the speaker name(class) and the text at that timestamp
    '''
    speaker_list=[]
    for i in range(len(timestamps)):
        word=timestamps[i][0]
        if(speaker_labels[i]['from']==timestamps[i][1] and speaker_labels[i]['to']==timestamps[i][2]):
            speaker_list.append([speaker_labels[i]['speaker'],word])
    return speaker_list

def combine_speaker_sentences(speaker_list):
    '''
    combining the continuous text by a particular speaker and storing into a csv file

    Parameters:
    ```````````
    speaker_list:list[list]
        The speaker list returned from get_speech_text_list function

    Returns:
    ````````
    df:pandas.DataFrame object
        DataFrame containing speaker and text in step-by-step conversation    
    '''
    #converting the list[list] into a dataframe
    df=pd.DataFrame(speaker_list, columns=['Speaker', 'Text'])
    
    # Combining the continuous text columns by the same speaker
    df['key'] = (df['Speaker'] != df['Speaker'].shift(1)).astype(int).cumsum()
    df=pd.DataFrame(df.groupby(['key', 'Speaker'])['Text'].apply(' '.join))
    df.reset_index(inplace=True)
    df=df.drop(columns=['key'])
    
    return df

if __name__=="__main__":
    with open('speechToText.json', 'r') as f:
        speech_to_text=json.load(f)
    
    timestamps=speech_to_text['results'][0]['alternatives'][0]['timestamps']
    speaker_labels=speech_to_text['speaker_labels']

    speaker_list=get_speech_text_list(speaker_labels, timestamps)
    
    df=combine_speaker_sentences(speaker_list)
    #saving the df to csv file
    df.to_csv('speech_text.csv', index=False)