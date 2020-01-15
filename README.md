# py3100G810
Grains weight and humidity collector from **3100 family weighing indicators** and **Gehaka grain meter G810 respectively** - a Python **Tkinter** Application

### Goals
* A python GUI application

  * That accepts an **ID code**
    * Used to identify the values collected below
  
  * To read values from **serial** port:
    * [3100 family weighing indicators](http://www.alfainstrumentos.com.br/produto/linha-3100-cs-painel/)
    * and [Gehaka Grain Meter G810](https://www.gehaka.com.br/produtos/linha-agricola/medidor-de-umidade-de-graos-de-bancada/g810-std)

  * To **persist** this three collected values in a ~~PostgreSQL~~ SQLite database.
  * *Export* to **CSV** file

### Requirements
* Python **3.7.6** with
  * **tkinter**
  * [pyserial](https://github.com/pyserial/pyserial)
  * **Optional**
    * [cx_freeze](https://anthony-tuininga.github.io/cx_Freeze/)

### Branch Trial CSV
* To use for trial/demonstration
* Persistance in SQLite database
* Export data to CSV file

##### Update 2020-01-15
* dao/__init__.py
  * added - required to cx_freeze work

* lang.ini
  * added - required to get the default app language

* setup.py
  * added - required to cx_freeze generate EXEs to Windows plataform

* gui/app_def.py
  * Refactoring to accepts other languages
    * The app language is defined on lang.ini
    * Brazilian portuguese is supported now as app language

* gui/app_win.py
  * try / catch block added _close_app
    * to prevent crash in Windows plataform when exit the app
    * Set focus to Id Code Entry(edit/input) after some system actions
    * remove random package and random function
      * Used to test the persistance

##### Update 2020-01-12
* dao/data_ids.py
  * include the return of sql result after insert a new ID
  * remove id field when export data to csv file
  * added method to cleanup database

* gui/app_def.py
  * more new text definitions 

* gui/app_win.py
  * New menu option added
    * allowed cleanup database
  * Load com ports of each device (3100 and g810) from ini file
    * new devices.ini added
  * Refactoring of strings used in dialogs by get_app_definitions method

##### Update 2020-01-06
* dao/data_ids.py
  * Improving database class
    * _run_sql method which execute queries and return if successful or not
      * refactoring other methods to use this one

* gui/app_def.py
  * New default text definitions 

* gui/app_win.py
  * Added Csv Exporter feature 
    * New menu option to use this feature
  * Added persistance of Weight and Humidity on sqlite database
    * After each persistance is asked if wish to clean fields
      * if not, the current id found is used to persistance the same attribute or the other
    * Refactoring on database operations because of the improvements list above
  * Cleaning fields on every change of id code value input

##### Update 2019-12-01 #2
* New text definitions added on app_def module
  * used on alert dialogs when no Id Code is Found and 
  when a new Id Code is added
* Remove various lines of dead code no more needed
  * Codes used to control auth and session data
* Insertion of new Id Codes implemented
* Search for Id Codes with autocomplete functionality implemented
  * When an Id Code is found, the weight and humidity of
    respectivity grain are returned
* Data access object directory added
  * Simple class to connect with Sqlite to persist the grain data

##### Update 2019-12-01 #1
* LICENSE add as hardcode on about_win module
* Preparing to integrate autocomplete with search/insert operations on sqlite
* sqlite db with new fields
  * record column - date of when register was add first
  * update column - when the record data was updated

##### Update 2019-11-15
* Removed:
   * login window
   * session
   * timer
* Update LICENSE
* PEP 8 fix
* add SQLite file
  * program starts and connect to sqlite
  * program fire close event and close sqlite file


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)