'''
-------------------------------------------------------------------------------------------------------------
compLaudo v0.0.2c1
        - função geraThumbs implementada e testada.
        
compLaudo v0.0.2d
        - Remodelagem do código criando a classe compLaudo
        - Testes da remodelagem

compLaudo v0.0.3a
        - Varrer a pasta de entrada e fazer o que segue:
            - Mapear todas as pastas onde existem arquivos de video (pastas_video) 
            - Para cada pasta_video, criar thumbs em pasta temporária
            - Apagar a pasta origem e renomear a pasta equivalente com os thumbs
            - Mapear todas as páginas html
            - Modificar os links de videos dos html mapeados para os thumbs 

-------------------------------------------------------------------------------------------------------------
'''

import ffmpy
import glob
import sys
import os
import subprocess
import datetime
import shutil
from bs4 import BeautifulSoup
from shutil import copy2
from _operator import contains

class compLaudo:
    THUMBS_X = 5
    THUMBS_Y = 5
    VIDEO_TYPES = ["MP4", "3GP", "MOV"]
    HTML_TYPES = ["HTML", "HTM"]

    DIR_LAUDO = ""
    __ALLFILES = []
    PROCESSED_FILES = []
    PASTAS_VIDEO = []
    HTML_PAGES = []
    __TEMPSUFIX = {"OLD":"_old", "NEW":"_new"}

    #PROCESSED_FILES_TMP = ["0011597f-62ee-4b34-8d68-51f42dcd9449.mp4", "0074fad0-84f2-4b3c-9d46-6a3997b69167.mp4"] 

    def __init__(self, dir):
        self.DIR_LAUDO = dir
        self.__ALLFILES = [file for file in glob.glob(self.DIR_LAUDO+"/**", recursive=True)]
        print(len(self.__ALLFILES))
  
    def getNumFrames(self, fileName):
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
    
    def getExt(self, arq):
        indext = arq.upper().rfind(".")
        ext = arq[indext+1:].upper()
        return ext
    
    def processa_HTML_videos(self, html_page):
        print(str(datetime.datetime.now()) + "Processando -->" + html_page)
        with open(html_page,"r", encoding='utf8') as f:
            soup = BeautifulSoup(f)  
        soup.prettify()
    
        for tag in soup.find_all("a"): 
            if any(os.path.split(os.path.abspath(tag['href']))[1] in s for s in self.PROCESSED_FILES):
                tag['href'] = str(tag['href']) + "_thumbs.jpg"
                    
        with open(html_page+self.__TEMPSUFIX["NEW"]+".html","w", encoding='utf8') as f:
            f.write(str(soup))  
    
    def geraThumbsPasta(self, dirOrigem, dirDestino):
#        files = [file for file in glob.glob(dirOrigem+"/**", recursive=True)]
        files = [file for file in glob.glob(dirOrigem+"/*")]
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
                ext = self.getExt(fileName)
                if os.path.isfile(fileName) and  ext in self.VIDEO_TYPES:
                    nFrames = self.getNumFrames(fileName)
                    if nFrames > (self.THUMBS_X * self.THUMBS_Y):
                        outputpars = '-loglevel panic -y -vf "select=not(mod(n\,'+str(nFrames // 25) 
                        outputpars+= ')),scale=320:240,tile='+str(self.THUMBS_X)+'+'+str(self.THUMBS_Y)+'" -frames 1'
                        ff = ffmpy.FFmpeg(inputs={fileName:None}, 
                                  outputs={newNameTmp: outputpars})
                        ff.run()
                        processed = True  
                        self.PROCESSED_FILES.append(os.path.split(os.path.abspath(fileName))[1])
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

    def process(self):
        # bkpLaudo - faz a cópia de backup do laudo.
        for arquivo in self.__ALLFILES:
            ext = self.getExt(arquivo)
            if os.path.isfile(arquivo):
            
                if ext in self.VIDEO_TYPES:
                    path = os.path.dirname(os.path.abspath(arquivo))                     
                    if path  not in self.PASTAS_VIDEO: 
                        self.PASTAS_VIDEO.append(path)                                        

                elif ext in self.HTML_TYPES:
                    self.HTML_PAGES.append(arquivo)

        for pasta in self.PASTAS_VIDEO:
            self.geraThumbsPasta(pasta, pasta+self.__TEMPSUFIX["NEW"])
            os.rename(pasta, pasta+self.__TEMPSUFIX["OLD"])
            os.rename(pasta+self.__TEMPSUFIX["NEW"], pasta)
            shutil.rmtree(pasta+self.__TEMPSUFIX["OLD"], ignore_errors=False, onerror=None)

        for pag in self.HTML_PAGES:
            self.processa_HTML_videos(pag)
            os.rename(pag, pag+self.__TEMPSUFIX["OLD"])
            os.rename(pag+self.__TEMPSUFIX["NEW"]+".html", pag)
            os.remove(pag+self.__TEMPSUFIX["OLD"])
                    
if len(sys.argv) < 2:
    print ("uso: python "+sys.argv[0]+" dir_entrada dir_saida")
    sys.exit(1)

cl = compLaudo(sys.argv[1])
cl.process()

#geraThumbs(sys.argv[1], sys.argv[2])
#processa_HTML_videos(sys.argv[3])

'''
def geraThumb(self, filename, newname): #- i/nt
        try: 
            ext = getExt(fileName)
            if os.path.isfile(fileName) and  ext in VIDEO_TYPES:
                nFrames = getNumFrames(fileName)
                if nFrames > (THUMBS_X * THUMBS_Y):
                    outputpars = '-loglevel panic -y -vf "select=not(mod(n\,'+str(nFrames // 25) 
                    outputpars+= ')),scale=320:240,tile='+str(THUMBS_X)+'+'+str(THUMBS_Y)+'" -frames 1'
                    ff = ffmpy.FFmpeg(inputs={fileName:None}, 
                              outputs={newname: outputpars})
                    ff.run()
                    processed = True
        except:
            print ("Erro no processamento de: "+str(sys.exc_info()))

'''

    
#ffmpeg -y -i input -c:v libx264 -preset medium -b:v 555k -pass 1 -an -f mp4 /dev/null && \
#ffmpeg -i input -c:v libx264 -preset medium -b:v 555k -pass 2 -c:a libfdk_aac -b:a 128k output.mp4        
# -s 640x480 -b:v 512k -vcodec mpeg1video -acodec copy
#        ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -fs "+str(newSize)})
#        ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -crf 45 "})
