# %%
#######################################
def chrome_urls_visited(History_file: str):
    """For a given 'History' database path for the Chrome browser, returns a pandas.DataFrame containing various information about visited URLs, along with human-readable timestamps.

    Examples:
        >>> results = chrome_urls_visited('History')\n
        >>> results[['url','last_visit_time','visit_count','visit_time']]\n
                                                        url            last_visit_time  visit_count                 visit_time\n
        0  https://www.google.com/search?q=best+python+se... 2021-11-11 11:20:40.781536            2 2021-11-11 11:20:39.598576\n
        1  https://www.google.com/search?q=best+python+se... 2021-11-11 11:20:40.781536            2 2021-11-11 11:20:40.781536\n
        2       https://www.udemy.com/topic/python-security/ 2021-11-11 11:21:13.023556            1 2021-11-11 11:21:13.023556\n
        3  https://www.sans.org/cyber-security-courses/au... 2021-11-11 11:21:16.156828            1 2021-11-11 11:21:16.156828\n
        4  https://www.sans.org/latest/cyber-security-cou... 2021-11-11 11:21:16.156828            1 2021-11-11 11:21:16.156828\n
        5  https://www.sans.org/cyber-security-courses/au... 2021-11-11 11:21:40.925808            3 2021-11-11 11:21:16.156828\n
        6  https://www.sans.org/cyber-security-courses/au... 2021-11-11 11:21:40.925808            3 2021-11-11 11:21:40.921122\n
        7  https://www.sans.org/cyber-security-courses/au... 2021-11-11 11:21:40.925808            3 2021-11-11 11:21:40.925808\n
        8  https://www.douglashollis.com/best-python-secu... 2021-11-11 11:22:34.307613            1 2021-11-11 11:22:34.307613\n

    References:
        # This revealed the numbers pertinent to converting the timestamps in Chrome sqlite database files:\n
        https://stackoverflow.com/questions/20458406/what-is-the-format-of-chromes-timestamps\n
        
        # Good information about Google Chrome forensics:\n
        https://www.sans.org/blog/google-chrome-forensics/

    Args:
        History_file (str): Reference the relative path of the 'History' file.
    """
    import sqlite3
    import pandas
    import datetime
#
    db_conn = sqlite3.connect(History_file)
    cursor = db_conn.execute("select urls.url, urls.title, urls.visit_count, urls.typed_count, urls.last_visit_time, urls.hidden, visits.visit_time, visits.from_visit, visits.transition FROM urls, visits where urls.id = visits.url;")
    columnheaders_urls_and_visits = list(map(lambda x:x[0], cursor.description))
    content_urls_and_visits = [e for e in cursor]
    results_df = pandas.DataFrame(content_urls_and_visits, columns=columnheaders_urls_and_visits)
#
    # modify the lvt column, changing the timestamp to one that is human-readable
    lvt_index = results_df.columns.get_loc('last_visit_time')
    lvt_content = results_df['last_visit_time']
    new_lvt_content = [datetime.datetime.fromtimestamp( (e / 1000000) -11644473600 ) for e in lvt_content]
    new_lvt_series = pandas.Series(new_lvt_content)
    new_lvt_series.name = 'last_visit_time'
#
    # remove the old lvt, and insert the new lvt
    # results_df.drop('last_visit_time', axis=1)
    throw_away = results_df.pop('last_visit_time')
    results_df.insert(lvt_index, new_lvt_series.name, new_lvt_series)
#
    # modify the vt column, changing the timestamp to one that is human-readable
    vt_index = results_df.columns.get_loc('visit_time')
    vt_content = results_df['visit_time']
    new_vt_content = [datetime.datetime.fromtimestamp( (e / 1000000) -11644473600 ) for e in vt_content]
    new_vt_series = pandas.Series(new_vt_content)
    new_vt_series.name = 'visit_time'
#
    # remove the old vt, and insert the new vt
    # results_df.drop('visit_time', axis=1)
    throw_away = results_df.pop('visit_time')
    results_df.insert(vt_index, new_vt_series.name, new_vt_series)    
#
    return results_df

