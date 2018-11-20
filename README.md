## Background
This contains Python 3 code that is used in multiple projects.
It was developed using the Anaconda distribution https://www.anaconda.com.

## Files
**inventor_info.py :**  
>get_inventor_info(applicant, grant_year):  
Get the basic information about and inventor from the XML files.  
applicant -- the applicant on the XML file  
grant_year -- the year the patent was granted in

**process_text.py :**  
>clean_patnum(patnum):
Removes extraneous zero padding  
patnum -- the original patent number  
>standardize_name(in_str):  
This cleans and standardizes strings, removing HTML and URL encodings.  
It keeps any UTF8 chracters and numbers and replaces all whitespace  
with a single space.  The returned string is not necessarily ASCII.  
in_str -- the original string  