import requests
import pandas as pd
import numpy as np


def fetch_data():
    url = "https://api.github.com/search/repositories?q=stars:>50&per_page=100&page=1"
    res = requests.get(url)
    repos = res.json()
    df = pd.DataFrame()
    df = df.append(repos['items'])
    while 'next' in res.links.keys():
        res = requests.get(res.links['next']['url'])
        repos = res.json()
        try:
            df = df.append(repos['items'])
        except NameError:
            print('items not defined')

    return df

def preprocess(df):
    cols = ['forks_count', 'open_issues_count', 'size', 'description', 'language', 'license', 'has_issues', 'has_projects', 'has_wiki', 'name', 'stargazers_count']
    new_df = df[cols]
    new_df[['description', 'license']] = new_df[['description', 'license']].fillna(' ')
    new_df['language'].replace(np.nan, 'No-language', inplace=True)
    new_df['descWordCount'] = new_df['description'].apply(lambda x : len(x.split(' ')))
    new_df['nameCharCount'] = new_df['name'].apply(lambda x : len(x))
    new_df = new_df.drop(['description', 'name'], 1)
    new_df[['has_issues', 'has_projects', 'has_wiki']] = new_df[['has_issues', 'has_projects', 'has_wiki']].astype(int)

    lang_cols = np.array(new_df.language.value_counts()[:6].index)
    data = new_df
    data[lang_cols[0]] = data.language.apply(lambda x : int(x == 'JavaScript'))                  
    data[lang_cols[1]] = data.language.apply(lambda x : int(x == 'No-language'))                  
    data[lang_cols[2]] = data.language.apply(lambda x : int(x == 'Python'))                  
    data[lang_cols[3]] = data.language.apply(lambda x : int(x == 'TypeScript'))                  
    data[lang_cols[4]] = data.language.apply(lambda x : int(x == 'Go'))                  
    data[lang_cols[5]] = data.language.apply(lambda x : int(x == 'Java'))
    data['other_language'] = (data[lang_cols].sum(axis=1) == 0).astype(int)
    data = data.drop('language', 1)

    license_df = data['license'].apply(pd.Series)
    data['license-name'] = license_df['name']
    license_cols = ['mit_license','nan_license','apache_license','other_license','remain_license'] 
    for i in license_cols:
        if i.startswith('mit'):
            data[i] = data['license-name'].apply(lambda x: 1 if x == 'MIT License' else 0)
        elif i.startswith('nan'):
            data[i] = data['license-name'].apply(lambda x: int(x == 0))
        elif i.startswith('apache'):
            data[i] = data['license-name'].apply(lambda x: 1 if x == 'Apache License 2.0' else 0)
        elif i.startswith('other'):
             data[i] = data['license-name'].apply(lambda x: 1 if x == 'Other' else 0)  

    data['remain_license'] = (data[license_cols[:-1]].sum(axis=1) == 0).astype(int)
    data = data.drop(['license', 'license-name'], 1)

    return data

def write_file(data):
    data.to_csv('training_dataset.csv')

df = fetch_data()
df = preprocess(df)
write_file(df)
