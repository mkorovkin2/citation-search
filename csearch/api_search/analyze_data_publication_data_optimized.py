import pandas as pd
import numpy as np

# Return the self-citation rate of a publication
def publication_score(df):

    # Dataframe of non-parent citations
    fdf = df.loc[df['layer'] > 0]

    # Grouped dataframe of IDs
    dgb = fdf.groupby(['id'])

    author_names = np.array(df.loc[df['layer'] == 0]['name'])
    author_repeat_count = 0

    # Iterate through table, finding self-citations
    for tab in dgb:
        names = tab[1]['name']
        for name in names:
            bk = False
            for aa in author_names:
                if name in aa:
                    author_repeat_count += 1
                    bk = True
                    break
            if bk:
                break


    num_pubs = np.float32(len(dgb.count()))

    prop = np.float32(author_repeat_count) / num_pubs

    # Return self-citation rate and related statistics
    return prop, num_pubs, len(fdf.loc[fdf['fb'] == 1].groupby(['id']).count().reset_index())

def publication_score_bavkwards(df):
    fdf = df.loc[df['layer'] < 0]
    dgb = fdf.groupby(['id'])

    # Extract only author names and format them as an array for verification
    author_names = np.array(df.loc[df['layer'] == 0]['name'])
    author_repeat_count = 0

    # Iterate through grouped papers and compare with current authors
    for tab in dgb:
        names = tab[1]['name']
        for name in names:
            bk = False
            for aa in author_names:
                if name in aa:
                    author_repeat_count += 1
                    bk = True
                    break
            if bk:
                break

    # Return statistics on the extraction
    num_pubs = np.float32(len(dgb.count()))
    prop = np.float32(author_repeat_count) / num_pubs

    # Return self-citation proportion, number of self-citing publications, number of total publications inspected
    return prop, num_pubs, len(fdf.loc[fdf['fb'] == 1].groupby(['id']).count().reset_index())

# Score self-citation rate on a given publication
def publication_score2(df):
    # Backward in time dataframe
    fdf = df.loc[df['fb'] < 0]

    # Grouped dataframe
    dgb = fdf.groupby(['id'])

    author_names = np.array(df.loc[df['layer'] == 0]['name'])
    author_repeat_count = 0

    # Iterate through the table and identify self-citations
    remove_list = list()
    for tab in dgb:
        names = tab[1]['name']
        for name in names:
            bk = False
            for aa in author_names:
                if name in aa:
                    author_repeat_count += 1
                    bk = True
                    break
            if bk:
                break

    num_pubs = np.float32(len(dgb.count()))

    prop = np.float32(author_repeat_count) / num_pubs

    # Return self-citation proportion, number of self-citing publications, number of total publications inspected,
    # the author repeat count, and the forward-looking dataframe
    return prop, num_pubs, len(fdf.loc[fdf['fb'] == 1].groupby(['id']).count().reset_index()), author_repeat_count, fdf

# Score the forward self-citation rate of a given publication
def publication_score2_f(df):
    # Forward self-citation dataframe
    fdf = df.loc[df['fb'] > 0]

    # Dataframe grouped by ID
    dgb = fdf.groupby(['id'])

    author_names = np.array(df.loc[df['layer'] == 0]['name'])
    author_repeat_count = 0

    # Iterate through the table looking for self-citations
    for tab in dgb:
        names = tab[1]['name']
        for name in names:
            bk = False
            for aa in author_names:
                if name in aa:
                    author_repeat_count += 1
                    bk = True
                    break
            if bk:
                break


    num_pubs = np.float32(len(dgb.count()))

    prop = np.float32(author_repeat_count) / num_pubs

    # Return self-citation proportion, number of self-citing publications, number of total publications inspected,
    # the author repeat count, and the forward-looking dataframe
    return prop, num_pubs, len(fdf.loc[fdf['fb'] == 1].groupby(['id']).count().reset_index()), author_repeat_count, fdf