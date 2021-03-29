import re
import collections
from pathlib import Path

def write_categories(filename, categories_list, match_strings_dict):
    with open(filename, 'w') as categories_file:
        for item in categories_list:
            categories_file.write("[" + item + "]\n")

            for match_item in match_strings_dict[item]:
                categories_file.write(match_item+", ")

            categories_file.write("\n\n")


def read_categories(filename=r"C:\Users\danie\Development\StateAnalise\categories1.txt"):

    with open(filename, 'r') as categories_file:
        data = categories_file.readlines()

    categories_list = list()
    match_strings_dict = dict()

    for i in range(len(data)):
        if re.match(r"\[\w+(\s+\w+)*\]", data[i]):
            category_name = re.sub(r"(\[|\]|\n)", "", data[i], count=3)
            # print("Category found:", category_name)

            if len(data[i+1]) == 0 or re.search(r"\w+(\s+\w+)*(,|\n|\Z)", data[i+1]) == None:
                print("Empty category", category_name)
                continue

            match_strings_dict[category_name] = list()
            for item in re.finditer(r"\w+(\s+\w+)*(,|\n|\Z)", data[i+1]):
                item_text = re.sub(",", "", item[0])
                item_text = re.sub("\n", "", item_text)
                # print(item_text)
                match_strings_dict[category_name].append(item_text)

            categories_list.append(category_name)

    return categories_list, match_strings_dict


def main():
    categories = ["Kos", "Apteek", "Parkering", "Brandstof", "Hardeware", "Sport toerusting"]
    match_strings_dict = dict()
    match_strings_dict["Kos"] = ["SPAR", "Spar", "CHECKERS", "BIRDSTRAAT SLAGHUIS", "WOOLWORTHS", "FLM", "PNP", "THE BOER AND BUTCH", "WHALE COAST SEAFOODS"]
    match_strings_dict["Apteek"] = ["APTEEK", "PHARMACY", "STELKOR", "MEDIHEALTH", "MEDIRITE"]
    match_strings_dict["Parkering"] = ["ST PARK SOLUTIONS", "PARKING"]
    match_strings_dict["Brandstof"] = ["KAAP AGRI FUEL"]
    match_strings_dict["Hardeware"] = ["BUILDERS EXP", "BUCO HERMANUS"]
    match_strings_dict["Sport toerusting"] = ["SPORTSMANS", "CAPE UNION MART"]

    # write_categories("categories1_test.txt", categories, match_strings_dict)

    # categories_read, match_string_read = read_categories("categories1_test.txt")
    categories_read, match_string_read = read_categories("categories1.txt")

    print("Categories_read:", categories_read)
    print("\nCategories_read == categories: " + 
        str(collections.Counter(categories) == collections.Counter(categories_read)))

    print("\nMatch_string_read:", match_string_read)
    print("\nmatch_strings_dict == match_string_read: " + 
        str(collections.Counter(match_strings_dict) == collections.Counter(match_string_read)))

if __name__ == '__main__':
    main()