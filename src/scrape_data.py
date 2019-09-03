import bs4
import requests
import contextlib
import collections
import pandas as pd

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with contextlib.closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except requests.exceptions.RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
        
def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_soup(url):
    """
    Turns the html into a soup object.
    """
    raw_html = simple_get(url)
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    return soup



def create_df(soup_table, list_of_column_names):
    """
    Recreate the table the from the website.
    """
    # create the dataframe headers
    dict_of_values = collections.OrderedDict()
    adjusted_column_names = list_of_column_names[:5] \
        + ['Home/Away'] \
        + [list_of_column_names[6]] \
        + ['boxscore'] \
        + list_of_column_names[8:]
    
    for col_header in adjusted_column_names:
        dict_of_values[col_header] = []

    df = pd.DataFrame(dict_of_values)        

    # break out each record in the table
    appended_lines = []
    for row in soup_table.find_all('tr'):
        if len(row) == 14:
            appended_lines.append(row)
        else:
            pass # don't append the titles

    # for each record, extract text for each column
    for record in appended_lines:
        text_record = [col.text for col in record]
        df_record = pd.DataFrame([text_record], columns=adjusted_column_names)
        df = df.append(df_record)   

    return df

def get_first_table(url):
    """
    Gets the first table in the html doc.
    """
    soup = get_soup(url)
    return soup.table

def list_of_headers(soup_table):
    """
    Get the names in the header table.
    """
    list_of_cols = []
    header_line = soup_table.tr # get the first record
    for row in header_line.find_all('th'):
        list_of_cols.append(str(row.find(text=True)))
    return list_of_cols