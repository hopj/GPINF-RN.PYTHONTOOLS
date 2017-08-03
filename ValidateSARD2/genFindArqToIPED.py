import sys

fields = ["caminho", "hash", "tamanho"]

def extractFieldsInCSVLines(fileName, fields):
    fdin = open (fileName, "r", encoding="UTF-8")
    header = fdin.readline()[1:-3].lower().split('";"')
    allLinesFields = []
    for line in fdin:        
        fieldsInLine = line[1:-3].replace('"""";""""', '""""-""""'). split('";"')
        fieldsExtrated=[]
        for field in fields:
            fieldsExtrated.append(fieldsInLine[header.index(field)])

        allLinesFields.append(tuple(fieldsExtrated))
    fdin.close()
    return allLinesFields

def generateIPEDFindFile(fileName, fields, allLinesFields):
    fdout = open (fileName, "w", encoding="latin1")
    fdout.write('hash:"0000" ')  
    for line in allLinesFields:
        fdout.write('|| ( {}:"{}" '.format(fields[0], line[0]))          
        ind = 1
        while ind < len(fields):
            fdout.write(' && {}:"{}" '.format(fields[ind], line[ind]))     
            ind += 1      
        fdout.write(')') 
    fdout.close()   
        
def checkIfRequestedIsInOriginal(requested, original):
    allright = True
    for file in requested:
        if file not in original:
            print ("arquivo não confere com o original: "+str(file))
            allright = False
    return allright
    
allLinesFieldsRequested = extractFieldsInCSVLines(sys.argv[1], fields)
allLinesFieldsOriginal = extractFieldsInCSVLines(sys.argv[2], fields)

if not checkIfRequestedIsInOriginal(allLinesFieldsRequested, allLinesFieldsOriginal):
    print("Nem todos os arquivos na lista selecionada estão na lista original")
else:
    print("Todos os arquivos na lista selecionada estão na lista original")
    
generateIPEDFindFile(sys.argv[1]+"_files_toFind_iped.txt", fields, allLinesFieldsRequested)

