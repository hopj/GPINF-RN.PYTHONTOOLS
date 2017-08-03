import hashlib
import sys
import glob
import os.path

def calcHash (alg, file):
    m = hashlib.new(alg)
    fdin = open (file, "rb")
    for linha in fdin:
        m.update(linha)
    fdin.close()
    return m.hexdigest().upper()

def checkHashWithName(alg, file):
    hash = calcHash (alg, file)
    baseName = os.path.basename(file)
    onlyFileName = os.path.splitext(baseName)[0]
    return (hash == onlyFileName.upper(), hash,  baseName)


hashes = ["-sha1", "-md5",  "-sha256"]

if len(sys.argv) != 3:
    print ("Uso: python "+sys.argv[0]+" <hashAlg> dirToValidate")
    
if sys.argv[1].lower() not in hashes:
    print ("Hashes suportados: "+hashes)
    sys.exit(-1)

print ("Localizando arquivos")
files = [file for file in glob.glob(sys.argv[2]+"/**", recursive=True)]
print ("Iniciando cálculo de hashes")

for file in files:
    if os.path.isfile(file):
        (checked, hash, fileName) = checkHashWithName (sys.argv[1].lower()[1:], file)
        if not checked:
            print ("\n******* ERROR ***** in file: "+file+" -> "+sys.argv[1][1:]+": "+ hash)
        else:
            print (end=".")
        
print ("\nPROCESSO CONCLUÍDO\n")

	