
def clean(df):

    # Convert datatypes
    df = df.astype({
        'key_fifths': 'int32',
        'divisions': 'int32',
        'time_beats': 'int32',
        'time_type': 'int32',
        'measure': 'int32',
        'pitch_alter': 'int32',
        'pitch_octave': 'int32',
        'duration_length': 'int32'
    })



    return df