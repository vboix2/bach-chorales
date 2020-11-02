import works
import constants as K
import pandas as pd
from os import path


def clean(df):

    # Title
    works_df = works.get_works()
    df = pd.merge(df, works_df, how='left', on='bwv')

    # Work
    df['work'] = 'BWV ' + df['bwv'] + ". " + df['title']

    # Key
    def get_key(row):
        if row['key_mode'] == 'major':
            idx = row['key_fifths'] + 8
            key = K.FIFTHS[idx]
        else:
            idx = row['key_fifths'] + 11
            key = K.FIFTHS[idx]
        return key

    df['key_pitch'] = df.apply(get_key, axis=1)

    # Metre
    df['metre'] = df.apply(lambda x: str(x['time_beats']) + "/" + str(x['time_type']), axis=1)

    # Tone
    def get_tone(row):
        tone = (row['pitch_octave'] + 1) * 12 + K.STEP_MAP[row['pitch_step']] + row['pitch_alter']
        return tone

    df['pitch_tone'] = df.apply(get_tone, axis=1)

    # Pitch step
    def get_step(row):
        step = row['pitch_step'] + K.ALTER_MAP[row['pitch_alter']]
        return step

    df['pitch_step'] = df.apply(get_step, axis=1)

    # Duration
    df['duration'] = df['duration_length'] * 12 / df['divisions']

    #Time
    df['time'] = 0
    for w in df.bwv.unique():
        for p in ['Soprano','Alto','Tenor','Bass']:
            idxs = df.query('bwv==@w and part==@p').index
            first_idx = min(idxs)
            last_idx = max(idxs)
            time = 0
            for i in range(first_idx, last_idx + 1):
                df.loc[df.index==i,'time'] = time
                time += df.loc[df.index==i,'duration'].item()

        first_measure_time = min(df.query('bwv==@w and measure==1').time)
        df.loc[df.bwv==w,'time'] = df.loc[df.bwv==w,'time'] - first_measure_time

    # Measure time
    df['measure_time'] = df['time'] - (df['measure'] - 1) * df['time_beats'] * 12


    return df


def process(df):

    if path.exists('csv/chorales_clean.csv'):
        df = pd.read_csv('csv/chorales_clean.csv', dtype={'bwv': object})
    else:
        df = clean(df)
        df.to_csv('csv/chorales_clean.csv', index=False)