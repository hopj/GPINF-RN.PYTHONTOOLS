import ffmpy
import glob
import sys
import os
import datetime
import shutil



if len(sys.argv) < 2:
    print ("uso: python "+sys.argv[0]+" dir_entrada dir_saida")
    sys.exit(1)
    
# COMANDO -->  ffmpeg -i ORIGEM.jpg -vf scale=640:-1 DESTINO.png
ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -fs "+str(newSize)})
    
ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newname: outputpars})
ff.run()


dirOrigem = "F:\TMP\testes_ffmpeg\origem)"
dirDestino = "F:\TMP\testes_ffmpeg\destino)"
files = [file for file in glob.glob(dirOrigem+"/*")]
posDP = dirOrigem.find(":")
if posDP < 0:
    posDP = 0
print ("Convertendo "+str(len(files))+" arquivos - Iniciado em:"+str(datetime.datetime.now()))
nfile = 1
for fileName in files:
    newName = fileName.replace(dirOrigem, dirDestino)
    os.makedirs(os.path.dirname(newName), exist_ok=True)
    newNameTmp = newName+"_small.jpg"
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



    
#ffmpeg -y -i input -c:v libx264 -preset medium -b:v 555k -pass 1 -an -f mp4 /dev/null && \
#ffmpeg -i input -c:v libx264 -preset medium -b:v 555k -pass 2 -c:a libfdk_aac -b:a 128k output.mp4        
# -s 640x480 -b:v 512k -vcodec mpeg1video -acodec copy
#ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -fs "+str(newSize)})
#        ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -crf 45 "})
