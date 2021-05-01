import json
import os.path
import pandas as pd
import re

def CompareBudgetWithActuals(strActualsFilename, strBudgetFilename="Budget.txt"):
    budget_dict = JSONFileToDict(strBudgetFilename)["Budget"]
    for key in budget_dict:
        print(key, ":", budget_dict[key])

    strDirectory, strFilename = os.path.split(strActualsFilename)
    strMonthSummaryFilename = os.path.join(strDirectory, "MonthSummary.txt")
    actuals_dict = JSONFileToDict(strMonthSummaryFilename)[strFilename]
    print(actuals_dict)

    dfBudgetActualsDiff = pd.DataFrame(columns=["Item", "Budget", "Actual", "Difference"])

    for key in actuals_dict.keys():
        print("%s: Budget %4.2f, Actual %4.2f, Diff %4.2f" % (key, budget_dict[key], -1*actuals_dict[key], budget_dict[key]+actuals_dict[key]))
        dfBudgetActualsDiff = dfBudgetActualsDiff.append({"Item":key, "Budget":budget_dict[key], "Actual":-1*actuals_dict[key], "Difference":budget_dict[key]+actuals_dict[key]}, ignore_index=True)

    strOutputFilename = re.sub(".csv", "_budgetdiff.csv", strFilename)
    strOutputFilename = os.path.join(strDirectory, strOutputFilename)

    dfBudgetActualsDiff.to_csv(strOutputFilename)

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
    print(json.dumps(budget_dict, indent=4, sort_keys=True))
    with open("Budget.txt", 'r') as budget_file:
        file_contents = budget_file.read()
        current_json = json.loads(file_contents)
        print(current_json)

if __name__ == "__main__":
     PrintBudget()
