# import libraries
import os, datetime, shutil, sys, csv

# delete old file and create new one
def createNewFolder(path):
    
    os.chdir(path)
    title = 'Rain Data'
    if os.path.exists(title):
        rmpath = path + "/" + title
        shutil.rmtree(rmpath)
    os.mkdir(title)

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
    rows = 24

    index = 0
    for key in d:
        with open(d[key], 'rt') as file:
            reader = csv.reader(file, delimiter = ',')
            reader = list(reader)
            length = len(reader)
            sum = 0
            for row in reader[length-rows:length]:
                sum += float(row[len(row)-1])
            #don't add row if newreadingdate isn't today's date
            if datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').date() != datetime.date.today():
                continue
            else:
                l[index].append(key)
                l[index].append(round(sum, 2))

                #modify date for maximo integration
                modDate = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')
                l[index].append(modDate)
                
                l[index].append('RAIN')
                l[index].append('1000')
                
                index += 1
        file.close()
        
    os.chdir(wpath)
    with open('rain.csv', 'w', newline='') as f:
        write = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        write.writerow(['FLAT', 'MXMETERInterface', 'AddChange', 'EN'])
        write.writerow(['ASSETNUM', 'NEWREADING', 'NEWREADINGDATE', 'METERNAME', 'SITEID'])
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
    fileDict = {'xxxx00024' : 'xx_Table1.csv',
                'xxxx00018' : 'xx_Table1.csv',
                'xxxx00023' : 'xx_Table1.csv',
                'xxxx00016' : 'xx_Table1.csv',
                'xxxx00025' : 'xx_Table1.csv',
                'xxxx00017' : 'xx_Table1.csv',
                'xxxx00021' : 'xx_Table1.csv',
                'xxxx00022' : 'xx_Table1.csv',
                'xxxx00026' : 'xx_Table1.csv',
                'xxxx00019' : 'xx_Table1.csv',
                'xxxx00027' : 'xx_Table1.csv',
                'xxxx00020' : 'xx_Table1.csv',
                'xxxx00015' : 'xx_Table1.csv',
                'xxxx00009' : 'xx_Table1.csv',
                'xxxx00003' : 'xx_Table1.csv',
                'xxxx00001' : 'xx_Table1.csv',
                'xxxx00010' : 'xx_Table1.csv',
                'xxxx00014' : 'xx_Table1.csv',
                'xxxx00002' : 'xx_Table1.csv',
                'xxxx00007' : 'xx_Table1.csv',
                'xxxx00011' : 'xx_Table1.csv',
                'xxxx00008' : 'xx_Table1.csv',
                'xxxx00013' : 'xx_Table1.csv',
                'xxxx00005' : 'xx_Table1.csv',
                'xxxx00004' : 'xx_Table1.csv',
                'xxxx00012' : 'xx_Table1.csv',
                'xxxx00006' : 'xx_Table1.csv'}

    return fileDict
        
def main():
    
    rpath = "S:/"
    dpath = "S:/"
    wpath = "H:"

    title = createNewFolder(rpath)
    rpath += "/" + title
    
    copyFiles(dpath, rpath)
    convertFiles(rpath)

    printResults(rpath, wpath)
    
main()
