import ffmpy
import glob
import sys
import os
import subprocess
import datetime

THUMBS_X = 5
THUMBS_Y = 5

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

if len(sys.argv) < 3:
	print ("uso: python "+sys.argv[0]+" dir_entrada dir_saida")
	sys.exit(1)
	
	
files = [file for file in glob.glob(sys.argv[1]+"/**", recursive=True)]
posDP = sys.argv[1].find(":")
if posDP < 0:
	posDP = 0

print ("Convertendo "+str(len(files))+" arquivos - Iniciado em:"+str(datetime.datetime.now()))
nfile = 1
for fileName in files:
    newName = fileName.replace(sys.argv[1], sys.argv[2])
    os.makedirs(os.path.dirname(newName), exist_ok=True)
    newNameTmp = newName+"_thumbs.jpg"
    processed = False	
    print ("Convertendo de: "+fileName+" para "+newNameTmp)
    try: 
        indext = fileName.upper().rfind(".")
        ext = fileName[indext+1:].upper()

        if os.path.isfile(fileName) and  ext in ["MP4", "3GP", "MOV"]:
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
    if 	processed:
        size = os.stat(fileName).st_size
        newsize = os.stat(newNameTmp).st_size
        print (fileName+": "+str(size)+
               " -> "+str(newsize)+ " "+newNameTmp, end='')
	else:
		os.replace(newNameTmp, newName)   # CONFIRMAR SE REALMENTE COPIA.
    print()
print ("Arquivos convertidos. Finalizado em:"+str(datetime.datetime.now()))
	
#ffmpeg -y -i input -c:v libx264 -preset medium -b:v 555k -pass 1 -an -f mp4 /dev/null && \
#ffmpeg -i input -c:v libx264 -preset medium -b:v 555k -pass 2 -c:a libfdk_aac -b:a 128k output.mp4		
# -s 640x480 -b:v 512k -vcodec mpeg1video -acodec copy
#		ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -fs "+str(newSize)})
#		ff = ffmpy.FFmpeg(inputs={fileName:None}, outputs={newName: "-loglevel panic -f mp4 -crf 45 "})
