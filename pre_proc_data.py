# This file should prepare the data by splitting it into first and second halfs, removing noise, and shortening it
# down to a manageable size for efficiency.
from xml.dom import minidom as mdom
import pandas as pd


def get_attr_value(ele, attr):
    return ele.attributes[attr].value


def split_halves(metadata_filename):
    """
    extracts metadata of game from a provided file and returns the details in a dictionary
    :param metadata_filename: the metadata file given with the game data
    :return: 3 dictionaries: pitch, which is the size details of the game pitch; first_half and second half,
    which gives the frames of the start and end of the first and second half, respectively
    """

    print("Splitting into first and second halves")
    metadata = mdom.parse(metadata_filename)

    # Finding the size of the pitch
    match = metadata.getElementsByTagName('match')[0]
    pitch = {'x': float(get_attr_value(match, 'fPitchXSizeMeters')),
             'y': float(get_attr_value(match, 'fPitchYSizeMeters'))}

    # finding the beginning and end frames of the first + second half
    first = metadata.getElementsByTagName('period')[0]
    second = metadata.getElementsByTagName('period')[1]

    first_half = {'start': int(get_attr_value(first, 'iStartFrame')), 'end': int(get_attr_value(first, 'iEndFrame'))}
    second_half = {'start': int(get_attr_value(second, 'iStartFrame')), 'end': int(get_attr_value(second, 'iEndFrame'))}

    return [pitch, first_half, second_half]


pitch, first_half, second_half = split_halves('data/metadata/metadata.xml')
print(first_half, second_half)


def eliminate_noise(half1, half2, datafile):
    """
    Produces a new .dat file with only active play (i.e. play during the first and second half)
    :param half1: extracted metadata about the first half
    :param half2: extracted metadata about the second half
    :param datafile: .dat file to be cleaned
    :return: name of the new file produced
    """
    half1_start = half1['start']
    half1_end = half1['end']
    half2_start = half2['start']
    half2_end = half2['end']

    print(half1_start, half1_end)
    with open(datafile, "r") as input_file:
        with open("data/gamedata/in_play.dat", "w") as output_file:
            start_processing = False
            for line in input_file:
                # get the frame number and cast to an int to compare
                frame = int(line.strip().split(":")[0])

                # print(frame, start_processing)
                if not start_processing:
                    # check if the target column has the target value
                    if frame == half1_start or \
                            frame == half2_start:
                        start_processing = True
                        output_file.write(line)
                # check if the frame is an end frame and stop processing if so
                elif frame == half1_end or \
                        frame == half2_end:
                    start_processing = False
                else:
                    # write the line to the new file
                    output_file.write(line)

    return output_file.name


def shorten_data(seconds, filename):
    """
    produces a new data file which only contains every x seconds the user specifies
    :param seconds: seconds per data capture. NB: this parameter refers to real seconds, NOT frames
    :param filename: name of the file to shorten down
    :return: the name of the new file produced
    """
    # 25 frames per second:
    n = seconds * 25

    with open(filename, "r") as file:
        with open("data/gamedata/short_data.dat", "w") as newfile:
            shortened_data = []
            for i, line in enumerate(file):
                if i % n == 0:
                    newfile.write(line)

    return newfile.name


def categorize_data(filename):
    """
    splits the data into two CSV files: players and ball
    :param filename: the name of the file to categorize
    :return: void
    """
    player_data = []
    ball_data = []

    with open(filename, 'r') as file:
        for i in file:
            # create frame num, list of players, and ball details
            frame_num = i.split(':')[0]
            players = i.split(':')[1].split(';')
            ball = i.split(':')[2].split(',')

            # add frame details to ball data and add to list
            ball_frame = [frame_num, ball[0], ball[1], ball[2], ball[3], ball[4], ball[5].strip(';')]
            ball_data.append(ball_frame)

            # add frame details to each player and add them to list
            for j in players:
                data = j.split(',')
                if len(data) > 1:
                    player_frame = [frame_num, data[0], data[1], data[2], data[3], data[4], data[5]]
                    player_data.append(player_frame)

    # add ball to CSV
    ball_df = pd.DataFrame(ball_data, columns=['frame_num', 'x', 'y', 'z', 'speed', 'poss', 'inPlay'])
    print(ball_df.head())
    ball_df.to_csv('./data/ball.csv/ball_df.csv')

    # add players to CSV
    player_df = pd.DataFrame(player_data, columns=['frame_num', 'team_id', 'player_id', 'squadNum', 'x', 'y', 'speed'])
    print(player_df.head())
    player_df.to_csv('./data/player.csv/player_df.csv')


# clean up file
categorize_data(shorten_data(5, eliminate_noise(first_half, second_half, 'data/gamedata/987601.dat')))
