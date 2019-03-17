import pandas as pd
import numpy as np

from csearch.api_search.analyze_data_individual_data_optimized import get_self_citation_dictionary

# Extract parent publications from a given author CSV file; return the dictionary of publications
def extract_parents(filename):
    df = pd.read_csv(filename)

    subdf = df.loc[df['parent'] > 0][['id', 'title', 'name']]
    all_ids = subdf.groupby(['id']).count().reset_index()['id']

    dict = {}

    for id in all_ids:
        gg = subdf.loc[subdf['id'] == id][['title', 'name']].reset_index()
        gg2 = gg.iloc[0]
        rets = gg2['title']
        l = gg[['name']]
        l = str(list(l['name']))
        l = l[1:(len(l) - 1)]
        l = l.replace("'", "")

        dict[str(id)] = rets

    return dict

# Extract parent publications from a given publication CSV file; return the dictionary of publications
def pub_extract_parents(filename):
    df = pd.read_csv(filename)

    subdf = df.loc[df['parent'] > 0][['id', 'name']]
    all_ids = subdf.groupby(['id']).count().reset_index()['id']

    dict = {}

    for id in all_ids:
        gg = subdf.loc[subdf['id'] == id][['title', 'name']].reset_index()
        rets = str(id)
        l = gg[['name']]
        l = str(list(l['name']))
        l = l[1:(len(l) - 1)]
        l = l.replace("'", "")
        print("113")
        print(l)

        dict[str(id)] = rets# + "|||" + l

    return dict

# Extract layer 1 parent publications from a given author CSV file; return the dictionary of publications
def extract_inspected(filename):
    df = pd.read_csv(filename)

    subdf = df.loc[df['fb'] < 0][['id', 'title', 'name']]
    all_ids = subdf.groupby(['id']).count().reset_index()['id']

    dict = {}

    for id in all_ids:
        gg = subdf.loc[subdf['id'] == id][['title', 'name']].reset_index()
        gg2 = gg.iloc[0]
        rets = gg2['title']
        l = gg[['name']]
        l = str(list(l['name']))
        l = l[1:(len(l) - 1)]
        l = l.replace("'", "")
        print("113-67")
        print(l)

        dict[str(id)] = rets

    return dict

# Extract layer 1 parent publications from a given publication CSV file; return the dictionary of publications
def pub_extract_inspected(filename):
    df = pd.read_csv(filename)

    subdf = df.loc[df['fb'] < 0][['id', 'title', 'name']]
    all_ids = subdf.groupby(['id']).count().reset_index()['id']

    dict = {}

    for id in all_ids:
        gg = subdf.loc[subdf['id'] == id][['name']].reset_index()
        gg2 = gg.iloc[0]
        rets = str(id)
        l = gg[['name']]
        l = str(list(l['name']))
        l = l[1:(len(l) - 1)]
        l = l.replace("'", "")

        dict[str(id)] = rets

    return dict

# Backwards
def pub_extract_b_self(author, filename):
    return get_self_citation_dictionary(author, filename, False)

# Backwards
def extract_b_self(author, filename):
    return get_self_citation_dictionary(author, filename, True)

# Extract layer 1 parent publications from a given publication CSV file; return the dictionary of publications (forward)
def pub_extract_forward(filename):
    df = pd.read_csv(filename)

    subdf = df.loc[df['fb'] > 0][['id', 'name']]
    all_ids = subdf.groupby(['id']).count().reset_index()['id']

    dict = {}

    for id in all_ids:
        gg = subdf.loc[subdf['id'] == id][['title', 'name']].reset_index()
        gg2 = gg.iloc[0]
        rets = str(id)
        l = gg[['name']]
        l = str(list(l['name']))
        l = l[1:(len(l) - 1)]
        l = l.replace("'", "")

        dict[str(id)] = rets

    return dict

# Extract layer 1 parent publications from a given author CSV file; return the dictionary of publications (forward)
def extract_forward(filename):
    df = pd.read_csv(filename)

    subdf = df.loc[df['fb'] > 0][['id', 'title', 'name']]
    all_ids = subdf.groupby(['id']).count().reset_index()['id']

    dict = {}

    for id in all_ids:
        gg = subdf.loc[subdf['id'] == id][['title', 'name']].reset_index()
        gg2 = gg.iloc[0]
        rets = gg2['title']
        l = gg[['name']]
        l = str(list(l['name']))
        l = l[1:(len(l) - 1)]
        l = l.replace("'", "")

        dict[str(id)] = rets

    return dict