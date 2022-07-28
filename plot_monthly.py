import re
import pandas
import sys
from read_write_categories import read_categories
import matplotlib
import matplotlib.pyplot as plot
import numpy as np
import json
import os
from datetime import datetime
from matplotlib.lines import Line2D
from matplotlib.cm import get_cmap

categories, match_strings_dict = read_categories()
categories.append("Sundries")
category_to_colour = dict()
#plt_colours = plot.rcParams['axes.prop_cycle'].by_key()['color']
plt_colours = [i for i in get_cmap('tab20').colors]
for i in range(len(categories)):
    category_to_colour[categories[i]] = plt_colours[i%len(plt_colours)]

def plot_piechart(strFullFilename, category_totals, dictIncomeTotals):
    #Plotting
    print(category_totals.values())
    # print("\n===\nCategories in dictionary", categories_dict.keys())
    for key in category_totals:
        category_totals[key] = -1*category_totals[key]
    keys = list()
    values = list()
    colours = list()
    ExpensesSum = np.sum(list(category_totals.values()))
    IncomesSum = np.sum(list(dictIncomeTotals.values()))
    print("Expenses Sum %2.2f" % ExpensesSum)
    print("Incomes Sum %2.2f" % IncomesSum)

    #Ignore smallest values in pie chart
    for key in category_totals.keys():
        print(category_totals[key])
        print("Percentage of total: ", 100*float(category_totals[key])/ExpensesSum)
        if (category_totals[key] < 0):
#            print("Not plotting income", key)
            continue
        elif category_totals[key] == 0:
#            print("Ignoring unused category", key)
            pass
        else:
            keys.append(key)
            values.append(category_totals[key])
            colours.append(category_to_colour[key])

    pie_labels = ["%s" % (keys[x]) for x in range(len(keys))]
    labels = ["%s:R%s" % (keys[x], format(values[x],",.2f").replace(",", " ")) for x in range(len(keys))]

    print(labels)
    fig = plot.figure()
    ax = fig.add_axes([0.2, 0.1, 0.4, 0.8])

    wedges, texts, autotexts = ax.pie(values, labels=pie_labels, colors=colours, autopct='%1.1f%%')

    ax.legend(wedges, labels,
                loc="center left",
                bbox_to_anchor=(0.9, 0, 0.4, 1))

    strDirectory, strFilename = os.path.split(strFullFilename)

    title_text = re.sub(".csv", "", strFilename)
    title_text = re.sub("_raw", "", title_text)
    title_text = re.sub("_transaksies", "", title_text)
    plot.title(title_text + "\n" + "Income R%2.2f, Expenses R%2.2f, Difference R%2.2f" % (IncomesSum, ExpensesSum, IncomesSum - ExpensesSum))
    strPlotSavePath = re.sub(".csv", "_pie.pdf", strFilename)
    strPlotSaveDirectory = os.path.join(strDirectory, "plots")
    try:
        os.mkdir(strPlotSaveDirectory)
    except FileExistsError:
#        print("%s folder already exists." % category_foldername)
        pass
    strPlotSavePath = os.path.join(strPlotSaveDirectory, strPlotSavePath)
    plot.savefig(strPlotSavePath)

def plot_stackedbargraph(category_totals, index, month, fig=None, ax=None, strFullFilename="Monthly_stackedbar.pdf"):
    """Plot the stacked bar graph of category totals of one month"""
    if fig == None:
        fig = plot.figure()
    if ax == None:
        ax = fig.add_axes([0.1, 0.4, 0.8, 0.4])

    keys = list()
    values = list()
    ExpensesSum = np.sum(list(category_totals.values()))

    for key in category_totals.keys():
        if 100*float(category_totals[key])/ExpensesSum > 0:
            keys.append(key)
            values.append(category_totals[key])
        elif category_totals[key] == 0:
            # print("Ignoring unused category", key)
            pass

    labels = ["%s:R%s" % (keys[x], format(values[x],",.2f").replace(",", " ")) for x in range(len(keys))]
    
    bottom_value = 0

    bars = list()
    
    print(keys)
    for i in range(len(keys)):
        key = keys[i]
        bars.append(ax.bar(index, values[i], bottom=bottom_value, color=category_to_colour[key]))
        bottom_value += values[i]

    custom_lines = list()
    custom_labels = list()
    for category in categories:
        custom_lines.append(Line2D([0], [0], 
                            color=category_to_colour[category], 
                            lw=4))
        custom_labels.append(category)

    fig.legend(custom_lines, custom_labels,
                bbox_to_anchor=(0.1, 0.1, 0.8, 0.5),
                ncol=2)

    strDirectory, strFilename = os.path.split(strFullFilename)

    title_text = re.sub(".csv", "", strFullFilename)
    title_text = re.sub("_raw", "", title_text)
    title_text = re.sub("_transaksies", "", title_text)
    plot.title(title_text)
    strPlotSavePath = re.sub(".csv", "_barstack.pdf", strFilename)
    strPlotSaveDirectory = os.path.join(strDirectory, "plots")
    strPlotSavePath = os.path.join(strPlotSaveDirectory, strPlotSavePath)
    plot.grid(which='major', alpha=0.3)
    plot.savefig(strPlotSavePath)
    return fig, ax

class MonthStackedBarGraph():
    def __init__(self):
        self.vstrMonths = list()
        self.fig = None
        self.ax = None

    def PlotStackedBar(self, category_totals, iIndex, strMonthName):
        self.vstrMonths.append(strMonthName)
        self.fig, self.ax = plot_stackedbargraph(category_totals, iIndex, strMonthName, self.fig, self.ax)
        self.ax.set_xticks(range(len(self.vstrMonths)))
        self.ax.set_xticklabels(self.vstrMonths)

def PlotStackedBarFilename(strFoldername):
    strFullFilename = os.path.join(strFoldername, "MonthSummary.txt")
    MonthGraph = MonthStackedBarGraph()

    if os.stat(strFullFilename).st_size <= 2:
        print("No values in MonthSummary.txt")
        return

    with open(strFullFilename, 'r') as summary_file:
        contents = summary_file.read()
        monthly_summary = json.loads(contents)

    months = list(monthly_summary.keys())
    # print(months)
    months.sort(key = lambda date: datetime.strptime(date[0:7], "%b%Y"))
    # print(months)

    fig = None
    ax = None
    for i in range(len(months)):
        month = months[i]
        print(month[0:7])
        category_totals = monthly_summary[month]
        for key in category_totals:
            category_totals[key] = -1*category_totals[key]
        MonthGraph.PlotStackedBar(category_totals, i, month)
        print(category_totals)

    plot.show()

def main():
    PlotStackedBarFilename("")

if __name__ == '__main__':
    main()
