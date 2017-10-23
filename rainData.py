# import libraries
import os, datetime, shutil, sys, csv

# check last modified dates
def errorCheck(path):
    
    os.chdir(path)
    files = os.listdir(path)

    year, month, day = getDate(0)

    wDate = 0;
    for f in files:
        time = os.path.getmtime(f)
        date = datetime.datetime.fromtimestamp(time)
        if date.day != int(day):
            wDate += 1
        if wDate > 1:
            print("Error with last modified dates, contact Robert!")
            sys.exit("Error with last modified dates!")

    if len(files) != 27:
        print("There are not 27 files, contact Robert!")
        sys.exit("There are not 27 files!")

# create file with yesterday's date as name
def createNewFolder(path):
    
    year, month, day = getDate(1)

    # format month and day
    if len(month) == 1: month = "0" + month
    if len(day) == 1: day = "0" + day
    
    os.chdir(path)

    title = year + "." + month + "." + day
    if not os.path.exists(title):
        os.mkdir(title)
    else:
        print("Error: Folder already exists!")
        sys.exit("Error: Folder already exists!")

    return title

# copy files
def copyFiles(src, dest):
    
    srcFiles = os.listdir(src)
    for file in srcFiles:
        fullName = os.path.join(src, file)
        if (os.path.isfile(fullName)):
            shutil.copy(fullName, dest)

def convertFiles(path):
    
    renameFiles = os.listdir(path)
    os.chdir(path)
    for file in renameFiles:
        base = os.path.splitext(file)[0]
        os.rename(file, base + ".csv")

def printResults(rpath, wpath):

    os.chdir(rpath)
    
    d = createDict()
    l = [[] for i in range(27)]

    # check if you want to include more than one day
    days = input("Enter amount of days you're recording: ")
    while (not days.isdigit() or int(days) < 1):
        days = input("Please enter an integer: ")
    days = int(days)
    rows = days*24

    index = 0
    for key in d:
        with open(d[key], 'rt') as file:
            reader = csv.reader(file, delimiter = ',')
            reader = list(reader)
            length = len(reader)
            sum = 0
            for row in reader[length-rows:length]:
                sum += float(row[len(row)-1])
            l[index].append(key)
            l[index].append(round(sum, 2))
            l[index].append(row[0])
            index += 1
        file.close()
        
    os.chdir(wpath)
    with open('rain.csv', 'w', newline='') as f:
        write = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(0, len(l)):
            write.writerow(l[x])
        f.close()

#get yesterday's date
def getDate(delta):
    
    d = datetime.datetime.now()
    date = d - datetime.timedelta(delta)
    
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)

    return year, month, day

# create dictionary to match maximo name with file
def createDict():
    fileDict = {'RGA000024' : 'RGALLEN_Table1.csv',
                'RGA000018' : 'RGFARMERSVILLE_Table1.csv',
                'RGA000023' : 'RGRICHARDSON_Table1.csv',
                'RGA000016' : 'RGFORNEY_Table1.csv',
                'RGA000025' : 'RGGARLAND_Table1.csv',
                'RGA000017' : 'RGMCKINNEY_Table1.csv',
                'RGA000021' : 'RGWYLIE_Table1.csv',
                'RGA000022' : 'RGPLANO_Table1.csv',
                'RGA000026' : 'RGPRINCETON_Table1.csv',
                'RGA000019' : 'RGROCKWALL_Table1.csv',
                'RGA000027' : 'RGROYSE_Table1.csv',
                'RGA000020' : 'RGMESQUITE_Table1.csv',
                'RGA000015' : '121LANDFILL_Table1.csv',
                'RGA000009' : 'ALLEN_Table1.csv',
                'RGA000003' : 'FARMERSVILLE_Table1.csv',
                'RGA000001' : 'FORNEY_Table1.csv',
                'RGA000010' : 'GARLAND_Table1.csv',
                'RGA000014' : 'WETLAND_Table1.csv',
                'RGA000002' : 'MCKINNEY_Table1.csv',
                'RGA000007' : 'PLANO_Table1.csv',
                'RGA000011' : 'PRINCETON_Table1.csv',
                'RGA000008' : 'RICHARDSON_Table1.csv',
                'RGA000013' : 'TAWAKONI_Table1.csv',
                'RGA000005' : 'MESQUITE_Table1.csv',
                'RGA000004' : 'ROCKWALL_Table1.csv',
                'RGA000012' : 'RGROYSE_Table1.csv',
                'RGA000006' : 'WYLIE_Table1.csv'}

    return fileDict
        
def main():
    
    rpath = "S:/"
    dpath = "S:/"
    wpath = "H:"

    errorCheck(dpath)

    title = createNewFolder(rpath)
    rpath += "/" + title
    
    copyFiles(dpath, rpath)
    convertFiles(rpath)

    printResults(rpath, wpath)
    
main()
