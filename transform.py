import works
import constants as K
from os import path
import pandas as pd


def process(df):

    # Title column
    if path.exists('csv/bach_works.csv'):
        works_df = pd.read_csv('csv/bach_works.csv')
    else:
        works_df = works.get_works()
        works_df.to_csv('csv/bach_works.csv', index=False)
    df = pd.merge(df, works_df, how='left', on='bwv')

    # Work column
    df['work'] = 'BWV ' + df['bwv'] + ". " + df['title']

    # Key column
    def get_key(row):
        if row['key_mode'] == 'major':
            idx = row['key_fifths'] + 8
            key = K.FIFTHS[idx]
        else:
            idx = row['key_fifths'] + 11
            key = K.FIFTHS[idx]
        return key

    df['key_pitch'] = df.apply(get_key, axis=1)

    # Tone column
    def get_tone(row):
        tone = (row['pitch_octave'] + 1) * 12 + K.STEP_MAP[row['pitch_step']] + row['pitch_alter']
        return tone

    df['pitch_tone'] = df.apply(get_tone, axis=1)

    # Pitch step
    def get_step(row):
        step = row['pitch_step'] + K.ALTER_MAP[row['pitch_alter']]
        return step

    df['pitch_step'] = df.apply(get_step, axis=1)

    return df