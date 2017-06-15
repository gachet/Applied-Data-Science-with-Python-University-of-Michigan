states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    import re
    import pandas as pd

    # Open the file, read the lines, and close the file
    fo = open('university_towns.txt', "r")
    lines = fo.readlines()
    fo.close()

    # remove empty lines
    new_lines = []
    for line in lines:
        if not re.match(r'^\s*$', line):
            new_lines.append(line)

    lines = new_lines.copy()

    # Strip the white space at the beginning and end of each line
    for index, line in enumerate(lines):
        lines[index] = line.strip()

        # Loop through the lines to form a dataframe
    df_result = pd.DataFrame(columns=('State', 'RegionName'))
    i = 0  # counter for each new line in the dataframe
    state_string = ""  # Empty initial state string
    for line in lines:
        if '[edit]' in line:
            state_string = line.replace('[edit]', "")
        else:
            region_string = re.sub(r' \(.*', "", line)
            df_result.loc[i] = [state_string, region_string]
            i += 1
    return df_result


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''

    import pandas as pd
    df_gdp = pd.read_excel('gdplev.xls', skiprows=220, parse_cols='E,G', header=None)
    df_gdp.columns = ['quarter', 'GDP']

    for i in range(4, len(df_gdp)):
        if (df_gdp.loc[i - 4, 'GDP'] > df_gdp.loc[i - 3, 'GDP']) \
                and (df_gdp.loc[i - 3, 'GDP'] > df_gdp.loc[i - 2, 'GDP']) \
                and (df_gdp.loc[i - 2, 'GDP'] < df_gdp.loc[i - 1, 'GDP']) \
                and (df_gdp.loc[i - 1, 'GDP'] < df_gdp.loc[i, 'GDP']):
            recession_base_idx = i - 4

    result = df_gdp.loc[recession_base_idx, 'quarter']
    j = recession_base_idx
    while True:
        if df_gdp.loc[j - 1, 'GDP'] > df_gdp.loc[j, 'GDP']:
            j -= 1
        else:
            result = df_gdp.loc[j + 1, 'quarter']
            break

    return result


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''

    import pandas as pd
    df_gdp = pd.read_excel('gdplev.xls', skiprows=220, parse_cols='E,G', header=None)
    df_gdp.columns = ['quarter', 'GDP']

    for i in range(4, len(df_gdp)):
        if (df_gdp.loc[i-4, 'GDP'] > df_gdp.loc[i-3, 'GDP']) \
                and (df_gdp.loc[i-3, 'GDP'] > df_gdp.loc[i-2, 'GDP']) \
                and (df_gdp.loc[i-2, 'GDP'] < df_gdp.loc[i-1, 'GDP']) \
                and (df_gdp.loc[i-1, 'GDP'] < df_gdp.loc[i, 'GDP']):
            result = df_gdp.loc[i, 'quarter']

    return result


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''

    import pandas as pd
    df_gdp = pd.read_excel('gdplev.xls', skiprows=220, parse_cols='E,G', header=None)
    df_gdp.columns = ['quarter', 'GDP']

    for i in range(4, len(df_gdp)):
        if (df_gdp.loc[i-4, 'GDP'] > df_gdp.loc[i-3, 'GDP']) \
                and (df_gdp.loc[i-3, 'GDP'] > df_gdp.loc[i-2, 'GDP']) \
                and (df_gdp.loc[i-2, 'GDP'] < df_gdp.loc[i-1, 'GDP']) \
                and (df_gdp.loc[i-1, 'GDP'] < df_gdp.loc[i, 'GDP']):
            result = df_gdp.loc[i-2, 'quarter']

    return result


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''

    import pandas as pd
    import numpy as np
    df = pd.read_csv('City_Zhvi_AllHomes.csv', header=0)

    # Create columns to keep
    cols_to_keep = ['RegionID', 'RegionName', 'State']
    for i in range(2000, 2017):
        for j in range(1, 13):
            if j <= 9:
                if i == 2016 and j == 9:
                    pass
                else:
                    month_str = '0' + str(j)
            else:
                if i == 2016:
                    pass
                else:
                    month_str = str(j)
            cols_to_keep.append(str(i) + '-' + month_str)
    df = df[cols_to_keep]

    # Convert two letter state abbreviations to state names
    df['State'] = df['State'].replace(states)

    def convert_to_qtr(ym):
        year, month = ym.split('-')
        if month == '01' or month == '02' or month == '03':
            result = year + 'q1'
        elif month == '04' or month == '05' or month == '06':
            result = year + 'q2'
        elif month == '07' or month == '08' or month == '09':
            result = year + 'q3'
        else:
            result = year + 'q4'
        return result

    # Stack the columns of GDP values and add a quarter column
    df_compiled = df.copy().set_index(['State', 'RegionName', 'RegionID']).stack(dropna=False)
    df_compiled = df_compiled.reset_index().rename(columns={'level_3': 'year_month', 0: 'gdp'})
    df_compiled.drop_duplicates(inplace=True)
    df_compiled['quarter'] = df_compiled['year_month'].apply(convert_to_qtr)
    df_compiled = df_compiled.drop('year_month', axis=1)
    result = df_compiled.pivot_table(values='gdp', index=['State', 'RegionName', 'RegionID'], columns='quarter',
                                     aggfunc=np.mean)
    result = result.reset_index()
    result = result.drop('RegionID', axis=1)
    # del result.index.name
    result = result.set_index(['State', 'RegionName'])
    return result


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    import pandas as pd
    import numpy as np
    from scipy.stats import ttest_ind

    univ_towns = get_list_of_university_towns()
    univ_towns['univ_town'] = True

    # merge the housing data with university town DataFrames
    df = pd.merge(convert_housing_data_to_quarters(), univ_towns, how='outer', left_index=True, right_on=['State', 'RegionName'])
    df['univ_town'] = df['univ_town'].replace({np.NaN: False})

    # Get the recession quarters
    recession_start = get_recession_start()
    recession_bottom = get_recession_bottom()

    # Parse the year and quarter of the recession quarters
    year_recession_start = int(recession_start[0:4])
    qtr_recession_start = int(recession_start[-1])
    year_recession_bottom = int(recession_bottom[0:4])
    qtr_recession_bottom = int(recession_bottom[-1])

    # get the columns to keep in the merged DataFrame
    cols_to_keep = ['State', 'RegionName', 'univ_town']
    qtrs_to_keep = []
    for i in range(year_recession_start, year_recession_bottom+1):
        for j in range(1, 5):
            if (i == year_recession_start and j < qtr_recession_start)\
                    or (i == year_recession_bottom and j > qtr_recession_bottom):
                pass
            else:
                qtrs_to_keep.append(str(i) + 'q' + str(j))
    df = df[cols_to_keep + qtrs_to_keep]

    # Compute the price_ratio
    df['price_ratio'] = df[recession_bottom] - df[recession_start]

    # t-test to determine if there is a difference between university and non-university towns
    univ_town_price_ratio = df[df['univ_town'] == True]['price_ratio']
    non_univ_town_price_ratio = df[df['univ_town'] == False]['price_ratio']
    st, p = ttest_ind(univ_town_price_ratio, non_univ_town_price_ratio, nan_policy='omit',)

    # get different and better values
    different = False
    if p <0.01:
        different = True

    # determine which type of town is better
    better = ""
    if univ_town_price_ratio.mean() > non_univ_town_price_ratio.mean():
        better = "university town"
    else:
        better = "non-university town"

    return different, p, better

print(run_ttest())