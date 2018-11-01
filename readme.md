# Follow The Steps
1. run init.bat
    - if fail
		- make sure pip path is in environment path
		- make sure pip path is in environment path
		- pip.exe should be in \<Path to Python27\>/Scripts
		- run pip install spacy in command line
2. add keyword file into keyword folder
	- recommended format
		- \<HIRING TITLE\>.txt
	- keywords should be seperated by ',' example
		- keyword1,keyword2,keyword3,keyword4
3. add resumes into resumes folder
	- pdf and word are supported
		- word should be 1 resume per file
4. open Command Line and cd into the directory
5. run python ResumeScanner.py \<HIRING TITLE\>
6. result will be in Outputs folder \<HIRING TITLE\>.xlsx
