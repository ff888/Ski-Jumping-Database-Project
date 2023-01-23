

![SKI JUMPING DATABASE PROJECT](photos/Ski%20Jumping%20DB%20Logo.png)


---
# ***SKI JUMPING DATABASE PROJECT***

---

### ***_From the author_***

>_Hello!_
>
>_This is my first python project, the first step into programming. My "Hello World!" as a developer. Therefore, any help, ideas, constructive feedback or cooperation is very much appreciated._
>
>_All the best,_
> 
>_Jakub Krajewski_


---

## ***_Purpose of the app_***

A hundred years of the ski jumping history on ONE CLICK!

Please note a hundred years of ski jumping is a long period of time, which means thousands of different types of tournaments (World Cup, Olympic, Team, Individual, Man, Woman, Mixed). 

Over the years, this discipline has changed a lot. Not only the sport changed has itself, but also the way how is shown. Another important aspect is the technology that is used, and the way how the data is stored is much different from 20-30 years ago. This app covers all these changes.

The goal of the app is to create a database with information about all senior ski jumping tournaments that happened over a hundred years of ski jumping history.
To achieve this goal, the program has to scrape [fis.com](https://www.fis-ski.com/en) website (to see how data is pulling from the web go to "How it's works" section). 

The program is pulling the data for each tournament (pdf file or website) and creates csv files (see the "About CSV file Structure" section).
Creates unique file name (see the "About file name structure" section) and saves it in proper location in a database according to gender, tournament type, season. To access and manage data in the easiest way.

Is worth mentioning that the fis.com database is not complete, especially records before 2002, where details are missing. 
If you have access to historical ski jumping data records please share them with me I will include them in this app.
___

## ***_How it's works_***

The app is goes through website:
>https://www.fis-ski.com/DB/general/results.html?sectorcode=JP&raceid={COD}#down
> 
where the COD is a number between 1 and 9999 where each is randomly ordered to single competition.
The program is using requests library and loop to go through and check if web is valid. 


To scrape data from valid website program is using few different techniques. 

1. WEB
   
   - Until 2002 all information are hold on websites.
   To pull data app uses BeautifulSoup4 library.
   (data is not as detailed as 2002 and after all empty spaces are replaced by NULL value).
     
   

2. PDF 
   
   - From 2002 fis starts save competition data in the pdf files (data here is more detailed).
   First pdf is downloaded then app pulls data using pdfplumber library.
   There are many variants of pdfs here and each variant has to be treated individually.
     
   
     

---

## ***_About DataBase structure_***

Database is built by pulling information from the file name (is accessing 5 different "file name" elements and on this basis it places
the files in the appropriate sections of DB):

1. First step is to access gender element in the file name and creates a proper dir 
   (Man, Women or Mixed).
   
   
2. Second directory is tournament type (Grand Prix, Olympics, World Cup or World Championship) 
   and creates a directory with the same name.
   
   
3. A third dir is Individual or Team competition.


4. Four directory is season date, season function is checking the date of file name and according to it its creates a season
   name, and the directory with the same name.


5. Finally, it saves the file in season dir.

See picture below:

![DB Structure Sample](photos/DB%20Structure%20Sample.png)

---

## ***_About CSV file structure_***

Each file has the same structure - csv tabular type of file.

There are 33 columns with all tournament data like ranking, name, speed, distance, points etc.

Each row holds information about each jumper performers on giving tournament.

Depending on when the competition took place and how detailed the date of the competition is,
there is a possibility of empty spaces in the tables, which are replaced with NULL values.

---
## ***_About file name structure_***

Name is created using information from fis.web and scraped using BeautifulSoup library. 
Each file name is created in the very same structure where each element holds useful information,
this way is easy to find the file and manage it.

File name structure:

> YYYY-mm-dd_city(country)_(codex)_tournament type_hill size_gender_individual or team.csv

See example below:

> ### 1985-01-04_Innsbruck(AUT)_(471)_WC_LH_M_I


Where:

Element 1: 1985-01-04 -  date formatted YYYY-mm-dd 

Element 2: Innsbruck(AUT) - city(NATIONALITY)

Element 4: (471) - codex (fis website cod specification)

Element 3: WC - tournament type 
- OL = Olympics
- WC = World Cup
- GP = Grand Prix
- CH = World Championship 
        
Element 4: LH - hill size
- NH = Normal Hill
- LH = Large Hill
- SF = Flying Hill

Element 5: M - gender
- M = Man 
- W = Woman
- X = Mixed

Element 6: I - Individual or Team competition
- I = Individual
- T = Team

Thanks to that is easy to find and access a file or group of files using different attributes 
(like all competition in giving city, or only Olympic tournaments).

---

## ***_Built With_***

- [Requests](https://docs.python-requests.org/en/latest/ "Requests: HTTP for Humans")
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/ "Beautiful Soup is a Python library for pulling data out of HTML and XML files.")
- [Pdfplumber](http://www.lib4dev.in/info/jsvine/pdfplumber/41279279 "Plumb a PDF for detailed information about each text character, rectangle, and line. Plus: Table extraction and visual debugging.")
- [Textwrap](https://docs.python.org/3/library/textwrap.html "Text wrapping and filling")
- [CSV](https://docs.python.org/3/library/csv.html "CSV File Reading and Writing")
- [Datetime](https://docs.python.org/3/library/datetime.html "The datetime module supplies classes for manipulating dates and times.")
- [OS](https://docs.python.org/3/library/os.html "This module provides a portable way of using operating system dependent functionality.")
- [Shutil](https://docs.python.org/3/library/shutil.html "The shutil module offers a number of high-level operations on files and collections of files.")
- [Pandas](https://pandas.pydata.org "Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
built on top of the Python programming language.")

---


### _Please note the app is not fully finished yet._

Ready for:

    [yes] File name creator.

    [yes] Database builder.

    [yes] Web scraper for individual competition before 2002.

    [yes] Web scraper for team competition before 2002.

    [yes] Pdf scraper for individual competition starts from 2002.
      - [yes] tabular pdf scraper for individuals
      - [yes] text pdf scraper for individuals

    [yes] Pdf scraper for team competition starts from 2002.
    [no] handle disqualification rows

---

## ***_Contributor_***

_Jakub Krajewski_ ( jakub.j.krajewski@gmail.com )

---

## ***_Licence: MIT_***

---
