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
* Python **3.7.5** with 
  * **tkinter**
  * [pyserial](https://github.com/pyserial/pyserial)

### Branch Trial CSV
* To use for trial/demonstration
* Persistance in SQLite database
* Export data to CSV file

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