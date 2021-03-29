import re
import pandas
import sys
from read_write_categories import read_categories
import matplotlib.pyplot as plot
import numpy as np
import json
from plot_monthly import plot_stackedbargraph, plot_piechart
import os

# categories = ["Kos", "Apteek", "Parkering", "Brandstof", "Hardeware", "Sport toerusting"]
categories_dict = dict()
# match_strings_dict=dict()
categories, match_strings_dict = read_categories()
print("Categories:", categories)
# print(match_strings_dict)

category_totals = dict()
filename = ""

plot_graphs = True
try:
    os.mkdir("by_category")
except FileExistsError:
    print("by_category folder already exists.")
try:
    os.mkdir("plots")
except FileExistsError:
    print("plots folder already exists.")

def match_category(data, category):
    print("\nCategory:", category)
    print("Search key:", match_strings_dict[category][0])
    categories_dict[category] = data[data['Beskrywing'].str.contains(match_strings_dict[category][0])]
    
    for i in range(1,len(match_strings_dict[category])):
        print("Search key:", match_strings_dict[category][i])
        categories_dict[category] = pandas.concat(
            [categories_dict[category],
            data[data['Beskrywing'].str.contains(match_strings_dict[category][i])]],
            )
        categories_dict[category] = categories_dict[category].drop_duplicates()
    print("\n")

    # print("Total of ", category + ":", "R%5.2f" % categories_dict[category]["Bedrag"].sum())
    category_filename = re.sub(".csv", "_" + category + ".csv", filename)
    category_filename = os.path.join("by_category", category_filename)
    print("category_filename", category_filename)
    categories_dict[category].to_csv(category_filename, mode='w')

    category_totals[category] = categories_dict[category]["Bedrag"].sum()

def get_remaining(data):
    """Rows from main dataframe which are not in any of the other frames"""
    sorted_df = pandas.concat(categories_dict)
    df_diff = data.merge(sorted_df, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only'].iloc[:,:-1]
    return df_diff

def main():
    if len(sys.argv) < 2:
        print("Usage: sort_by_vendor.py <filename.csv> <plot_graphs> <extra_file.pdf>")
        exit(0)

    global filename, plot_graphs
    filename = sys.argv[1]
    secondary_filename = ""

    print("Filename:", filename)

    plot_variable = ""
    if len(sys.argv) == 3:
        plot_variable = sys.argv[2]

    if plot_variable == "no" or plot_variable == "0":
        plot_graphs = False

    if len(sys.argv) >= 4:
        secondary_filename = sys.argv[3]
        print("Secondary filename: ", secondary_filename)

    data = pandas.read_csv(filename)
    # print(data)

    if secondary_filename != "":
        data2 = pandas.read_csv(filename)
        data = data.append(data2, ignore_index = True)

    for category in categories:
        match_category(data, category)

    # print(categories_dict["Kos"])
    # print("Total of Kos:", categories_dict["Kos"]["Bedrag"].sum())
    # print("\n", categories_dict["Apteek"])

    remaining = get_remaining(data)

    print("Category totals:")
    for key in category_totals.keys():
        print(key, ":", "R%5.2f" % category_totals[key])

    print("\nRemaining:\n", remaining)

    category_totals["Sundries"] = remaining["Bedrag"].sum()
    print("Sundries:", category_totals["Sundries"])

    current_json = None
    #Write out to MonthSummary
    try:
        file_size = os.stat("MonthSummary.txt").st_size
        print("File size:", file_size)
        if file_size > 2:
            with open("MonthSummary.txt", 'r') as summary_file:
                file_contents = summary_file.read()
                current_json = json.loads(file_contents)
                # print(current_json)
    except FileNotFoundError:
        print("MonthSummary.txt does not exists, continuing.")

    split_filename, directory = os.path.split(filename)

    if current_json == None or split_filename not in current_json:
        if current_json == None:
            current_json = dict()

    print("Writing to MonthSummary")
    current_json[split_filename] = category_totals
    with open("MonthSummary.txt", 'w') as summary_file:
        summary_file.write(json.dumps(current_json))

    if plot_graphs == True:
        plot_piechart(split_filename, category_totals)
        plot_stackedbargraph(category_totals, 0, split_filename[0:7], filename=os.path.join("plots",split_filename))

    plot.show()

if __name__ == '__main__':
    main()