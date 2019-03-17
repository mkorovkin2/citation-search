import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import json
from os import system

directory = "/Users/mkorovkin/Desktop/"

# Execute external search script; this is for authors
def execute_search_pubmed_terminal(search_name, filter_value, to_id="100"):
    search_name = search_name.lower()
    search_name_nospace = search_name.replace(" ", "+")
    to_id = search_name.replace(" ", "_")

    # Parameters                                                                     search name                 identifier    filtering to last 7 years (boolean)
    system("python " + directory + "_build_desktop_pull_Entrez_individual_AGG.py " + search_name_nospace + " " + to_id + " " + str(filter_value))

# Execute external search script; this is for authors; no 7-year filtering
def execute_search_pubid_terminal(search_id, to_id="100"):
    system(
        "python " + directory + "_desktop_pull_data_Entrez_OPTIMIZED_AGG.py " + search_id + " " + to_id + " False " + search_id)
    return search_id

def execute_search_pubid_terminal_ALERT_TRUE(search_id, to_id="100"):
    system(
        "python " + directory + "_desktop_pull_data_Entrez_OPTIMIZED_AGG.py " + search_id + " " + to_id + " True " + search_id)
    return search_id

# Execute external search script; this is for authors; 7-year filtering
def execute_search_pubid_terminal_name(search_id, to_id="100"):
    search_id_plus = search_id.replace(" ", "_")
    system("python " + directory + "_desktop_pull_data_Entrez_optimized_publication.py " + search_id_plus + " " + to_id + " True " + search_id_plus)
    return search_id_plus

# Execute external search script; this is for retreiving suggested papers based on a query
def execute_search_pubid_suggest_name(search_id, to_id="100"):
    search_id_plus = search_id.replace(" ", "_")
    system("python " + directory + "_desktop_SUB_pull_data_Entrez_optimized_publication2.py " + search_id_plus + " True")
    return search_id_plus

# Execute external search script; this is for publication data; no filtering
def execute_search_pubid_terminal_name_3(search_id, to_id="100"):
    search_id_plus = search_id.replace(" ", "_")
    system(
        "python " + directory + "_desktop_pull_data_Entrez_OPTIMIZED_AGG.py " + search_id_plus + " " + to_id + " False " + search_id_plus)
    return search_id_plus