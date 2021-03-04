#extract_timeseries.py

# from github import Github
# from datetime import datetime, timedelta, timezone
import sys
import csv
import os

def generate_timeseries(input, versions, output):

    results = dict()
    # metrics = ["cbo", "fanin", "fanout", "dit", "noc", "lcom", "noa", "nom"]
    metrics = ["cbo", "fanin", "fanout", "wmc", "dit", "noc", "rfc", "lcom", "tcc", "lcc", "totalMethodsQty", "staticMethodsQty", "publicMethodsQty", "privateMethodsQty", "protectedMethodsQty", "defaultMethodsQty", "abstractMethodsQty", "finalMethodsQty", "synchronizedMethodsQty", "totalFieldsQty", "staticFieldsQty", "publicFieldsQty", "privateFieldsQty", "protectedFieldsQty", "defaultFieldsQty", "visibleFieldsQty", "finalFieldsQty", "synchronizedFieldsQty", "nosi", "loc", "returnQty", "loopQty", "comparisonsQty", "tryCatchQty", "parenthesizedExpsQty", "stringLiteralsQty", "numbersQty", "assignmentsQty", "mathOperationsQty", "variablesQty", "maxNestedBlocksQty", "anonymousClassesQty", "innerClassesQty", "lambdasQty", "uniqueWordsQty", "modifiers", "logStatementsQty"]
    # indexColuns = [4, 5, 6, 8, 9, 12, 24, 15]
    indexColuns = [4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

    print("---------------------------------- Starting the process of reading and exporting of the project timeseries release ----------------------------------\n")

    for release in list(range(int(versions))):
    
        release_index = release + 1
        path = input + "/" + str(release_index) + "/class.csv" if not input.endswith('/') else input + str(release_index) + "/class.csv"
        
        print("Reading release " + str(release_index) + " from the project...")

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:

                    package_test = "." + row[1].rsplit(", ", 1)[0] + "."
                    if (".test." not in package_test.lower()) and (".tests." not in package_test.lower()):
                    
                        if row[1] not in results:
                            results[row[1]] = dict()
                        
                        results[row[1]][release_index] = dict()

                        for i in list(range(len(indexColuns))):
                            results[row[1]][release_index][metrics[i]] = row[indexColuns[i]]

                    # break
                line_count = line_count + 1

    print(len(results.keys()))

    print("\nFinished reading process!")

    print("\nStarting exporting process...")

    name_project = input.rsplit("/", 1)[1] if not input.endswith('/') else input.rsplit("/", 2)[1]
    timeseries_output = output + "/" + name_project + "/" if not input.endswith('/') else output + name_project + "/"

    if not os.path.exists(timeseries_output):
            os.makedirs(timeseries_output)

    for i in list(range(len(indexColuns))):

        print("Exporting " + metrics[i].upper() + " timeseries...")
        
        csv_name = timeseries_output + metrics[i] + ".csv"

        with open(csv_name, mode='w') as timeserie_file:
            writer = csv.writer(timeserie_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for key in results:
                line = [key]
                
                for release in list(range(int(versions))):

                    release_index = release + 1
                    if release_index in results[key]:
                        line.append(results[key][release_index][metrics[i]])
                    else: 
                        if metrics[i] == 'lcom':
                            line.append("-1.0")
                        else:
                            line.append("-1")
                
                writer.writerow(line)

    print("\nFinished exporting process!")
            

            # employee_writer.writerow(['John Smith', 'Accounting', 'November'])
            # employee_writer.writerow(['Erica Meyers', 'IT', 'March'])

    # print("---------------------------------- Starting the process of reading and exporting of the project timeseries release ----------------------------------\n")

    # print(input + "\n")
    # print(str(versions) + "\n")
    # print(input + "\n")



if __name__ == '__main__':
    args = sys.argv

    if len(args) != 4:
        print("Usage python3 extract_timeseries.py <directory of the versions with system metrics> <nº of versions> <path to save the output files>")
    else:
        generate_timeseries(args[1], args[2], args[3])
