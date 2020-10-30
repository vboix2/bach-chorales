import xml.etree.ElementTree as ET
import re
import pandas as pd
import constants as K
from os import listdir


def read_xml(file):
    """Read a musicxml file and returns a pandas dataframe"""

    # Parse file
    parsed_xml = ET.parse(file)
    root = parsed_xml.getroot()

    # Create dataframe
    df = pd.DataFrame(columns=K.XML_COLUMNS)

    # Title
    filename = file.split('/')[1]
    title = "BWV " + str(int(filename[:4]))

    # Part list
    part_list = {}
    for score_part in root.findall('./part-list/score-part'):
        id = score_part.attrib['id']
        part_name = score_part.find('./part-name').text
        part_list[id] = part_name

    del_keys = []
    for key in part_list.keys():
        if re.match('S\..*|Soprano.*' ,part_list[key]): part_list[key] = 'Soprano'
        if re.match('A\..*|Alto.*', part_list[key]): part_list[key] = 'Alto'
        if re.match('T\..*|Tenor.*', part_list[key]): part_list[key] = 'Tenor'
        if re.match('B\..*|Bass.*', part_list[key]): part_list[key] = 'Bass'

        if part_list[key] not in ['Soprano','Alto','Tenor','Bass']:
            del_keys.append(key)

    for i in range(len(del_keys)):
        del part_list[del_keys[i]]

    if len(part_list) > 4:
        return df

    # Parts
    for node_part in root.findall('./part'):
        part_key = node_part.attrib['id']
        if part_key not in part_list.keys(): continue
        part = part_list[part_key]

        # Key
        node_att = node_part.find('./measure/attributes')
        key_fifths = node_att.find('./key/fifths').text
        key_mode = node_att.find('./key/mode').text

        # Time
        divisions = node_att.find('./divisions').text
        time_beats = node_att.find('./time/beats').text
        time_type = node_att.find('./time/beat-type').text

        # Measures
        for node_measure in node_part.findall('./measure'):
            measure = node_measure.attrib['number']

            # Notes
            for node_note in node_measure.findall('note'):

                # Pitch
                pitch_step = 'rest'
                pitch_alter = '0'
                pitch_octave = '0'
                if ET.iselement(node_note.find('pitch')):
                    pitch_step = node_note.find('./pitch/step').text

                    if ET.iselement(node_note.find('./pitch/alter')):
                        pitch_alter = node_note.find('./pitch/alter').text

                    pitch_octave = node_note.find('./pitch/octave').text

                # Duration
                duration_length = node_note.find('duration').text
                duration_type = ''
                if ET.iselement(node_note.find('type')):
                    duration_type = node_note.find('type').text

                # tie
                tie = False
                if ET.iselement(node_note.find('tie')):
                    if node_note.find('tie').attrib['type'] == "start": tie = True

                # rest
                rest = False
                if ET.iselement(node_note.find('rest')):
                    rest = True

                # add values to dataframe
                row = {'title': title, 'part': part, 'key_fifths': key_fifths, 'key_mode': key_mode,
                        'divisions': divisions, 'time_beats': time_beats, 'time_type': time_type,
                        'measure': measure, 'pitch_step': pitch_step, 'pitch_alter': pitch_alter,
                        'pitch_octave': pitch_octave, 'duration_length': duration_length,
                        'duration_type': duration_type, 'is_tied': tie, 'is_rest': rest}
                df = df.append(row, ignore_index=True)

    return df

def read_files(path):
    """Read all XML files and return a dataframe"""

    df = pd.DataFrame(columns=K.XML_COLUMNS)

    for file in listdir(path):
        df = df.append(read_xml(path + "/" + file), ignore_index=True)

    return df
