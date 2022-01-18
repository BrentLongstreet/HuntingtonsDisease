import os
import glob
import csv


start = os.path.dirname(__file__)

def updatePenetrance(startDir, dir, region, site):
    os.chdir(dir)
    dnaSequence = glob.glob('*.txt')
    spot = -1
    count_dic = {"ACG" : 0, "Max" : 0, "Total" : 0}

    for index in range(len(dnaSequence)-1):
        spot += 1
        f = open(dnaSequence[index], 'r')
        dna = f.read()
        for x in [dna[i:i+3] for i in range(0, len(dna),3)]:
            if x == "CAG":
                if count_dic["ACG"] < count_dic["Max"] :
                    count_dic["ACG"] += 1

                elif count_dic["ACG"] >= count_dic["Max"]:
                    count_dic["ACG"] += 1
                    count_dic["Max"] = count_dic["ACG"]
            else:
                count_dic["ACG"] = 0

        rows = None

        if count_dic["Max"] >= 27 and count_dic["Max"] <= 35:
            g = os.path.splitext(dnaSequence[spot])[0]
            rows = [[g, region, site,'Intermediate']]

        elif count_dic["Max"] >= 36 and count_dic["Max"] <= 39:
            g = os.path.splitext(dnaSequence[spot])[0]
            rows = [[g, region, site,'Reduced Penetrance']]
            

        elif count_dic["Max"] >= 40:
            g = os.path.splitext(dnaSequence[spot])[0]
            rows = [[g, region, site,'Full Penetrance']]
        
        if rows != None:
            writeToCSV(startDir, rows, dir)
            count_dic["Total"] += 1

        count_dic["Max"] = 0
        
    os.chdir(startDir)
    
def writeToCSV(startDir, rows, currentDir):
    os.chdir(startDir)
    with open('disease.csv', 'a',newline='') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        # writing the data rows  
        csvwriter.writerows(rows)
    os.chdir(currentDir)

def Main():
    while True:
        result = input("Enter (S) to start: ").upper()
        if result == "S":
            print("Process Starting...")
            for root, dirs, files in os.walk('.'):
                newRoot = root.replace('.\\', '')
                for dir in dirs:
                    if newRoot[0] == '.':
                        continue
                    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
                    abs_file_path = os.path.join(script_dir, newRoot,dir)
                    region = newRoot.replace('data\\', '')
                    site = dir
                    updatePenetrance(start, abs_file_path, region, site)
            print("Process Completed.... Results saved to disease.csv")
            break
        else:
            print("INVALID INPUT")

Main()
