from __future__ import unicode_literals

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon
import os.path
from scipy.integrate import quad
from scipy.stats import beta
import matplotlib.mlab as mlab

import csearch.api_search.extract_data as extract_data

import unidecode

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .forms import SearchForm, AuthorSearchForm, PubSearchForm, AuthorRepullSearchForm

import os
import pandas as pd
from csearch.api_search.analyze_data_individual_data_optimized import find_self_citation_percentage_from_author, find_self_citation_percentage_from_author2,\
    df_clean_exclude, find_self_citation_percentage_from_author2_forward
from csearch.api_search.analyze_data_publication_data_optimized import publication_score, publication_score_bavkwards, publication_score2, publication_score2_f
from csearch.api_search.APP_pull_data_individual import execute_search_pubmed_terminal, execute_search_pubid_terminal, execute_search_pubid_terminal_name, \
    execute_search_pubid_suggest_name, execute_search_pubid_terminal_name_3, execute_search_pubid_terminal_ALERT_TRUE

save_directory = "/Users/mkorovkin/PycharmProjects/Attempt1/csearch/static/"
dataset_directory = "/Users/mkorovkin/Desktop/"

# Deprecated list
xlist = [0.0   , 0.0125, 0.025 , 0.0375, 0.05  , 0.0625, 0.075 , 0.0875,
         0.1   , 0.1125, 0.125 , 0.1375, 0.15  , 0.1625, 0.175 , 0.1875,
         0.2   , 0.2125, 0.225 , 0.2375, 0.25  , 0.2625, 0.275 , 0.2875,
         0.3   , 0.3125, 0.325 , 0.3375, 0.35  , 0.3625, 0.375 , 0.3875,
         0.4   , 0.4125, 0.425 , 0.4375, 0.45  , 0.4625, 0.475 , 0.4875,
         0.5   , 0.5125, 0.525 , 0.5375, 0.55  , 0.5625, 0.575 , 0.5875,
         0.6   , 0.6125, 0.625 , 0.6375, 0.65  , 0.6625, 0.675 , 0.6875,
         0.7   , 0.7125, 0.725 , 0.7375, 0.75  , 0.7625, 0.775 , 0.7875,
         0.8   , 0.8125, 0.825 , 0.8375, 0.85  , 0.8625, 0.875 , 0.8875,
         0.9   , 0.9125, 0.925 , 0.9375, 0.95  , 0.9625, 0.975 , 0.9875]

# Deprecated stats
pct_0 = np.round(0.000000 * 100.0, decimals=2)
pct_25 = np.round(0.030792 * 100.0, decimals=2)
pct_50 = np.round(0.103914 * 100.0, decimals=2)
pct_75 = np.round(0.217391 * 100.0, decimals=2)

# Deprecated test statistics
def get_practical_percentile(x):
    blist = [0.0011655012, 0.0, 0.003649635, 0.0, 0.01858407, 0.0050301813, 0.0, 0.015625, 0.009009009, 0.0021145714, 0.0,
     0.00931677, 0.0032894737, 0.0, 0.0, 0.0, 0.0040650405, 0.002042901, 0.0, 0.011424731, 0.011111111, 0.01884422,
     0.015053763, 0.0114478115, 0.0, 0.005461165, 0.0, 0.0021008404, 0.007950225, 0.004548408, 0.0088417325,
     0.001497006, 0.0, 0.0023391813, 0.032258064, 0.026610645, 0.0013550136, 0.0056497175, 0.0062305294, 0.0,
     0.0008354219, 0.0049806307, 0.0069258264, 0.0020325202, 0.0, 0.0020318849, 0.000621118, 0.0, 0.0045454544, 0.0,
     0.02011963, 0.0056410255, 0.003907946, 0.0040716613, 0.0, 0.054545455, 0.016666668, 0.017897092, 0.015151516,
     0.0073574493, 0.0, 0.01, 0.0086629, 0.0, 0.026845638, 0.010526316, 0.00096153846, 0.0060975607, 0.0, 0.00882353,
     0.004350979, 0.0062240665, 0.0, 0.006302521, 0.0, 0.001010101, 0.003508772, 0.004878049, 0.009186352, 0.0014947683,
     0.007310705, 0.018621974, 0.0023640662, 0.0025839794, 0.0, 0.0031434186, 0.0121951215, 0.019308943, 0.032863848,
     0.0, 0.0023809525, 0.008368201, 0.019157087, 0.00952381, 0.0011299435, 0.007575758, 0.0, 0.009836066, 0.0124223605,
     0.01056338, 0.0, 0.009041592, 0.0010351967, 0.0038043477, 0.0, 0.029850746, 0.0045592706, 0.0042293235,
     0.007867133, 0.0074487897, 0.0, 0.0, 0.0, 0.0, 0.014160156, 0.0952381, 0.0, 0.0, 0.0, 0.00498132]
    blist.sort()
    print(blist)
    count = 0
    for i in blist:
        if x > i:
            count += 1
    return np.float32(count) / np.float32(len(blist)) * 100.0

