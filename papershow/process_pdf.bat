@echo off 
set folder_path=%1%
set /a folder_num=%2%

:loop
set /a n+=1
if %n% leq %folder_num% (
	if exist %folder_path%%n% ( 
		start "" cmd /c call java -cp cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path %folder_path%%n% -outputs jats 
	)
goto :loop)
java -cp cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path %folder_path%0 -outputs jats 


