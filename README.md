## Background
This contains Python 3 code that is used in multiple projects.
It was developed using the Anaconda distribution https://www.anaconda.com.

## Files
**inventor_info.py :**  
This deals with getting inventor information from the XML files.  
```
get_inventor_info(applicant, grant_year):  
	Get the basic information about and inventor from the XML files.  
	applicant -- the applicant on the XML file  
	grant_year -- the year the patent was granted in
```

**process_text.py :**  
This contains functions to clean up and standardized text taken from the XML files.
```
clean_patnum(patnum):
	Removes extraneous zero padding  
	patnum -- the original patent number
```
```
standardize_name(in_str):  
	This cleans and standardizes strings, removing HTML and URL encodings.  
	It keeps any UTF8 chracters and numbers and replaces all whitespace  
	with a single space.  The returned string is not necessarily ASCII.  
	in_str -- the original string
```
```
standardize_name_late_of(in_str):  
    Remove the "LATE OF" from a string  
    in_str -- the original string  
```
```
clean_up_inventor_name(applicant, xml_path):  
    Cleans up the inventor names  
    applicant -- the applicant on the XML document  
    xml_path -- the XML path to the applicant  
```
```
standardize_name_cdp(in_str):  
    Standardizes the name of a Census Designated Place  
    in_str -- the original string  
```
```
split_first_name(in_name):  
    Get middle name out of first name of an inventor  
    in_name -- the original name from the XML document  
```
```
split_name_suffix(in_name):  
    Takes the suffix off the last name of an inventor  
    in_name -- the original name from the XML document  
```
```
get_assignee_info(assignee, xml_path):  
    Returns a standardized assignee name  
    assignee -- the assignee on an XML patent  
    xml_path -- the path to the assignee name  
```

**utility_functions.py :**  
This is a collection of general reused functions.  
```
split_seq(seq, NUMBER_OF_PROCESSES):  
    Slices a sequence into NUMBER_OF_PROCESSES pieces of roughly the same size  
    seq -- the original sequence to be split  
    NUMBER_OF_PROCESSES -- the number of pieces to split seq into  
```
```
initialize_close_city_spelling(file_path):  
	This uses a closure to return the get_zip3 function with its own copy  
    of the CLOSE_CITY_SPELLINGS.  get_zip3 returns possible zip3s of a  
    city-state combination, taking into account potential city mispellings,  
    incorrect state/country abbreviations, and prior residencies.  
    file_path -- the path to the CLOSE_CITY_SPELLINGS json file  

    get_zip3(in_state, in_city,  
                 zip3_json, cleaned_cities_json, inventor_names_json=None,  
                 last_name='', first_name='', middle_initial='',  
                 flag=0):  
        Attempts to find a zip3 from an applicant's city and state information.  
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
```