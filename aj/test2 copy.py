#%%
from sw_func import find_standardworks
from cleaner import preprocess_df
import polars as pl
import pandas as pd


df = (preprocess_df("../data/journals.csv", 15)
      .query("word_count > 10")
      .filter(['internal_id','chunks'])
      .rename({'chunks':'pieces'}, axis=1)
      ).tail(000).head(1000)

df = pl.DataFrame(df)

#%%
def detect_sw_matches(df):

    df = df.with_columns([
        pl.col("pieces")
        .apply(find_standardworks)
        .alias("things")
    ])

    df1 = pd.DataFrame(df).T.filter([0,1,2,3])

    df1.columns=['internal_id', 'text','temp']

    df1[['verse', 'probability']] = df1['temp'].apply(lambda x: pd.Series([x[0], x[1]]))

    df1 = df1.drop('temp', axis=1).sort_values(by=['probability'], ascending=False)

    return df1

df = detect_sw_matches(df)

#%%
df.to_csv('5last_1000.csv', index=False)
# %%
