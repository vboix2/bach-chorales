# Read dataframe
XML_COLUMNS = [
    'bwv',
    'part',
    'key_fifths',
    'key_mode',
    'divisions',
    'time_beats',
    'time_type',
    'measure',
    'is_implicit',
    'pitch_step',
    'pitch_alter',
    'pitch_octave',
    'duration_length',
    'duration_type',
    'is_tied',
    'is_rest'
]

# Transform
FIFTHS = ['Fb','Cb','Gb','Db','Ab','Eb','Bb',
          'F','C','G','D','A','E','B',
          'F#','C#','G#','D#','A#','E#','B#']
STEP_MAP = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11, 'rest':0}
ALTER_MAP = {-2: 'bb', -1: 'b', 0: '', 1: '#', 2:'##'}

# Column groups
WORK_COLS = ['bwv','title','work']
KEY_COLS = ['key_fifths','key_pitch','key_mode']
METRE_COLS = ['time_beats','time_type', 'metre']
PITCH_COLS = ['pitch_octave','pitch_tone','pitch_step','pitch_alter']
TIME_COLS = ['measure','beat']
DURATION_COLS = ['duration_length','is_tied']


COLUMNS = [WORK_COLS, KEY_COLS, PITCH_COLS]