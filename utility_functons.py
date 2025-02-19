from difflib import SequenceMatcher as SeqMatcher
import json
from random import shuffle


def split_seq(seq, NUMBER_OF_PROCESSES):
    '''Slices a sequence into NUMBER_OF_PROCESSES pieces of roughly the same size

    seq -- the original sequence to be split
    NUMBER_OF_PROCESSES -- the number of pieces to split seq into
    '''
    shuffle(seq)  # don't want newer/older years going to a single process
    num_files = len(seq)
    if num_files < NUMBER_OF_PROCESSES:
        NUMBER_OF_PROCESSES = num_files
    size = NUMBER_OF_PROCESSES
    newseq = []
    splitsize = 1.0 / size * num_files
    if NUMBER_OF_PROCESSES == 1:
        newseq.append(seq[0:])
        return newseq
    for i in range(size):
        newseq.append(seq[int(round(i * splitsize)):int(round((i + 1) * splitsize))])
    return newseq


def initialize_close_city_spelling(file_path):
    '''This uses a closure to return the get_zip3 function with its own copy
    of the CLOSE_CITY_SPELLINGS.  get_zip3 returns possible zip3s of a
    city-state combination, taking into account potential city mispellings,
    incorrect state/country abbreviations, and prior residencies.

    file_path -- the path to the CLOSE_CITY_SPELLINGS json file
    '''
    with open(file_path) as json_data:
        CLOSE_CITY_SPELLINGS = json.load(json_data)

    def get_zip3(in_state, in_city,
                 zip3_json, cleaned_cities_json, inventor_names_json=None,
                 last_name='', first_name='', middle_initial='',
                 flag=0):
        '''Attempts to find a zip3 from an applicant's city and state information.

        in_state -- the state to find the zip3 in
        in_city -- the city to find the zip3 for
        zip3_json -- the json file with city-state to zip3 mappings
        cleaned_cities_json -- the json file of standardized city names
        inventor_names_json -- the json file of inventor names and prior
            residencies (default None)
        last_name -- the inventor's last name (default '')
        first_name -- the inventor's first name (default '')
        middle_initial -- the inventor's middle name (default '')
        flag -- is for when we call this function again and avoid infinite recursion.
        inventor_names_json determines if this is assigning zip3s to an assignee
        or an inventor.
        '''
        nonlocal CLOSE_CITY_SPELLINGS
        if inventor_names_json:
            possible_zip3s = set()
        else:
            possible_zip3s = dict()
        possible_cities = [in_city]
        cleaned_cities = cleaned_cities_json.get(in_state)
        if cleaned_cities:
            for hold_city, spellings in cleaned_cities.items():
                if hold_city not in possible_cities:
                    if in_city[:20] in spellings:
                        possible_cities.append(hold_city)
        city_names = zip3_json.get(in_state)
        close_city_names = CLOSE_CITY_SPELLINGS.get(in_state)
        if close_city_names:
            close_city_names_keys = close_city_names.keys()
        else:
            close_city_names_keys = []
        for alias in possible_cities:
            if alias in close_city_names_keys:  # is the name ok?
                if inventor_names_json:
                    possible_zip3s.update(close_city_names[alias])
                else:
                    for zip3 in close_city_names[alias]:
                        possible_zip3s[zip3] = in_state
                continue
            if in_state not in CLOSE_CITY_SPELLINGS.keys():  # is this a real state?
                continue
            CLOSE_CITY_SPELLINGS[in_state][alias] = set()  # this isn't there
            if city_names:  # this may be a new misspelling, which we're going to check for now
                for city, zips in city_names.items():
                    str_match = SeqMatcher(None, alias, city)
                    if str_match.ratio() >= 0.9:  # good enough match
                        CLOSE_CITY_SPELLINGS[in_state][alias].update(zips)
                        if inventor_names_json:
                            possible_zip3s.update(zips)
                        else:
                            for zip3 in zips:
                                possible_zip3s[zip3] = in_state
        # If we couldn't find a zip3 we'll see if we can correct the city, state or country
        if not possible_zip3s and not flag:
            if inventor_names_json:
                try:
                    l_name = last_name[:20]
                    f_name = first_name[:15]
                    middle_initial = middle_initial[:0]
                    locations = inventor_names_json.get(l_name).get(f_name).get(middle_initial)
                except Exception:  # possible the name isn't in our JSON file
                    locations = []
                if locations:
                    for location in locations:
                        app_city = in_city[:20]
                        app_state = in_state
                        possible_city = location['city']
                        possible_state = location['state']
                        # Foreign national
                        if len(possible_state) == 3 and possible_state[2] == 'X':
                            continue
                        # We only allow the city OR the state to be incorrect.
                        # Otherwise we could be finding a different inventor with
                        # the same name with a relatively high probability.
                        # The state is wrong (seems to happen more often so it's first)
                        elif app_city == possible_city and app_state != possible_state:
                            app_state = possible_state
                        # The city is wrong (seems to happen less often so it's second)
                        elif app_city != possible_city and app_state == possible_state:
                            app_city = possible_city
                        # Nothing is wrong
                        else:
                            continue
                        hold_corrected_zip3 = get_zip3(app_state, app_city,
                                                       zip3_json, cleaned_cities_json, inventor_names_json,
                                                       flag=1)
                        possible_zip3s.update(hold_corrected_zip3)
            else:
                # Maybe the state is wrong so look for a matching city name
                states = zip3_json.keys()
                for state in states:
                    zips = zip3_json[state].get(in_city)
                    if zips:
                        for zip3 in zips:
                            possible_zip3s[zip3] = state
        return possible_zip3s
    return get_zip3
