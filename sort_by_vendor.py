import re
import pandas
import sys
from read_write_categories import read_categories
import matplotlib.pyplot as plot
import numpy as np
import json
from plot_monthly import plot_stackedbargraph, plot_piechart
import os

categories_dict = dict()
categories, match_strings_dict = read_categories()
print("Categories:", categories)

category_totals = dict()

plot_graphs = True
try:
    os.mkdir("by_category")
except FileExistsError:
    print("by_category folder already exists.")
try:
    os.mkdir("plots")
except FileExistsError:
    print("plots folder already exists.")

def match_category(data, category, strFilenameToProcess):
#    print("\nCategory:", category)
#    print("Search key:", match_strings_dict[category][0])
    categories_dict[category] = data[data['Description'].str.contains(match_strings_dict[category][0])]
    
    for i in range(1,len(match_strings_dict[category])):
#        print("Search key:", match_strings_dict[category][i])
        categories_dict[category] = pandas.concat(
            [categories_dict[category],
            data[data['Description'].str.contains(match_strings_dict[category][i])]],
            )
        categories_dict[category] = categories_dict[category].drop_duplicates()
#    print("\n")

    strDirectory, strFilename = os.path.split(strFilenameToProcess)
    # print("Total of ", category + ":", "R%5.2f" % categories_dict[category]["Amount"].sum())
    category_filename = re.sub(".csv", "_" + category + ".csv", strFilename)
#    print("Category_filename", category_filename)
    category_foldername = os.path.join(strDirectory, "by_category")
#    print("category_foldername", category_foldername)
    category_filename = os.path.join(category_foldername, category_filename)
#    print("category_filename", category_filename)
    categories_dict[category].to_csv(category_filename, mode='w')

    category_totals[category] = categories_dict[category]["Amount"].sum()

def get_remaining(data):
    """Rows from main dataframe which are not in any of the other frames"""
    sorted_df = pandas.concat(categories_dict)
    df_diff = data.merge(sorted_df, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only'].iloc[:,:-1]
    return df_diff

def SortByVendor(strFilenameToProcess, bPlotGraphs):

    global categories, match_strings_dict
    categories, match_strings_dict = read_categories()
    print("Filename:", strFilenameToProcess)

    try:
        OpenCheck = open(strFilenameToProcess, 'r')
    except FileNotFoundError:
        print("File %s was not found: " % strFilenameToProcess)
        return

    data = pandas.read_csv(strFilenameToProcess)
    # print(data)

    # Make expenses a positive value
    data['Amount'] = -1*data['Amount']

    # Drop incomes (i.e. negative expenses)
    data = data.drop(data[data['Amount'] <= 0].index)


    for category in categories:
        match_category(data, category, strFilenameToProcess)

    remaining = get_remaining(data)

    print("Category totals:")
    for key in category_totals.keys():
        print(key, ":", "R%5.2f" % category_totals[key])

    print("\nRemaining:\n", remaining)

    category_totals["Sundries"] = remaining["Amount"].sum()
    print("Sundries:", category_totals["Sundries"])

    directory, split_filename = os.path.split(strFilenameToProcess)
    print(split_filename)
    strRemainingFilename = re.sub(".csv", "_uncategorized.csv", split_filename)
    print(strRemainingFilename)
    strRemainingFilename = os.path.join("uncategorized", strRemainingFilename)
    print(strRemainingFilename)
    strRemainingFilename = os.path.join(directory, strRemainingFilename)
    print(strRemainingFilename)
    
    try:
        os.mkdir(os.path.join(directory,"uncategorized"))
    except FileExistsError:
        print("uncategorized folder already exists.")
    remaining.to_csv(strRemainingFilename)
    
    current_json = None
    #Write out to MonthSummary
    strMonthSummaryFilename = os.path.join(directory, "MonthSummary.txt")
    try:
        file_size = os.stat(strMonthSummaryFilename).st_size
        print("File size:", file_size)
        if file_size > 2:
            with open(strMonthSummaryFilename, 'r') as summary_file:
                file_contents = summary_file.read()
                current_json = json.loads(file_contents)
                # print(current_json)
    except FileNotFoundError:
        print("%s does not exists, continuing." % strMonthSummaryFilename)


    if current_json == None or split_filename not in current_json:
        if current_json == None:
            current_json = dict()

    print("Writing to MonthSummary")
    current_json[split_filename] = category_totals
    with open(strMonthSummaryFilename, 'w') as summary_file:
        summary_file.write(json.dumps(current_json))

    strPlotFolder = os.path.join(directory, "plots")

    if plot_graphs == True:
        plot_piechart(strFilenameToProcess, category_totals)
        plot_stackedbargraph(category_totals, 0, split_filename[0:7], strFullFilename=strFilenameToProcess)

    plot.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: sort_by_vendor.py <filename.csv> <plot_graphs>")
        exit(0)

    strFilenameToProcess = sys.argv[1]

    bPlotGraphs = False
    if len(sys.argv) >= 3:
    	if sys.argv[2] == "1" or "True":
    		bPlotGraphs = True
    	else:
    		print("Unknown input for argument 2 (Plot graphs)")

    SortByVendor(strFilenameToProcess, bPlotGraphs)

if __name__ == '__main__':
    main()
