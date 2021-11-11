# %%
#######################################
def firefox_urls_visited(places_sqlite: str):
    """For a given 'places.sqlite' database path for the Firefox browser, returns a pandas.DataFrame containing the human-readable 'last_visit_date', 'visi_count', and 'url'.

    Examples:
        >>> results = firefox_urls_visited('places.sqlite')\n
        >>> results.head()\n
                    last_visit_date  visit_count                                                url\n
        0 2021-05-15 09:01:10.772497            1                               http://www.sans.org/\n
        1 2021-05-15 09:01:10.871628            1                              https://www.sans.org/\n
        2 2021-05-15 09:01:14.508394            1                 https://www.sans.org/account/login\n
        3 2021-05-15 09:01:33.163270            2              https://www.sans.org/account/loginsso\n
        4 2021-05-15 09:01:15.093349            1  https://idp.sans.org/simplesaml/saml2/idp/SSOS...\n

    References:
        # Good reference for what .sqlite files contain various artifacts\n
        https://www.foxtonforensics.com/browser-history-examiner/firefox-history-location\n
        
        # Helpful in showings ways to change column position\n
        https://sparkbyexamples.com/pandas/pandas-change-position-of-a-column/\n
        
        # Some good info and testing, I got the idea of using list comps from here\n
        https://towardsdatascience.com/apply-function-to-pandas-dataframe-rows-76df74165ee\n
        
        # Good info on assignment and the SettingWithCopyWarning\n
        https://realpython.com/pandas-settingwithcopywarning/\n

    Args:
        places_sqlite (str): Reference the relative path of the 'places.sqlite' file.

    Returns:
        pandas.DataFrame: Returns a DataFrame.
    """
    import pandas
    import datetime
    import sqlite3
    
    db_conn = sqlite3.connect(places_sqlite)
    table_name = 'moz_places'
    cursor = db_conn.execute(f"select * from '{table_name}';")
    column_headers = list(map(lambda x:x[0], cursor.description))
    row_contents = [e for e in cursor]
    data_frame = pandas.DataFrame(row_contents, columns=column_headers)
    listcomp_last_visit_date = [ datetime.datetime.fromtimestamp(x / 1000000) for x in data_frame['last_visit_date'] ]
    temp_series = pandas.Series(listcomp_last_visit_date)
    temp_series.name = 'last_visit_date'
    new_df = data_frame[['visit_count','url']]
    new_df.insert(0, temp_series.name, temp_series)
    return new_df

