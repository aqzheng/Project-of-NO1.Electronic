@echo off

java -cp src/reference/run.jar pl.edu.icm.cermine.ContentExtractor -path %1% -outputs jats

python src/reference/main.py %1%
python src/material/run.py %1%