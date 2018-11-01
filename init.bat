@ECHO OFF
FOR /f %%p in ('where python') do SET PYTHONPATH=%%p
setlocal enabledelayedexpansion
set S=%PYTHONPATH%
set I=0
set L=-1
:l
if "!S:~%I%,1!"=="" goto ld
if "!S:~%I%,1!"=="\" set L=%I%
set /a I+=1
goto l
:ld
CALL set p=%%PYTHONPATH:~0,%L%%%
set PIP=%p%\Scripts\pip
mkdir keyword
mkdir Outputs
mkdir resumes
python -m pip install --upgrade pip
%PIP% install PyPDF2
%PIP% install xlsxwriter
%PIP% install docx2txt
%PIP% install spacy
python -m spacy download en_core_web_sm