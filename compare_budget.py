import json
import os.path
import pandas as pd
import re
import sys
from PySide2.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
import numpy as np
from plot_monthly import plt_colours

def CompareBudgetWithActuals(strActualsFilename, strBudgetFilename="Budget.txt"):
    budget_dict = JSONFileToDict(strBudgetFilename)
    print(budget_dict)

    budget_dict = JSONFileToDict(strBudgetFilename)["Budget"]
    for key in budget_dict:
        print(key, ":", budget_dict[key])

    strDirectory, strFilename = os.path.split(strActualsFilename)
    strMonthSummaryFilename = os.path.join(strDirectory, "MonthSummary.txt")
    dictMonthSummary = JSONFileToDict(strMonthSummaryFilename)
    if strFilename in dictMonthSummary:
        actuals_dict = dictMonthSummary[strFilename]
        print(actuals_dict)
    else:
        print("Actual expenses for %s not yet in MonthSummary.txt" % strFilename, file=sys.stderr)
        msg = QMessageBox()
        msg.setText("Error: Actual expenses for %s not yet in MonthSummary.txt. Run Sort Vendor" % strFilename)
        msg.exec_()
        return

    dfBudgetActualsDiff = pd.DataFrame(columns=["Item", "Budget", "Actual", "Difference"])

    for key in actuals_dict.keys():
        print("%s: Budget %4.2f, Actual %4.2f, Diff %4.2f" % (key, budget_dict[key], -1*actuals_dict[key], budget_dict[key]+actuals_dict[key]))
        dfBudgetActualsDiff = dfBudgetActualsDiff.append({"Item":key, "Budget":budget_dict[key], "Actual":-1*actuals_dict[key], "Difference":budget_dict[key]+actuals_dict[key]}, ignore_index=True)

    strOutputFilename = re.sub(".csv", "_budgetdiff.csv", strFilename)
    strOutputFilename = os.path.join(strDirectory, strOutputFilename)

    dfBudgetActualsDiff.to_csv(strOutputFilename)
    PlotBudgetActualsDiff(dfBudgetActualsDiff, strFilename)

def JSONFileToDict(strFilename):
    with open(strFilename, 'r') as JSONfile:
        file_contents = JSONfile.read()
        current_json = json.loads(file_contents)
#        print(current_json)
        return current_json

def PrintBudget():
    budget_dict = dict()
    budget_dict["Budget"] = dict()
    budget_dict["Budget"]["Bank"] = 0.0
#    print(json.dumps(budget_dict, indent=4, sort_keys=True))
    with open("Budget.txt", 'r') as budget_file:
        file_contents = budget_file.read()
        current_json = json.loads(file_contents)
#        print(current_json)

def PlotBudgetActualsDiff(dfBudgetActualsDiff, strPlotTitle):
    dfBudgetActualsExpenses = dfBudgetActualsDiff[dfBudgetActualsDiff["Actual"] > 0]
    dfBudgetActualsIncomes = dfBudgetActualsDiff[dfBudgetActualsDiff["Actual"] < 0]
    vRange = range(len(dfBudgetActualsExpenses["Item"]))
    vActualsRange = np.arange(0.4,len(dfBudgetActualsExpenses["Item"]), 1)
    print(dfBudgetActualsExpenses)
    ExpensesSum = dfBudgetActualsExpenses["Actual"].sum()
    IncomesSum = -1*dfBudgetActualsIncomes["Actual"].sum()
    print("Expenses Sum %2.2f" % ExpensesSum)
    print("Incomes Sum %2.2f" % IncomesSum)
    Indexes = dfBudgetActualsExpenses.index
    plt.bar(vRange, dfBudgetActualsExpenses["Budget"], width=0.4, color=plt_colours[0], label="Budget")
    for x_index in vRange:
        Index = Indexes[x_index]
        fYValue = dfBudgetActualsExpenses["Budget"][Index]
        strYValue = "%2.0f" % fYValue
        plt.text(x_index, fYValue, strYValue, color=plt_colours[0], ha='center')
    plt.bar(vActualsRange, dfBudgetActualsExpenses["Actual"], width=0.4, color=plt_colours[2], label="Actual")
    for x_index in vRange:
        Index = Indexes[x_index]
        fYValue = dfBudgetActualsExpenses["Actual"][Index]
        strYValue = "%2.0f" % fYValue
        plt.text(x_index + 0.4, fYValue, strYValue, color=plt_colours[2], ha='center')
    plt.xticks(vRange, dfBudgetActualsExpenses["Item"], rotation=90)
    plt.legend()

    plt.title(strPlotTitle + ": Actuals vs Budget\n" + "Incomes R%2.2f Expenses R%2.2f" % (IncomesSum, ExpensesSum))
    plt.subplots_adjust(top=0.9, bottom=0.4)
    plt.show()


if __name__ == "__main__":
     PrintBudget()
