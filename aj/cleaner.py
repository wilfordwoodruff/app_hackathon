import pandas as pd
import re
import calendar
import numpy as np

def preprocess_df(path, chunk_size):
    
      df = pd.read_csv(path)

      df = (df
            .filter(['internal_id','text_only_transcript'])
            .sort_values(by=['internal_id'], ascending=True))

      #%% months and days
      months = list(calendar.month_name)[1:]
      short_months = [month[:4] for month in months]
      shorter_months = [month[:3] for month in months]

      allmonths = list(set(months).union(set(short_months)).union(set(shorter_months)))

      allmonths = sorted(allmonths, key=lambda x: len(x), reverse=True)

      days = list(calendar.day_name)
      days = sorted(days, key=lambda x: len(x), reverse=True)
      days = [x.lower() for x in days]

      #%%
      allmonths = '|'.join([x.lower() for x in allmonths])
      days = '|'.join([x.lower() for x in days])


      df = (df
            .assign(
                  text_only_transcript = (df.text_only_transcript
                        .str.replace('\[\[.*?\]\]', '', regex=True)
                        .str.replace('\r\n', ' ', regex=True)
                        .str.replace('[^a-zA-Z]', ' ')
                        .str.lower()
                        .str.replace(allmonths, '')
                        .str.replace(days, '')
                        .str.replace('br |th ', ' ')
                        .str.replace('\s+', ' ', regex=True))
                  )
            )
      
      df['chunks'] = df.apply(lambda x: chunk_string(chunk_size, x.text_only_transcript), axis=1)

      df = df.explode('chunks').drop('text_only_transcript', axis=1)

      df['word_count'] = df['chunks'].str.count(' ')

      df = df.dropna()

      return df

def chunk_string(chunk_size, my_string):
      if my_string is None:
            return None
      if pd.isnull(my_string):
            return None
      
      chunk_size = chunk_size+1

      words = my_string.split()    
      chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
      return chunks
