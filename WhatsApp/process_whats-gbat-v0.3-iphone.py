# -*- coding: latin-1 -*-

import sys
import os
import sqlite3

def new_file(outputDirName, fileName, columnNames):
	print ("\nGerando arquivo para "+fileName)
	fdout = open (outputDirName+"/"+fileName+".html", 'w',  encoding=fileEncoding)
	fdout.write ("<HTML>\n")
	fdout.write ('<TABLE BORDER="1"> <BOLD> <FONT SIZE=14> <TR BGCOLOR="Green">\n')
	for i in range(7):
		fdout.write ("<TD>"+columnNames[i]+"</TD>")
	fdout.write ("</FONT> </BOLD> </TR>\n")
	return fdout

def write_line(fd, columns, owner):
	if columns[3] == owner:
#		fd.write('<TR BGCOLOR="PaleGreen">')
		fd.write('<TR BGCOLOR="Beige">')
	else:
		fd.write('<TR>')
		
	for i in range(5):
		fd.write("<TD>"+str(columns[i])+"</TD>")
		
	if columns[5] == 0:
		fd.write("<TD>Texto</TD><TD>"+columns[6]+"</TD>")
	elif columns[5] == 1:
		fd.write("<TD>Arquivo</TD> \
				  <TD><A HREF='"+str(columns[7])+"'>"+str(columns[7])+"</A></TD>")
	elif columns[5] == 3:
		fd.write("<TD>Áudio</TD> \
				  <TD><A HREF='"+str(columns[7])+"'>"+str(columns[7])+"</A></TD>")
	elif columns[5] == 6:
		fd.write("<TD>Criação/<br>Entrada<br>em Grupo </TD><TD></TD>")
	else:
		fd.write("<TD>Não identificado<BR>"
					"tipo: "+str(columns[5])+"<br>"+
					"</TD><TD>")
		if columns[6] is not None:
			fd.write(str(columns[6])+"<br>");
		if columns[7] is not None:
			fd.write("<A HREF='"+str(columns[7])+"'>"+str(columns[7])+"</A>")
		fd.write("</TD>")
		
	fd.write ("</TR>\n")

def write_members(fd, members):
	if fd != '':
		fd.write ("</TABLE>\n")
		fd.write ("Membros nesse chat")
		fd.write ("<TABLE BORDER='1'> <BOLD> <FONT SIZE=14>")
		for member in members:
			fd.write ("<TR><TD>"+str(member)+"</TD></TR>")
		fd.write ("</TABLE>")
	
def close_file(fd):
	if fd != '':
		fd.write ("</HTML>")
		fd.close()
		
def createMasterChat(chats):
	fdout = open (outputDirName+"/chats.html", 'w',  encoding=fileEncoding)
	fdout.write ("<HTML>\n")
	fdout.write ("<TABLE BORDER='1'> <BOLD> <FONT SIZE=14> <TR>\n")
	fdout.write ("<TR><TD>Id do Chat</TD><TD>Nome do contato/grupo</TD></TR> <TR>\n")
	for key in chats.keys():
		fdout.write ("<TR><TD>"+str(key)+"</TD>")
		fdout.write ("<TD><A HREF='"+str(key)+".html'>"+chats[key]+"</TD></TR>")
	fdout.write ("</FONT> </BOLD> </TR>\n")
	fdout.close()
	
def process_file(owner, dirOutputName):
	dbconn = sqlite3.connect(sourceFileName)
	cursor = dbconn.cursor()
	cursor.execute ("SELECT m.zchatsession AS IDCHAT, zsort AS IDMSG, \
						   datetime(zmessagedate + 978307200, 'unixepoch') as  DATA_HORA, \
						   CASE \
								WHEN zisfromme = 0 AND m.zgroupmember IS NOT NULL THEN gm.zcontactname \
								     || ' (' || zmemberjid || ')' \
								WHEN zisfromme = 0 AND m.zgroupmember IS NULL THEN cs.zpartnername \
								     || ' (' || zcontactjid || ')' \
								ELSE '"+owner+"' \
						   END AS ORIGEM, \
						   CASE \
								WHEN zisfromme = 1 OR m.zgroupmember IS NOT NULL \
									THEN cs.zpartnername\
								ELSE '"+owner+"'\
						   END AS DESTINO,  \
						   zmessagetype  AS TIPO, \
						   ztext AS MENSAGEM, \
						   zmedialocalpath AS ARQUIVO \
					FROM zwamessage m, zwachatsession cs \
					LEFT JOIN  zwagroupmember gm ON gm.z_pk = m.zgroupmember \
					LEFT JOIN zwagroupinfo gi ON gi.zchatsession = gm.zchatsession \
					LEFT JOIN zwamediaitem mi ON mi.zmessage = m.z_pk \
					WHERE cs.z_pk = m.zchatsession \
					ORDER BY m.zchatsession, zsort")

	columnNames = [desc[0] for desc in cursor.description]
	actualColumn = ''
	fdout = ''
	chats = {}
	
	members=set()
	for columns in cursor.fetchall():
		if columns[5] == 0 and columns[5] != owner:
			chats[columns[0]] = columns[5]
		if columns[columnToSplit] != actualColumn:
			if byChat:
				write_members(fdout, members)
				close_file(fdout)
				members.clear()
				fdout = new_file(dirOutputName, str(columns[columnToSplit]), columnNames)
			elif fdout == '':			
				fdout = new_file(dirOutputName, "chats-all", columnNames)
			actualColumn = columns[columnToSplit]	
		if byChat:
			members.add(columns[3])
		write_line(fdout, columns, owner)		

	if byChat:
		createMasterChat(chats)
		
	close_file(fdout)
	

if len(sys.argv) < 2:
	print ('usage: python3 process_whats sourceDB [--byChat] [utf-8]')
	os._exit (1)
	
sourceFileName = sys.argv[1]
columnToSplit = 0

if len(sys.argv) > 3:
	fileEncoding = sys.argv[3]
else:
	fileEncoding = "utf-8"
	
if len(sys.argv) > 2 and sys.argv[2] == "--byChat":
	byChat = True
else:
	byChat = False

outputDirName = "results"
#os.mkdir(outputDirName)
	
process_file('Laurita', outputDirName)