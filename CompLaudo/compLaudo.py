###-------------------------------------------------------------------------------------------------------------
'''
compLaudo v0.0.2c
        - função geraThumbs implementada e testada.
        
compLaudo v0.0.2d
        - Remodelagem do código criando a classe compLaudo
        - Testes da remodelagem

compLaudo v0.0.3a
        - Criar cópia de backup da pasta de entrada
        - Varrer a pasta de entrada e fazer o que segue:
            - Mapear todas as pastas onde existem arquivos de video (pastas_video) 
            - Para cada pasta_video, criar thumbs em pasta temporária
            - Apagar a pasta origem e renomear a pasta equivalente com os thumbs
            - Mapear todas as páginas html
            - Modificar os links de videos dos html mapeados para os thumbs 
            
'''
###-------------------------------------------------------------------------------------------------------------

import ffmpy
import glob
import sys
import os
import subprocess
import datetime
import shutil
from bs4 import BeautifulSoup
from shutil import copy2

THUMBS_X = 5
THUMBS_Y = 5

VIDEO_TYPES = ["MP4", "3GP", "MOV"] 

def getNumFrames(fileName):
    retval = 0
    print ("Recuperando nframes de: "+fileName, end='')
    p = subprocess.Popen('ffprobe -show_streams "'+fileName+'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in p.stdout:
        fields = line.decode().split('=')
        if fields[0] == 'nb_frames':
            retval = int (fields[1])
            break
#    p.wait()
    print (" => "+str(retval))
    return retval

def getExt(arq):
    indext = arq.upper().rfind(".")
    ext = arq[indext+1:].upper()
    return ext

def processa_HTML_videos(html_page):
    with open(html_page,"r") as f:
        soup = BeautifulSoup(f)  
    soup.prettify()

    for tag in soup.find_all("a"):
        if getExt(tag['href']) in VIDEO_TYPES: 
            tag['href'] = str(tag['href']) + "_thumbs.jpg"
                
    with open(html_page+"_processada.html","w") as f:
        f.write(str(soup))  

def geraThumbs(dirOrigem, dirDestino):
    files = [file for file in glob.glob(dirOrigem+"/**", recursive=True)]
    posDP = dirOrigem.find(":")
    if posDP < 0:
        posDP = 0

    print ("Convertendo "+str(len(files))+" arquivos - Iniciado em:"+str(datetime.datetime.now()))
    nfile = 1
    for fileName in files:
        newName = fileName.replace(dirOrigem, dirDestino)
        os.makedirs(os.path.dirname(newName), exist_ok=True)
        newNameTmp = newName+"_thumbs.jpg"
        processed = False    
        print ("Convertendo de: "+fileName+" para "+newNameTmp)
        try: 
            ext = getExt(fileName)
            if os.path.isfile(fileName) and  ext in VIDEO_TYPES:
                nFrames = getNumFrames(fileName)
                if nFrames > (THUMBS_X * THUMBS_Y):
                    outputpars = '-loglevel panic -y -vf "select=not(mod(n\,'+str(nFrames // 25) 
                    outputpars+= ')),scale=320:240,tile='+str(THUMBS_X)+'+'+str(THUMBS_Y)+'" -frames 1'
                    ff = ffmpy.FFmpeg(inputs={fileName:None}, 
                              outputs={newNameTmp: outputpars})
                    ff.run()
                    processed = True
        except:
            print ("Erro no processamento de: "+str(sys.exc_info()))
        
        print (str(nfile)+"/"+str(len(files)), end=' ')
        if processed:
            size = os.stat(fileName).st_size
            newsize = os.stat(newNameTmp).st_size
            print (fileName+": "+str(size)+
                   " -> "+str(newsize)+ " "+newNameTmp, end='') 
        elif os.path.isfile(fileName) :
            copy2(fileName,newName)
#            os.replace(fileName,newName)   
        
    print()
    print ("Arquivos convertidos. Finalizado em:"+str(datetime.datetime.now()))

if len(sys.argv) < 4:
    print ("uso: python "+sys.argv[0]+" dir_entrada dir_saida")
    sys.exit(1)

geraThumbs(sys.argv[1], sys.argv[2])
processa_HTML_videos(sys.argv[3])
    
#ffmpeg -y -i input -c:v libx264 -preset medium -b:v 555k -pass 1 -an -f mp4 /dev/null && \
#ffmpeg -i input -c:v libx264 -preset medium -b:v 555k -pass 2 -c:a libfdk_aac -b:a 128k output.mp4        
# -s 640x480 -b:v 512k -vcodec mpeg1video -acodec copy
#        ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -fs "+str(newSize)})
#        ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -crf 45 "})
