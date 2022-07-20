Set args = WScript.Arguments
directory = args.Item(0)

projDir = left(directory, len(directory)-7)
FullFileName = projDir & "\Tests\UDFs\project_config\project_setup_paths.py"
SearchFor = "v_current_project_path"
newline = vbTab & SearchFor &" = r""" & projDir & """"

Set fso= CreateObject("Scripting.FileSystemObject")
NewFilename = fso.GetParentFolderName(FullFileName) & "\" & "New" & "_" & fso.GetFileName(FullFileName) 

set readfile = fso.OpenTextFile(FullFileName, 1, false)
set writefile = fso.CreateTextFile(NewFileName, 2)

Do until readfile.AtEndOfStream = true
	ThisLine = readfile.ReadLine
	If Left(trim(ThisLine),22) = SearchFor Then	
		pos = instr(20,ThisLine, "r""",1)
		newline = left(ThisLine, pos-1) & "r""" & projDir & """"
		writefile.write newline  & vbCRLF
	Else
		writefile.write ThisLine & vbCRLF
	End If
loop

readfile.close
writefile.close
fso.CopyFile NewFilename, FullFileName, True
fso.DeleteFile NewFilename, True
