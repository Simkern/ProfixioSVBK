# ProfixioSVBK
Suite to scrape match data from Profixio's page for Volleyball tounaments

## Downloading match data

Clone the repository and install all necessary dependencies. Then, if you are happy with the configuration in the config.py file, run the main script main_profixiodata.py to download the match data.

## Converting .csv to .xls

1. Open .csv file in Excel
2. Press Alt+F11 to open the Visual Basic editor
3. Press Crtl+M to import a file and choose the file "cleanup.bas" and close the Visual Basic editor to return to Excel.
4. Press Alt+F8 to view the loaded macros in the Excel session.
5. Run the macro "Cleanup" that performs all the conversion steps.
6. If there are problems during the macro execution, close Excel, reopen the .csv and repeat the loading process. Then run the four macros manually in order (TextToCol, ColorDivs, ColorDate, SortDate) to identify the problem.
    
