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
 
compLaudo v0.0.3b
        - Implementa o resize das imagens

compLaudo v0.0.3c1 (atual)
        - Criação do log
        - Correção de bug no processamento de videos pequenos (poucos k).
            . Foi adicionada condição de somente processar o video caso ele tenha um tamanho mínimo.

compLaudo v0.0.3d (futuro)
        - LOG: escrever qual a pasta de imagens esta sendo processada
        - PERFORMANCE: 
            . compLaudo.process --> testar o tamanho da imagem antes de inseri-la em self.IMG_FILES 
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
    IMG_TYPES = ["JPEG", "JPG","PNG", "TIFF"]

    DIR_LAUDO = ""
    __ALLFILES = []
    PROCESSED_FILES = []
    PASTAS_VIDEO = []
    HTML_PAGES = []
    IMG_FILES = [] 
    __TEMPSUFIX = {"OLD":"_old", "NEW":"_new"}
    __IMGSUFIX = ".jpg"
    __LOGFILE = ""

    #PROCESSED_FILES_TMP = ["0011597f-62ee-4b34-8d68-51f42dcd9449.mp4", "0074fad0-84f2-4b3c-9d46-6a3997b69167.mp4"] 

    def __init__(self, dir):
        self.DIR_LAUDO = dir
        self.__LOGFILE = self.DIR_LAUDO+"/compLaudoLOG.txt"
        with open(self.__LOGFILE, "w") as f:
            print()
        self.__writeLog("Iniciando processamento de ---> "+self.DIR_LAUDO )
        self.__ALLFILES = [file for file in glob.glob(self.DIR_LAUDO+"/**", recursive=True)]
        self.__writeLog("Númeto Total de Arquivos = "+ str(len(self.__ALLFILES)))
        
    def __writeLog(self, mensagem):
        with open(self.__LOGFILE, "a") as f:
            f.write(str(datetime.datetime.now()) + " -::- "+ mensagem +"\n")
            f.close()
        print(str(datetime.datetime.now()) + " -::- "+ mensagem +"\n")
        
    def getNumFrames(self, fileName):
        retval = 0
        #self.__writeLog("Recuperando nframes de: "+fileName)
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
        self.__writeLog("Processando HTML --> " + html_page)
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
        #self.__writeLog("Convertendo "+str(len(files))+" arquivos")
        nfile = 1
        for fileName in files:
            newName = fileName.replace(dirOrigem, dirDestino)
            os.makedirs(os.path.dirname(newName), exist_ok=True)
            newNameTmp = newName+"_thumbs.jpg"
            processed = False    
            try: 
                ext = self.getExt(fileName)
                if os.path.isfile(fileName) and  ext in self.VIDEO_TYPES and os.stat(fileName).st_size > 100000:
                    nFrames = self.getNumFrames(fileName)
                    if nFrames > (self.THUMBS_X * self.THUMBS_Y):
                        self.__writeLog("Convertendo de: "+fileName+" para "+newNameTmp)
                        outputpars = '-loglevel panic -y -vf "select=not(mod(n\,'+str(nFrames // 25) 
                        outputpars+= ')),scale=320:240,tile='+str(self.THUMBS_X)+'+'+str(self.THUMBS_Y)+'" -frames 1'
                        ff = ffmpy.FFmpeg(inputs={fileName:None}, 
                                  outputs={newNameTmp: outputpars})
                        ff.run()
                        processed = True  
                        self.PROCESSED_FILES.append(os.path.split(os.path.abspath(fileName))[1])
            except:
                self.__writeLog("Erro no processamento de: "+str(sys.exc_info()))
            
            #self.__writeLog(str(nfile)+"/"+str(len(files)))
            if processed:
                size = os.stat(fileName).st_size
                newsize = os.stat(newNameTmp).st_size
                #self.__writeLog(fileName+": "+str(size)+ " -> "+str(newsize)+ " "+newNameTmp) 
            elif os.path.isfile(fileName) :
                copy2(fileName,newName)
    #            os.replace(fileName,newName)   
            
        print()

    def resizeImg(self, imagem):
        if os.stat(imagem).st_size > 100000:
             outputPars = "-loglevel panic -y -vf scale=800:-1"
             newImg = os.path.splitext(imagem)[0]+self.__TEMPSUFIX["NEW"]+self.__IMGSUFIX 
             try: 
                 ff = ffmpy.FFmpeg(inputs={imagem:None}, outputs={newImg:outputPars})
                 ff.run()
                 os.rename(imagem, imagem+self.__TEMPSUFIX["OLD"])
                 os.rename(newImg, os.path.splitext(imagem)[0]+self.__IMGSUFIX)
                 os.remove(imagem+self.__TEMPSUFIX["OLD"])
             except:
                 self.__writeLog("Erro no processamento da imagem: "+imagem +"  -  "+str(sys.exc_info()))
                
    def process(self):
        
        self.__writeLog("Iniciando varredura dos arquivos e seleção de: PASTAS DE VIDEO, IMAGENS e HTMLs")
        for arquivo in self.__ALLFILES:
            ext = self.getExt(arquivo)
            if os.path.isfile(arquivo):
            
                if ext in self.VIDEO_TYPES:
                    path = os.path.dirname(os.path.abspath(arquivo))                     
                    if path  not in self.PASTAS_VIDEO: 
                        self.PASTAS_VIDEO.append(path)                                        

                elif ext in self.IMG_TYPES: # poderia fazer o resize diretamente aqui. Para facilitar os testes o resize será feito em laço específico mais abaixo.
                    self.IMG_FILES.append(arquivo)
                
                elif ext in self.HTML_TYPES:
                    self.HTML_PAGES.append(arquivo)

        try:
            self.__writeLog("############################# Inicio da geração dos thumbs dos videos ############################# ")
            for pasta in self.PASTAS_VIDEO:
                self.geraThumbsPasta(pasta, pasta+self.__TEMPSUFIX["NEW"])
                os.rename(pasta, pasta+self.__TEMPSUFIX["OLD"])
                os.rename(pasta+self.__TEMPSUFIX["NEW"], pasta)
                shutil.rmtree(pasta+self.__TEMPSUFIX["OLD"], ignore_errors=False, onerror=None)
    
            self.__writeLog("############################# Inicio do processamento dos arquivos HTML ############################# ")
            for pag in self.HTML_PAGES:
                self.processa_HTML_videos(pag)
                os.rename(pag, pag+self.__TEMPSUFIX["OLD"])
                os.rename(pag+self.__TEMPSUFIX["NEW"]+".html", pag)
                os.remove(pag+self.__TEMPSUFIX["OLD"])
            self.__writeLog("############################# Inicio do resize das imagens ############################# ")
            for img in self.IMG_FILES: 
                self.resizeImg(img)                

        except:     
            self.__writeLog("Erro no processamento:  "+ str(sys.exc_info()))

        self.__writeLog("Finalizado processamento de "+self.DIR_LAUDO )
                    
if len(sys.argv) < 2:
    print ("uso: python + diretório de entrada")
    sys.exit(1)


cl = compLaudo(sys.argv[1])
cl.process()