# Does a string represent an integer?
def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Format a word based on the quantity (e.g. the "eleventh percentile" versus "second percentile"
def english_ext(x):
    if x % 10 == 1:
        return "st"
    elif x % 10 == 2:
        return "nd"
    elif x % 10 == 3:
        return "rd"
    else:
        return "th"

# Deprecated graphing method using a string instead of a matplotlib graph
def construct_string(ix):
    ar = [0.0, pct_25, pct_50, pct_75, 1.0]
    bk = 0

    for q in range(len(ar) - 1):
        if ix >= ar[q] and ix <= ar[q + 1]:
            bk = q
            break

    x1 = ar[bk]; x2 = ar[bk + 1]
    diff = (x2 - x1)
    diffx2 = ix - x1
    diff_ov = diffx2 / diff * 5
    stop_at = bk * 5 + np.ceil(diff_ov)

    const = "< "
    for i in range(20):
        if i == stop_at:
            const += "* "
        else:
            const += "- "

    return const + ">"

def compute_percentile_pubid(x):
    integ = f_integrate_pubid(x)
    if integ < 0.99:
        return integ
    else:
        return 0.99

# Compute the percentile of an author with self-citations
def f_integrate(x):
    return beta.pdf(x, 1.230, 7.078)

# Compute the percentile of an publication with self-citations
def f_integrate_pubid(x):
    return beta.cdf(x, 0.521, 9.493)

# Compute the percentile of an publication with self-citations
def f_pubid2(x):
    return beta.pdf(x, 0.521, 9.493)

# Show the plot of an publication self-citation distribution
def show_plot_pubid(stat):
    xmax = 1.0
    if stat < 0.15:
        xmax = 0.25
    elif stat < 0.25:
        xmax = stat * 2
    x = np.linspace(0, xmax, 1000)
    plt.plot(xlist, [f_pubid2(x) for x in xlist], 'k')
    plt.title("Distribution of Self-Citation Frequency")
    plt.ylabel("Relative frequency of self-citation rate")
    plt.xlabel("Self-citation rate")
    plt.axvline(x=stat, ymin=0, ymax=1, color='r', linewidth=2)

    img_dir = save_directory + "temp_fig_pub.png"
    print("Saving in directory \"" + img_dir + "\"")
    plt.savefig(img_dir)
    plt.clf()
    plt.close()
    return img_dir

# Compute the percentile of an author with self-citations
def compute_percentile(x):
    return beta.cdf(x, 1.230, 7.078)

# Show the plot of an author self-citation distribution
def show_plot(stat):
    import matplotlib.font_manager as fm
    set([f.name for f in fm.fontManager.ttflist])
    plt.figure()
    xmax = 1.0
    if stat < 0.5:
        xmax = stat * 2.0
        if xmax < 0.25:
            xmax = 0.25
    xlist = np.float32(range(100)) * xmax / 100.0

    # Create the plot in matplotlib
    plt.plot(xlist, [f_integrate(x) for x in xlist], 'k')
    plt.title("Distribution of Self-Citation Frequency")
    plt.ylabel("Min-max scaled relative frequency")
    plt.xlabel("Self-citation rate")
    plt.axvline(x=stat, ymin=0, ymax=1, color='r', linewidth=2)
    img_dir = save_directory + "temp_fig.png"
    print("Saving in directory \"" + img_dir + "\"")
    plt.savefig(img_dir)
    plt.clf()
    plt.close()
    return img_dir

# Format an author name using the PubMed format
def format_author(word):
    to_return = word[(word.index(" ") + 1):] + " " + word[0]
    return to_return.lower()

# Interpret a form request
def search_submit_request(request):
    username = "::ERROR::"
    filter_value = False
    skip = True

    if request.method == "POST":
        # Get the posted form
        my_form = AuthorSearchForm(data=request.POST)

        if my_form.is_valid():
            username = my_form.cleaned_data['username']
            filter_value = my_form.cleaned_data['filter']
            skip = False

    else:
        my_form = AuthorSearchForm()

    if not skip:
        file = open("/Users/mkorovkin/Desktop/temp_file1.txt", "w+")
        file.write("username:" + str(username) + "\nfilter:" + str(filter_value))

    return render(request, 'submit.html', {})

# Deprecated search backup method used for search updates and looping
def search2(request):
    global search_ids

    username = ":"
    filter_value = False
    tfs = "/Users/mkorovkin/Desktop/temp_file1.txt"

    if not os.path.isfile(tfs):
        return render(request, 'failed_to_load.html', {})
    else:
        f_info = open(tfs, "r")
        lines_array = f_info.readlines()
        for line in lines_array:
            if line.startswith("username:"):
                username = line[9:]
            elif line.startswith("filter:"):
                filter_value = line[7:] == "True"

    string_nospace = dataset_directory + "citations_" + username.replace(" ", "_").lower() + str(filter_value) + ".csv"
    if not os.path.isfile(string_nospace):
        execute_search_pubmed_terminal(search_name=username.lower(), filter_value=filter_value)
    if os.path.isfile(string_nospace):
        return HttpResponse("<h1>Title:" + username + "</h1>")
    if os.path.isfile(string_nospace) and not True:
        x, total_found, total_inspected, total_citations = find_self_citation_percentage_from_author2(format_author(username.lower()),
                                                                                                      pd.read_csv(string_nospace))
        percentile_to_return = np.int32(np.ceil(compute_percentile(x) * 100.0))

        practical_percentile = np.ceil(get_practical_percentile(x))

        return render(request, 'submitted.html', {"username": username, "percent": str(np.round(x * 100.0, decimals=2)),
                                                  "twenty_five": pct_25, "fifty": pct_50, "seventy_five": pct_75,
                                                  "graphic": show_plot(x), "percentile": percentile_to_return,
                                                  "total_citations": total_citations,
                                                  "publication_number_ext": "publication" if total_citations == 1 else "publications",
                                                  "percentile_ext": english_ext(percentile_to_return),
                                                  "filter_bool": filter_value,
                                                  "ss_number": total_found,
                                                  "ss_insp": total_inspected,
                                                  "percentile_practical": np.int32(practical_percentile),
                                                  "percentile_practical_ext": english_ext(practical_percentile)
                                                  })

# Method that catches failed form requests
def intermit_search(request):
    global search_ids

    username = "::ERROR::"
    skip = True

    if request.method == "POST":
        # Get the posted form
        my_form = SearchForm(data=request.POST)

        if my_form.is_valid():
            username = unidecode.unidecode(my_form.cleaned_data['username'])
            skip = False

    else:
        print("Something failed in intermit_search(...)")
        my_form = SearchForm()
        return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed author"})

    if not skip:
        d_pop = {}

        return render(request, 'failed_to_load_test.html', {"input": username,
                                                            "links": d_pop,
                                                            "header": "Header",
                                                            "type_request": "PubMed author"})

# Display list of 5 papers which are closest to the user's query
def display_list(request):
    global search_ids

    username = "::ERROR::"
    filter_value = False
    skip = True

    # Deal with the form
    if request.method == "POST":
        # Get the posted form
        my_form = AuthorSearchForm(data=request.POST)

        if my_form.is_valid():
            username = unidecode.unidecode(my_form.cleaned_data['username'])
            filter_value = my_form.cleaned_data['filter']
            skip = False

    else:
        print("Something failed in display_list(...)")
        my_form = AuthorSearchForm()
        return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed author"})

    # If the form is valid...
    if not skip:
        # Find the article names and IDs
        split = username.split("|||")
        username = split[0]
        header = split[1]
        op = np.int32(split[2])
        pub = False
        author_2 = "ERROR"
        if "False.csv" in username:
            author_2 = username[(username.index("citations_") + 10):username.index("False.csv")]
            author_2 = author_2.replace("_", " ")
        elif "True.csv" in username:
            author_2 = username[(username.index("citations_") + 10):username.index("True.csv")]
            author_2 = author_2.replace("_", " ")
        else:
            pub = True
            author_2 = "Publication"

        # Construct a dictionary out of the contents
        d_pop = None
        if pub:
            if op == 1:
                d_pop = extract_data.pub_extract_parents(username) # Total backwards citations
            elif op == 3:
                d_pop = extract_data.pub_extract_b_self(username) # Back self-citations
            elif op == 4:
                d_pop = extract_data.pub_extract_forward(username) # Forward citations
            else:
                return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed author"})
        else:
            if op == 1:
                d_pop = extract_data.extract_parents(username)
            elif op == 2:
                # Inspected
                d_pop = extract_data.extract_inspected(username)
            elif op == 3:
                d_pop = extract_data.extract_b_self(format_author(author_2), username)
            elif op == 4:
                d_pop = extract_data.extract_forward(username)
            else:
                return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed author"})

        return render(request, 'failed_to_load_test.html', {"input": username,
                                                            "links": d_pop,
                                                            "operation": op,
                                                            "header": header,
                                                            "type_request": "PubMed author"})

# Deprecated: filtered request submission based on keywords
def submitted_filtered(request):

    username = "::ERROR::"
    filter_value = False
    i_key = ""
    e_key = ""
    skip = True

    if request.method == "POST":
        # Get the posted form
        my_form = AuthorSearchForm(data=request.POST)

        if my_form.is_valid():
            print(my_form.cleaned_data.keys())
            username = unidecode.unidecode(my_form.cleaned_data['username'])
            filter_value = my_form.cleaned_data['filter']
            i_key = my_form.cleaned_data['includedkey']
            if i_key == None:
                i_key = ""
            e_key = my_form.cleaned_data['excludedkey']
            if e_key == None:
                e_key = ""
            skip = False

    else:
        print("Error >>>> FORM FAILED")
        my_form = AuthorSearchForm()

    if not skip:
        string_nospace = dataset_directory + "citations_" + username.replace(" ", "_").lower() + str(
            filter_value) + ".csv"
        if not os.path.isfile(string_nospace):
            execute_search_pubmed_terminal(search_name=username.lower(), filter_value=filter_value)
        if os.path.isfile(string_nospace):
            csv = pd.read_csv(string_nospace)
            if len(i_key) > 0:
                pass
            if len(e_key) > 0:
                if ',' in e_key:
                    for b in e_key.split(','):
                        csv = df_clean_exclude(b, csv)
                else:
                    csv = df_clean_exclude(e_key, csv)
            x, total_found, total_inspected, total_citations, forward_citations = find_self_citation_percentage_from_author2(
                format_author(username.lower()), csv)
            fsr = find_self_citation_percentage_from_author2_forward(format_author(username.lower()), csv)

            percentile_to_return = np.int32(np.ceil(compute_percentile(x) * 100.0))

            practical_percentile = np.ceil(get_practical_percentile(x))

            total_citations_link = ""
            ss_insp_link = ""
            forward_ref_link = ""
            ss_number_link = ""

            return render(request, 'submitted.html',
                          {"username": username, "percent": str(np.round(x * 100.0, decimals=2)),
                           "twenty_five": pct_25, "fifty": pct_50, "seventy_five": pct_75,
                           "graphic": show_plot(x), "percentile": percentile_to_return,
                           "total_citations": total_citations,
                           "publication_number_ext": "publication" if total_citations == 1 else "publications",
                           "percentile_ext": english_ext(percentile_to_return),
                           "filter_bool": filter_value,
                           "forward_citation_number": forward_citations,
                           "ss_number": total_found,
                           "ss_insp": total_inspected,
                           "percentile_practical": np.int32(practical_percentile),
                           "percentile_practical_ext": english_ext(practical_percentile),
                           "total_citations_link": total_citations_link,
                           "ss_insp_link": ss_insp_link,
                           "ss_number_link": ss_number_link,
                           "forward_ref_link": forward_ref_link,
                           "local_link": string_nospace,
                           "fsr": np.round(fsr * 100.0, decimals=2),
                           })  # "graphic": show_plot(x)
            # "rep_string": construct_string(x),
            #    #, "graphic": get_graphic(statistics)})
            # <img src="data:image/png;base64,{{graphic|safe}}" style="margin: 4%; width: 20%; height: 20%;">
        else:
            print('Error >>> NO LOCAL FILE FOUND')
            return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed author"})

# PRIMARY method for author self-citation searching
def search(request):
    global search_ids

    # All potential input values
    username = "::ERROR::"
    filter_value = False
    i_key = ""
    e_key = ""
    skip = True
    caution = False
    repull_value = False

    # Form verification
    if request.method == "POST":
        # Get the posted form
        my_form = AuthorRepullSearchForm(data=request.POST)
        my_form2 = SearchForm(data=request.POST)

        if my_form.is_valid():
            username = unidecode.unidecode(my_form.cleaned_data['username'])
            filter_value = my_form.cleaned_data['filter']
            repull_value = my_form.cleaned_data['repull']
            i_key = my_form.cleaned_data['includedkey']
            if i_key == None:
                i_key = ""
            elif len(i_key) > 5:
                iarray = i_key.split("|||")
                location2 = username.split("|||")[1]
                dfff = pd.read_csv(location2)
                caution = True
                for ui in iarray[1:]:
                    lenoriginal = len(dfff.loc[:]['parent'])
                    dfff = dfff.loc[dfff['parent'] != np.int32(ui)]
                    dfff = dfff.loc[dfff['id'] != np.int32(ui)]
                    len_new = len(dfff.loc[:]['parent'])
                    print("Local database size reduction from", lenoriginal, "to", len_new)

                dfff.to_csv(location2)

            e_key = my_form.cleaned_data['excludedkey']
            if e_key == None:
                e_key = ""
            skip = False
    else:
        print("Error >>>> FORM FAILED")
        my_form = AuthorRepullSearchForm()

    # If the form is vaild...
    if not skip:
        string_nospace = ""
        if not caution:
            string_nospace = dataset_directory + "citations_" + username.replace(" ", "_").lower() + ".csv"
        else:
            # Identify usernames and papers
            uu = username.split("|||")
            username = uu[0]
            string_nospace = uu[1]

        # Verify file path
        if not os.path.isfile(string_nospace):
            execute_search_pubmed_terminal(search_name=username.lower(), filter_value=filter_value)

        # Operate on the file path; create graphs; analyze data
        if os.path.isfile(string_nospace):
            if repull_value:
                execute_search_pubmed_terminal(search_name=username.lower(), filter_value=filter_value)
            if os.path.isfile(save_directory + "temp_fig.png"):
                os.remove(save_directory + "temp_fig.png")
            csv = pd.read_csv(string_nospace)
            if len(i_key) > 0:
                pass
            if len(e_key) > 0:
                if ',' in e_key:
                    for b in e_key.split(','):
                        csv = df_clean_exclude(b, csv)
                else:
                    csv = df_clean_exclude(e_key, csv)

            # Analyze data
            x, total_found, total_inspected, total_citations, forward_citations, refdfb, refdff, refdfo, ref_ss = find_self_citation_percentage_from_author2(format_author(username.lower()), csv)
            fsr = find_self_citation_percentage_from_author2_forward(format_author(username.lower()), csv)

            # List out all titles/IDs of papers which appear in the bottom drop down list areas
            refdfb_k = list(refdfb.loc[:]["id"])
            refdfb_v = list(refdfb.loc[:]['title'])

            refdff_k = list(refdff.loc[:]["id"])
            refdff_v = list(refdff.loc[:]['title'])

            refdfo_k = list(refdfo.loc[:]["id"])
            refdfo_v = list(refdfo.loc[:]['title'])

            refdfb_dict = {}
            refdff_dict = {}
            refdfo_dict = {}

            for index in range(len(refdfb_k)):
                refdfb_dict[str(refdfb_k[index])] = refdfb_v[index]
            for index in range(len(refdff_k)):
                refdff_dict[str(refdff_k[index])] = refdff_v[index]
            for index in range(len(refdfo_k)):
                refdfo_dict[str(refdfo_k[index])] = refdfo_v[index]

            x = x if total_found > 0 else 0

            # Compute more paper statistics
            practical_percentile = np.ceil(get_practical_percentile(x))
            percentile_computed = np.int8(np.ceil(compute_percentile(x) * 100))

            # Establish links
            total_citations_link = ""
            ss_insp_link = ""
            forward_ref_link = ""
            ss_number_link = ""

            # Temporary stuff
            dddd={"http://www.google.com": "Google",
                                                                       "http://www.yahoo.com": "Yahoo",
                                                                       "http://www.apple.com": "Apple",
                                                                       "http://www.apple2.com": "Apple2",
                                                                       "http://www.apple3.com": "Apple3",
                                                                       "http://www.apple4.com": "Apple4",
                                                                       "http://www.apple5.com": "Apple5",
                                                                       "http://www.apple6.com": "Apple6",
                                                                       "http://www.apple7.com": "Apple7"}

            # Delete data file -- commented b/c could be kept for quick access before
            # os.remove(string_nospace)

            # Render the page
            return render(request, 'submitted.html', {"username": username, "percent": str(np.round(x * 100.0, decimals=2)),
                                                      "twenty_five": pct_25, "fifty": pct_50, "seventy_five": pct_75,
                                                      "graphic": show_plot(x), "percentile": percentile_computed,
                                                      "total_citations": total_citations,
                                                      "publication_number_ext": "publication" if total_citations == 1 else "publications",
                                                      "percentile_ext": english_ext(percentile_computed),
                                                      "filter_bool": filter_value,
                                                      "forward_citation_number": forward_citations,
                                                      "ss_number": total_found,
                                                      "ss_insp": total_inspected,
                                                      "percentile_practical": np.int32(practical_percentile),
                                                      "percentile_practical_ext": english_ext(practical_percentile),
                                                      "total_citations_link": total_citations_link,
                                                      "ss_insp_link": ss_insp_link,
                                                      "ss_number_link": ss_number_link,
                                                      "forward_ref_link": forward_ref_link,
                                                      "local_link": string_nospace,
                                                      "filter_value_": filter_value,
                                                      "papers_input": dddd,
                                                      "papers_input_1": refdfo_dict,
                                                      "papers_input_2": refdfb_dict,
                                                      "papers_input_3": ref_ss,
                                                      "papers_input_4": refdff_dict,
                                                      "fsr": np.round(fsr * 100.0, decimals=2),
                                                      })
        else:
            # Failed to load the page
            print('Error >>> NO FILE; local file directory: ' + string_nospace)
            return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed author"})
    else:
        # Form was not valid
        print('Error >>> FORM WAS NOT VALID')
        return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed author"})

# Deprecated
def select_papers(request):
    pass

# PRIMARY method for publication self-citation searching
def search_pub(request):
    global search_id

    # Important parameters
    username = "::ERROR::"
    choosepaper = False
    skip = True

    # Verify form
    if request.method == "POST":
        # Get the posted form
        my_form = PubSearchForm(data=request.POST)

        if my_form.is_valid():
            username = my_form.cleaned_data['username']
            choosepaper = my_form.cleaned_data['choosepaper']
            skip = False
        else:
            print("Error >>>> ", my_form.errors)
    else:
        my_form = PubSearchForm()
        print("Error >>>> FORM WAS NOT VALID")

    # If the user has elected to chooose the "closest paper to the query string", run this operation
    if choosepaper:
        # Use this paper as the search query -- TODO
        pass

    # If form was valid...
    if not skip and not choosepaper:
        # Local files
        string_nospace = dataset_directory + "citations_" + str(username) + ".csv"
        print("string nospace", string_nospace)
        f_info_string = dataset_directory + "citations_" + str(username) + "_info.txt"

        # Retrieve publication information
        if not os.path.isfile(string_nospace):
            if represents_int(username):
                execute_search_pubid_terminal(search_id=username)
            else:
                segment = execute_search_pubid_suggest_name(search_id=username)
                string_nospace = dataset_directory + "citations_" + segment + ".csv"
                f_info_string = dataset_directory + "citations_" + segment + "_info.txt"
                paperdict = {}
                with open(f_info_string) as f:
                    for line in f:
                        split_ = line.split("|||{split}|||")
                        paperdict[split_[0]] = split_[1]

                # Render the select papers page
                return render(request, 'select_papers.html',
                              {"input": username,
                               "papers": paperdict,
                               "header": "Select a publication...",
                               "location": string_nospace
                               })

        # Locate the local file
        if os.path.isfile(string_nospace):
            print("yeed"); print(string_nospace)
            x, num_pubs, len_citedin, num_ss_pub, refdfb = publication_score2(pd.read_csv(string_nospace))
            x_f, num_pubs_f, len_citedin_f, num_ss_pub_f, refdff = publication_score2_f(pd.read_csv(string_nospace))
            if os.path.isfile(save_directory + "temp_fig_pub.png"):
                os.remove(save_directory + "temp_fig_pub.png")

            # Compute the percentile of self-citations
            x = x if num_pubs > 0 else 0
            x_f = x_f if num_pubs_f > 0 else 0
            x_str = str(np.round(x * 100.0, decimals=2))
            x_str_f = str(np.round(x_f * 100.0, decimals=2))
            percentile_to_return = np.int32(np.ceil(compute_percentile_pubid(x) * 100.0))

            # Construct strings used within the page
            cited_in_text = "This publication was cited by " + str(len_citedin) + " other publications."
            if len_citedin < 1:
                cited_in_text = "Failed to determine number of publications citing this citation."

            # Extract publication information from local text file
            pub_name = "<name of pub>"
            pub_year = 2021
            pub_la = ":la"
            pub_fa = ":fa"
            pub_id = "0"
            pub_doi = "doi.bububu"
            pub_author_list_string = ""
            f_info = open(f_info_string, "r")
            lines_array = f_info.readlines()
            for line in lines_array:
                if line.startswith("name:"):
                    pub_name = line[5:]
                elif line.startswith("doi:"):
                    pub_doi = line[4:]
                elif line.startswith("year:"):
                    pub_year = line[5:]
                elif line.startswith("fa:"):
                    pub_fa = line[3:].replace(" ", ", ")
                elif line.startswith("id:"):
                    pub_id = line[3:].replace(" ", ", ")
                elif line.startswith("la:"):
                    pub_la = line[3:].replace(" ", ", ")
                elif line.startswith("gauthor:"):
                    pub_author_list_string += line[8:(len(line) - 1)] + ", "
            pub_link = "https://www.ncbi.nlm.nih.gov/pubmed/" + str(pub_id)

            # Determine publication year
            use_new_data = False

            pub_author_list_string = pub_author_list_string[:(len(pub_author_list_string) - 2)]

            # Organize data and information used for papers within the drop-down area of the page
            refdfb_k = list(refdfb.loc[:]["id"])
            refdfb_v = list(refdfb.loc[:]['title'])  # ["title"])

            refdff_k = list(refdff.loc[:]["id"])
            refdff_v = list(refdff.loc[:]['title'])

            refdfb_dict = {}
            refdff_dict = {}

            for index in range(len(refdfb_k)):
                refdfb_dict[str(refdfb_k[index])] = refdfb_v[index]
            for index in range(len(refdff_k)):
                refdff_dict[str(refdff_k[index])] = refdff_v[index]

            # Delete files to clear space usage; commented for cache-efficiency purposes and such
            #os.remove(string_nospace)
            #os.remove(f_info_string)

            # Render the page
            return render(request, 'submitted_pub.html',
                          {"pubid": pub_id, "percent": np.round(x * 100, decimals=2),#x_str_f,
                           "twenty_five": pct_25, "fifty": pct_50, "seventy_five": pct_75,
                           "graphic": show_plot_pubid(x),
                           "percentile": percentile_to_return,
                           "total_citations": np.int32(num_pubs),
                           "publication_number_ext": "publication" if num_pubs == 1 else "publications",
                           "percentile_ext": english_ext(percentile_to_return),
                           "pub_name": pub_name,
                           "pub_year": str(pub_year)[:(len(str(pub_year)) - 1)],
                           "pub_doi": "DOI not found" if pub_doi.startswith("::") else pub_doi,
                           "pub_doi_link": "http://doi.org/" + str(pub_doi),
                           "pub_link": pub_link,
                           "forward_citation_number": np.int16(num_pubs_f),
                           "ss_number": num_ss_pub,
                           "forward_percent": np.round(x_f * 100.0, decimals=2),
                           "author_string": pub_author_list_string,
                           "cited_in_text": cited_in_text,
                           "local_link": string_nospace,
                          "papers_input_2": refdfb_dict,
                          "papers_input_4": refdff_dict,
                           })
        else:
            # Local files not found
            print("Error >>>> LOCAL FILE ABSENT (pub); local directory: " + string_nospace)
            return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed ID search"})
    else:
        # Form failed
        return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed ID search"})

# Deprecated - update the local database of publication based on user selection
def update_list(request):
    global search_ids

    username = "::ERROR::"
    filter_value = False
    skip = True

    # Deal with form
    if request.method == "POST":
        # Get the posted form
        my_form = AuthorSearchForm(data=request.POST)

        if my_form.is_valid():
            username = unidecode.unidecode(my_form.cleaned_data['username'])
            filter_value = my_form.cleaned_data['filter']

    else:
        print("Something failed in update_list(...)")
        my_form = AuthorSearchForm()
        return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed author"})

    # Form was valid
    if not skip:
        split = username.split("|||")
        username = split[0]
        typez = split[1]
        other = split[2]
        author_2 = ""

        if "False.csv" in username:
            author_2 = username[(username.index("citations_") + 10):username.index("False.csv")]
            author_2 = author_2.replace("_", " ")
        elif "True.csv" in username:
            author_2 = username[(username.index("citations_") + 10):username.index("True.csv")]
            author_2 = author_2.replace("_", " ")
        else:
            author_2 = "Publication"

        # Extract list of papers
        if "|" in other:
            other = other[:(len(other) - 1)]
            checkboxes = other.replace("checkbox", "")
            pmid_array = checkboxes.split("|")
            int_array = list()
            for pmid in pmid_array:
                int_array.append(np.int32(pmid))

            df = pd.read_csv(username)
            for id in int_array:
                newint = np.int32(typez)
                if newint == 1:
                    df = df.loc[df['id'] != id]
                    df = df.loc[df['parent'] != id]
                elif newint == 2:
                    df = df.loc[df['id'] != id]
                    df = df.loc[df['parent'] != id]
                elif newint == 3:
                    df = df.loc[df['id'] != id]
                elif newint == 4:
                    df = df.loc[df['id'] != id]
                else:
                    df = df.loc[df['id'] != id]
                    df = df.loc[df['parent'] != id]

                df.to_csv(username)

            return render_updated_page(request, username, author_2)

        else:
            return render(request, 'failed_to_load.html', {"input": author_2,
                                                                "type_request": "PubMed author"})

# Deprecated - update the local database of publication based on user selection; used by update_list(...) function
def render_updated_page(request, user, authorname):
    username = user
    if "False.csv" in username:
        filter_value = False
    else:
        filter_value = True
    if not os.path.isfile(username):
        execute_search_pubmed_terminal(search_name=authorname.lower(), filter_value=filter_value)
    if os.path.isfile(username):
        csv = pd.read_csv(username)
        x, total_found, total_inspected, total_citations, forward_citations = find_self_citation_percentage_from_author2(
            format_author(authorname.lower()), csv)
        percentile_to_return = np.int32(np.ceil(compute_percentile(x) * 100.0))

        practical_percentile = np.ceil(get_practical_percentile(x))

        total_citations_link = ""
        ss_insp_link = ""
        forward_ref_link = ""
        ss_number_link = ""

        return render(request, 'submitted.html',
                      {"username": authorname, "percent": str(np.round(x * 100.0, decimals=2)),
                       "twenty_five": pct_25, "fifty": pct_50, "seventy_five": pct_75,
                       "graphic": show_plot(x), "percentile": percentile_to_return,
                       "total_citations": total_citations,
                       "publication_number_ext": "publication" if total_citations == 1 else "publications",
                       "percentile_ext": english_ext(percentile_to_return),
                       "filter_bool": filter_value,
                       "forward_citation_number": forward_citations,
                       "ss_number": total_found,
                       "ss_insp": total_inspected,
                       "percentile_practical": np.int32(practical_percentile),
                       "percentile_practical_ext": english_ext(practical_percentile),
                       "total_citations_link": total_citations_link,
                       "ss_insp_link": ss_insp_link,
                       "ss_number_link": ss_number_link,
                       "forward_ref_link": forward_ref_link,
                       "local_link": username,
                       })
    else:
        print('Errro >>>> NO LOCAL FILE FOUND')
        return render(request, 'failed_to_load.html', {"input": authorname, "type_request": "PubMed author"})

# Deprecated - used to search for full names of papers; identical to search_pub(...) method but older and doesn't work
def search_pub_specified_paper(request):
    global search_id

    username = "::ERROR::"
    skip = True

    if request.method == "POST":
        # Get the posted form
        my_form = SearchForm(data=request.POST)

        if my_form.is_valid():
            username = my_form.cleaned_data['username']
            skip = False
        else:
            print("Error >>>>", my_form.errors)
    else:
        my_form = SearchForm()
        print("Error >>>> FORM NOT VALID")

    if not skip:
        username = username.split("|||")[1]
        print("----specified paper-----")

        # Local files
        string_nospace = dataset_directory + "citations_" + str(username) + ".csv"
        print("string nospace", string_nospace)
        f_info_string = dataset_directory + "citations_" + str(username) + "_info.txt"

        # Retrieve publication information
        if not os.path.isfile(string_nospace):
            if represents_int(username):
                execute_search_pubid_terminal(search_id=username)
            else:
                segment = execute_search_pubid_suggest_name(search_id=username)
                string_nospace = dataset_directory + "citations_" + segment + ".csv"
                f_info_string = dataset_directory + "citations_" + segment + "_info.txt"
                paperdict = {}
                with open(f_info_string) as f:
                    for line in f:
                        split_ = line.split("|||{split}|||")
                        paperdict[split_[0]] = split_[1]

                # Render the select papers page
                return render(request, 'select_papers.html',
                              {"input": username,
                               "papers": paperdict,
                               "location": string_nospace
                               })

        # Locate the local file
        if os.path.isfile(string_nospace):
            print("yeed");
            print(string_nospace)
            x, num_pubs, len_citedin, num_ss_pub, refdfb = publication_score2(pd.read_csv(string_nospace))
            x_f, num_pubs_f, len_citedin_f, num_ss_pub_f, refdff = publication_score2_f(pd.read_csv(string_nospace))
            if os.path.isfile(save_directory + "temp_fig_pub.png"):
                os.remove(save_directory + "temp_fig_pub.png")

            # Compute the percentile of self-citations
            x = x if num_pubs > 0 else 0
            x_f = x_f if num_pubs_f > 0 else 0
            x_str = str(np.round(x * 100.0, decimals=2))
            x_str_f = str(np.round(x_f * 100.0, decimals=2))
            percentile_to_return = np.int32(np.ceil(compute_percentile_pubid(x) * 100.0))

            # Construct strings used within the page
            cited_in_text = "This publication was cited by " + str(len_citedin) + " other publications."
            if len_citedin < 1:
                cited_in_text = "Failed to determine number of publications citing this citation."

            # Extract publication information from local text file
            pub_name = "<name of pub>"
            pub_year = 2021
            pub_la = ":la"
            pub_fa = ":fa"
            pub_id = "0"
            pub_doi = "doi.bububu"
            pub_author_list_string = ""
            f_info = open(f_info_string, "r")
            lines_array = f_info.readlines()
            for line in lines_array:
                if line.startswith("name:"):
                    pub_name = line[5:]
                elif line.startswith("doi:"):
                    pub_doi = line[4:]
                elif line.startswith("year:"):
                    pub_year = line[5:]
                elif line.startswith("fa:"):
                    pub_fa = line[3:].replace(" ", ", ")
                elif line.startswith("id:"):
                    pub_id = line[3:].replace(" ", ", ")
                elif line.startswith("la:"):
                    pub_la = line[3:].replace(" ", ", ")
                elif line.startswith("gauthor:"):
                    pub_author_list_string += line[8:(len(line) - 1)] + ", "
            pub_link = "https://www.ncbi.nlm.nih.gov/pubmed/" + str(pub_id)

            # Determine publication year
            use_new_data = False

            pub_author_list_string = pub_author_list_string[:(len(pub_author_list_string) - 2)]

            # Organize data and information used for papers within the drop-down area of the page
            refdfb_k = list(refdfb.loc[:]["id"])
            refdfb_v = list(refdfb.loc[:]['title'])  # ["title"])

            refdff_k = list(refdff.loc[:]["id"])
            refdff_v = list(refdff.loc[:]['title'])

            refdfb_dict = {}
            refdff_dict = {}

            for index in range(len(refdfb_k)):
                refdfb_dict[str(refdfb_k[index])] = refdfb_v[index]
            for index in range(len(refdff_k)):
                refdff_dict[str(refdff_k[index])] = refdff_v[index]

            # Delete files to clear space usage; commented for cache-efficiency purposes and such
            # os.remove(string_nospace)
            # os.remove(f_info_string)

            # Render the page
            return render(request, 'submitted_pub.html',
                          {"pubid": pub_id, "percent": np.round(x * 100, decimals=2),  # x_str_f,
                           "twenty_five": pct_25, "fifty": pct_50, "seventy_five": pct_75,
                           "graphic": show_plot_pubid(x),
                           "percentile": percentile_to_return,
                           "total_citations": np.int32(num_pubs),
                           "publication_number_ext": "publication" if num_pubs == 1 else "publications",
                           "percentile_ext": english_ext(percentile_to_return),
                           "pub_name": pub_name,
                           "pub_year": str(pub_year)[:(len(str(pub_year)) - 1)],
                           "pub_doi": "DOI not found" if pub_doi.startswith("::") else pub_doi,
                           "pub_doi_link": "http://doi.org/" + str(pub_doi),
                           "pub_link": pub_link,
                           "forward_citation_number": np.int16(num_pubs_f),
                           "ss_number": num_ss_pub,
                           "forward_percent": np.round(x_f * 100.0, decimals=2),
                           "author_string": pub_author_list_string,
                           "cited_in_text": cited_in_text,
                           "local_link": string_nospace,
                           "papers_input_2": refdfb_dict,
                           "papers_input_4": refdff_dict,
                           })
        else:
            print("Error >>>> LOCAL FILE NOT FOUND")
            return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed ID search"})
    else:
        print("Error >>>> FORM WAS NOT VALID")
        return render(request, 'failed_to_load.html', {"input": username, "type_request": "PubMed ID search"})