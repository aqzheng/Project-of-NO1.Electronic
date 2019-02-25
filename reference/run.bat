@echo off

set solved_file_num=%1%
set day=%date:~,4%%date:~5,2%%date:~8,2%
set targetDir=%~dp0papershow\static\pdf_data\%day%

echo start: moving files
python %~dp0reference\move_pdf.py %targetDir% %solved_file_num%
echo finish: moving files

echo start: converting pdf to xml
java -cp reference\cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path %targetDir% -outputs jats
echo finish: converting pdf to xml

echo start: extract citation
python reference\main.py %targetDir%
echo finish: extract citation

rem rd %targetDir% /s/q
