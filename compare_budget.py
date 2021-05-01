import pandas as pd

def CompareBudgetWithActuals(strActualsFilename, strOutputFilename, strBudgetFilename="Budget.csv"):
    budget_values = pd.read_csv(strBudgetFilename)
    actuals_values = pd.read_csv(strActualsFilename)

    for key in budget_values:
        print(budget_values[budget_values["category"] == key])


def PrintBudget():
    Inkopies	R3,500.00
    Irene pille	R167.39
    Kuns klas	R430.00
    Brandstof	R900.00
    Netflix	R139.00
    Rachel Patreon	R32.00
    Bankkostes	R274.00
    Mweb Internet	R639.00
    Medies Irene	R1,400.00
    Huur	R9,500.00
    Elektrisiteit	R500.00
    Discovery Vitality	R290.00
    Belegging	R4,500.00
    Apple Music	R80.00


 if __name__ == "__main__":
     PrintBudget()
