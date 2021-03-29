import csv
import re
import sys
from datetime import datetime
import os
from pathlib import Path
import pandas as pd

#from pdfminer.high_level import extract_text
import pdfplumber

currency_match_string = r"(\bZA\b|\bIE\b|\bDE\b|\bUS\b|\bGB\b|\bHK\b|\bNL\b|\bLU\b)"

def ConvertDebietToCSV(strFilename):

    print("Filename:", strFilename)

    text = ""

    with pdfplumber.open(strFilename) as pdf:
        for page in pdf.pages:
#            print(page.extract_text())
            if (page.extract_text() != None):
                text += page.extract_text()

#    text = extract_text(strFilename)
    text_output_filename = re.sub(".pdf", "_raw.txt", strFilename)

    with open(text_output_filename, 'w') as output_file:
        output_file.write(text)


    begin_saldo_line = ""
    transaction_lines = list()
    # nonConformantTransactions_lines = list()

    data = text.splitlines()

    #print(data)
    match_text = ""
    matching = False
    matchline_count = 0

    for i in range(len(data)):
        line = data[i]
        # print(line)

        begin_saldo_match = re.search(r"\d{1,2}/\d{2}/\d{4}.*SALDO OORGEDRA.*\d*,?\d+\.\d{2}\s*",
                            line)

        if begin_saldo_match == None:
            begin_saldo_match = re.search(r"\d{1,2}/\d{2}/\d{4}.*Saldo (O|o)orgedra.*\d*,?\d+\.\d{2}\s*", line)
        if begin_saldo_match != None:
            print(begin_saldo_match[0])
            begin_saldo_line = begin_saldo_match[0]


        match = re.search(r"\d{1,2}/\d{2}/\d{4}.*(\d*,?\d+\.\d{2}\s*){2,3}",
                            line)
        if match != None:
            match_text = match[0]
            matching = True
            transaction_lines.append(match_text)

        #Check if the next line is also part of the transaction
        elif matching:
            match_text += line
            # print(match_text)
            matchline_count+=1
            transaction_lines[-1] = match_text

            if matchline_count > 3:
                matching = False

        else:
            # If we stopped matching, store transactions
            if matching == True:
                transaction_lines.append(match_text)

            matching = False
            continue
    
    if begin_saldo_line == "":
        print("Kon nie \"SALDO OORGEDRA\" of \"Saldo Oorgedra\" vind nie")
        return

    transaction_strFilename = re.sub(".pdf", "_rawtransaksies.txt", strFilename)
    print(transaction_strFilename)
    with open(transaction_strFilename, 'w') as transaction_file:
        for line in transaction_lines:
            transaction_file.write(line + "\n")
            # print(line, "\n")

    column_names = ["Tran Datum","Verwerk datum","Beskrywing","Eenheid","Bedrag"]
    transaction_df = pd.DataFrame(columns=column_names)
    prev_saldo_string = re.search(r"\d*,?\d+\.\d{2}", begin_saldo_line)[0]
    prev_saldo_string = prev_saldo_string.replace(",", "")    
    prev_saldo = float(prev_saldo_string)
    # Format into transaksies.csv format
    for line in transaction_lines:
        columns_list = list()
        datum = re.search(r"\d{1,2}/\d{2}/\d{4}", line)[0]
        # print("datum:", datum.split(" "))
        date_obj = datetime.strptime(datum, "%d/%m/%Y")

        bedrag_matches = re.findall(r"\d*,?\d+\.\d{2}", line)
        # print("bedrag_matches", bedrag_matches)
        transaksie_bedrag = bedrag_matches[len(bedrag_matches)-2]
        saldo_bedrag_string = bedrag_matches[len(bedrag_matches)-1]
        saldo_bedrag_string = saldo_bedrag_string.replace(",", "")
        saldo_bedrag = float(saldo_bedrag_string)

        difference = prev_saldo - saldo_bedrag
        # print("transaksie_bedrag, difference", transaksie_bedrag, difference)
        prev_saldo = saldo_bedrag

        # print("transaksie_bedrag", transaksie_bedrag)
        # print("saldo_bedrag", saldo_bedrag)

        # Clean up the remaining line
        remaining_line = line[:]
        remaining_line = re.sub(datum, "", remaining_line)
        for bedrag in bedrag_matches:
            # print(bedrag)
            remaining_line = remaining_line.replace(bedrag, "", 1)
        
        remaining_line = re.sub(r"\s{2,}", " ", remaining_line)
        remaining_line = remaining_line.replace("VEREFFENIN", "")
        remaining_line = remaining_line.replace("IBANK", "")
        remaining_line = remaining_line.replace("ABSA BANK", "")
        # print(" ")
        # print(line)
        # print(remaining_line)


        # If this is a true expense
        if difference > 0.0:
            # Add trans date in "%d %MON" format
            columns_list.append(date_obj)
            #Add process date, similar to trans date because its a debit card
            columns_list.append(date_obj)
            #Add description
            columns_list.append(remaining_line)
            #Assuming all values are in Rands
            columns_list.append("ZA")
            columns_list.append("%.2f" % difference)

            # Add to pandas Dataframe as well
            # print(columns_list)
            column_series = pd.Series(columns_list, index=transaction_df.columns)
            # print(column_series)
            transaction_df = transaction_df.append(column_series, ignore_index=True)
            # print(transaction_df)

    if strFilename.find(".pdf") == -1:
        print("Should have opened a PDF file")
        exit(0)

    transaction_csv_strFilename_pandas = re.sub(".pdf", "_transaksies.csv", strFilename)
    transaction_df.to_csv(transaction_csv_strFilename_pandas, float_format="%2.2f")

    month_year = re.search(r"\w{3}\d{4}", transaction_strFilename)
    if month_year:
        print("Month year found:", month_year)

    else:
        print(r"strFilename not in a format as expected, please use <Month>{3}<Year>{4}. Exiting.")
        exit(0)

    AlleTransaksies_path = str(month_year[0]) + '_together.csv'
    AlleTransaksies_path = os.path.join(os.path.dirname(transaction_csv_strFilename_pandas), "../AlleTransaksies/", AlleTransaksies_path)
    try:
        read_transaction_df = pd.read_csv(AlleTransaksies_path, index_col=0, parse_dates=["Tran Datum", "Verwerk datum"])
#        print(read_transaction_df)
#        print("read_transaction_df", read_transaction_df.info())
#        print("transaction_df", transaction_df.info())
        transaction_df = transaction_df.append(read_transaction_df, ignore_index=True)
#        print(transaction_df)
        transaction_df = transaction_df.drop_duplicates()
        transaction_df = transaction_df.sort_values(by="Tran Datum", ignore_index=True)
#        print(transaction_df)
        print("Appended together transactions")

    except FileNotFoundError:
        print(AlleTransaksies_path + ' not found')

    transaction_df.to_csv(AlleTransaksies_path, float_format="%2.2f")

def main():
    if len(sys.argv) < 2:
        print("Usage: convert_pdf2csv.py <filename.pdf>")
        exit(0)

    strFilename = sys.argv[1]
    ConvertDebietToCSV(strFilename)

if __name__ == '__main__':
    main()
