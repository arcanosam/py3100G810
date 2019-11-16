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
  * Export to CSV file

### Requirements
* Python **3.7.5** with 
  * **tkinter**
  * [pyserial](https://github.com/pyserial/pyserial)

### Branch Trial CSV
* To use for trial/demonstration
* Persitance in SQLite database
* Export data to CSV file

##### Update 2019-11-15
* Remove login window
* Update LICENSE
* PEP 8 fix


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)