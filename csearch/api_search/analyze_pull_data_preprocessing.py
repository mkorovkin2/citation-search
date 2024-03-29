import numpy as np
import pandas as pd

# Simply verifies whether an author is an author or co-author of a given publication, given a PubMed ID
def verify_author_of_id(author, id_to_find):
    global df

    author_of = df.loc[df['id'] == id_to_find]
    parent_id_to_find = author_of.iloc[0]['parent']
    containsz_df = df.loc[df['id'] == parent_id_to_find][['name']]

    return len(containsz_df.loc[containsz_df['name'] == author]) > 0

# Returns a list of unique citation IDs that cite a given publication (in a given dataframe)
def papers_citing_id(given_id):
    global df

    paper_cited_by = df.loc[df['parent'] == given_id][['layer', 'id']]
    paper_cited_by_gb = paper_cited_by[paper_cited_by['layer'] > 0].groupby(['id']).count().reset_index()

    return paper_cited_by_gb.iloc[:]['id']

# Returns the number of unique citation IDs that cite a given publication (in a given dataframe)
def number_of_papers_citing_id(given_id):
    return len(papers_citing_id(given_id))

# Finds the self-citation rate of a publication given a parent publication ID and a time constraint condition
def find_self_citation_percentage_from_parent_id(parent_id, df, condition='backwards'):
    total_inspected = 0

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
        author = author.encode('utf-8')
        bk = False
        # Loops through all citations in the grouped_citation table
        for cited_name_table in cited_by_grouped:
            total_inspected += 1
            for cited_name in cited_name_table[1]['name']:
                # Compares citation co-author names with names of each parent publication co-author
                cited_name = cited_name.encode('utf-8')
                if cited_name == author:
                    # If found, increments the self-citation count and breaks both inner loops
                    cited_count += 1
                    bk = True
                    break
            if bk:
                break

    # Returns the self-citation rate as a NumPy 32-bit float
    return np.float32(cited_count) / np.float32(cited_by[['id']].count())[0], total_inspected

# Finds the self-citation rate of an author given their name and a time constraint condition
def find_self_citation_percentage_from_author(author, df, condition='backwards'):
    # global df

    # Determines which parent publications the author was a part of and extracts them
    author_appears = df.loc[df['name'] == author][['id', 'layer', 'name']]
    author_appears = author_appears.loc[author_appears['layer'] == 0]['id']

    # Counts the times they cite themselves
    cited_count = 0

    # Counts the total references their publications have
    total_count = 0

    # Loops through all of the author's parent papers and compares all citation co-authors' names to the query author
    for parent_id in author_appears:
        # Creates a dataframe of only the author's publication's references
        cited_by = df[df['parent'] == parent_id][['id', 'layer', 'name', 'fb']]
        cited_by = cited_by[cited_by['layer'] > 0]

        # Applies a given time constraint filter to the citation dataframe
        if condition == 'backwards':
            cited_by = cited_by[cited_by['fb'] < 0]
        elif condition == 'forwards':
            cited_by = cited_by[cited_by['fb'] > 0]

        # Groups the citations by ID
        cited_by_grouped = cited_by.groupby(['id'])

        # Loops through the names within the citations and compares co-author names to the query author's name
        for cited_name_table in cited_by_grouped:
            for cited_name in cited_name_table[1]['name']:
                if cited_name == author:
                    # Increments citation found count and breaks the loop
                    cited_count += 1
                    break

        # Increments the total count of citations inspected
        total_count += len(cited_by_grouped)
    print(np.float32(cited_count))
    print(np.float32(total_count))

    # Returns self-citation rate as a NumPy 32-bit float
    return np.float32(cited_count) / np.float32(total_count), total_count

# Converts an author name (given in the format "first_name last_name") to PubMed format
def format_author(word):
    to_return = word[(word.index(" ") + 1):] + " " + word[0]
    return to_return.lower()

# # # # # # # # # # # # # # # # # # # # script initiation code # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Load local data into a dataframe
# df = pd.read_csv("/Users/mkorovkin/Desktop/citations_Gary Benson_data_ms549451.csv")

# Define an author to search
# author_to_search = "Gary Benson"

# Calculate self-citation score for an author
# sc_score = find_self_citation_percentage_from_author(format_author(author_to_search), condition='backwards')

# Print the results from above
# print("Author \"" + author_to_search + "\" has " + str(np.round(sc_score * 100.0, decimals=2)) + "% self-citation.")