import numpy as np
import pandas as pd

# Simply verifies whether an author is an author or co-author of a given publication, given a PubMed ID
def verify_author_of_id(author, id_to_find):
    global df

    # Group authors and IDs
    author_of = df.loc[df['id'] == id_to_find]
    parent_id_to_find = author_of.iloc[0]['parent']
    containsz_df = df.loc[df['id'] == parent_id_to_find][['name']]

    return len(containsz_df.loc[containsz_df['name'] == author]) > 0

# Returns a list of unique citation IDs that cite a given publication (in a given dataframe)
def papers_citing_id(given_id):
    global df

    # Group papers by parent; extract layer and ID
    paper_cited_by = df.loc[df['parent'] == given_id][['layer', 'id']]
    paper_cited_by_gb = paper_cited_by[paper_cited_by['layer'] > 0].groupby(['id']).count().reset_index()

    # return the grouped papers by ID
    return paper_cited_by_gb.iloc[:]['id']

# Returns the number of unique citation IDs that cite a given publication (in a given dataframe)
def number_of_papers_citing_id(given_id):
    return len(papers_citing_id(given_id))

# Finds the self-citation rate of a publication given a parent publication ID and a time constraint condition
def find_self_citation_percentage_from_parent_id(parent_id, condition='backwards'):
    global df

    # Filter publications that cite a given ID (child publications)
    cited_by = df.loc[df['parent'] == parent_id][['id', 'name', 'layer', 'fb']]
    cited_by = cited_by.loc[cited_by['layer'] > 0]

    # Applies a given condition filter if given a condition parameter
    if condition == 'backwards':
        cited_by = cited_by.loc[cited_by['fb'] < 0]  # Only looking backwards in time
    elif condition == 'forwards':
        cited_by = cited_by.loc[cited_by['fb'] > 0]  # Only looking backwards in time

    # Extracts a list of authors of the parent publication
    authors_of_parent_pub = df.loc[df['id'] == parent_id]['name']

    # Groups the references by PubMed ID
    cited_by_grouped = cited_by.groupby(['id'])

    # Counts the self-citation
    cited_count = 0

    # For each author of the parent citation, searches all references to
    for author in authors_of_parent_pub:
        bk = False
        # Loops through all citations in the grouped_citation table
        for cited_name_table in cited_by_grouped:
            for cited_name in cited_name_table[1]['name']:
                # Compares citation co-author names with names of each parent publication co-author
                if cited_name == author:
                    # If found, increments the self-citation count and breaks both inner loops
                    cited_count += 1
                    bk = True
                    break
            if bk:
                break

    # Returns the self-citation rate as a NumPy 32-bit float
    return np.float32(cited_count) / np.float32(cited_by[['id']].count())[0]

# Finds the self-citation rate of an author given their name and a time constraint condition
def find_self_citation_percentage_from_author(author, df, condition='backwards'):
    ref_df = df.loc[df['parent'] == 0]
    author_count = 0
    ref_df_grouped = ref_df.groupby(['id'])
    tab_list = [tab[1]['name'] for tab in ref_df_grouped]

    for tab in tab_list:
        for name in tab:
            if author in name: # length doesn't matter because spaces are sued as separators
                author_count += 1

    return np.float32(author_count) / np.float32(len(ref_df.groupby(['id']).count())), len(df.loc[df['layer'] == 0].groupby(['id']).count())


# Finds a self-citation rate given an author and a dataframe
def find_self_citation_percentage_from_author2(author, df, condition='backwards'):
    # Forward in time citations
    ref_df_forward = df.loc[df['fb'] > 0]

    # Backward in time citations
    ref_df = df.loc[df['fb'] < 0]

    # Author count tracker
    author_count = 0
    ref_df_grouped = ref_df.groupby(['id'])

    # Iterate through the dataframe based on each ID
    tab_list = [tab[1] for tab in ref_df_grouped]
    countindexfortab = 0
    sslistdf = {}
    for tab in tab_list:
        # Identify names
        for name in tab['name']:
            ln = len(name)
            try:
                if author in name:
                    author_count += 1
                    idtemp = list(tab['id'])[0]
                    titletemp = list(tab['title'])[0]
                    sslistdf[idtemp] = titletemp
                    #print(author_count)
            except Exception:
                pass
            countindexfortab += 1

    print("sslistdf", sslistdf)
    # Return a bunch of information including citation rate, total number of inspected citations, and total number of self-citations
    return np.float32(author_count) / np.float32(len(ref_df.groupby(['id']).count())), author_count, len(ref_df_grouped.count()), len(df.loc[df['layer'] == 0].groupby(['id']).count()),\
           len(ref_df_forward.groupby(['id']).count().reset_index()), ref_df, ref_df_forward, df.loc[df['fb'] == 0], sslistdf

# The same thing as above except only for forward citations
def find_self_citation_percentage_from_author2_forward(author, df):
    ref_df = df.loc[df['fb'] > 0]
    author_count = 0
    ref_df_grouped = ref_df.groupby(['id'])
    tab_list = [tab[1]['name'] for tab in ref_df_grouped]

    # Iterate through each ID in a grouped list
    for tab in tab_list:
        for name in tab:
            ln = len(name)
            try:
                if author in name:
                    author_count += 1
            except Exception:
                pass
    cc = len(ref_df.groupby(['id']).count())

    # Return a self-citation rate
    return np.float32(author_count) / np.float32(cc) if cc > 0 else 0

# Return a dictionary of self-citations
def get_self_citation_dictionary(author, file, b, condition='backwards'):
    if b: # If backwards
        df = pd.read_csv(file)

        ref_df = df.loc[df['fb'] < 0]
        ref_df_grouped = ref_df.groupby(['id'])

        dict = {}

        # Find all self-citations and add them to a dictionary mapped ID to title
        tab_list = [tab[1] for tab in ref_df_grouped]
        for tab in tab_list:
            for name in tab['name']:
                try:
                    if author in name:
                        title = tab['title'].unique()[0]
                        idd = tab['id'].unique()[0]
                        dict[str(idd)] = title
                except Exception:
                    pass

        return dict
    else: # If forwards
        df = pd.read_csv(file)

        ref_df = df.loc[df['fb'] < 0]
        ref_df_grouped = ref_df.groupby(['id'])

        dict = {}

        # Find all self-citations and add them to a dictionary mapped ID to ID
        tab_list = [tab[1] for tab in ref_df_grouped]
        for tab in tab_list:
            for name in tab['name']:
                try:
                    if author in name:
                        title = tab['id'].unique()[0]
                        idd = tab['id'].unique()[0]
                        dict[str(idd)] = title
                except Exception:
                    pass

        return dict

# Clean a dataframe except for certain IDs
def df_clean_exclude(keyzs, df):
    conditions = keyzs
    split = False
    if "," in keyzs:
        split = True
        conditions = keyzs.split(",")

    if not split:
        mdf = df[~df[['title']]['title'].str.contains(str(keyzs))]
        return mdf

# Converts an author name (given in the format "first_name last_name") to PubMed format
def format_author(word):
    to_return = word[(word.index(" ") + 1):] + " " + word[0]
    return to_return.lower()