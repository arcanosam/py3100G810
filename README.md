# py3100G810
Grains weight and humidity collector from **3100 family weighing indicators** and **Gehaka grain meter G810 respectively** - a Python **Tkinter** Application

### Goals
* A python GUI application

  * That accepts an **ID code**
    * Used to identify the values collected below
  
  * To read values from **serial** port:
    * [3100 family weighing indicators](http://www.alfainstrumentos.com.br/produto/linha-3100-cs-painel/)
    * and [Gehaka Grain Meter G810](https://www.gehaka.com.br/produtos/linha-agricola/medidor-de-umidade-de-graos-de-bancada/g810-std)

  * To **persist** this two collected values in a PostgreSQL database.

### Requirements
* Python **3.7.1** with 
  * **tkinter**
  * [pyserial](https://github.com/pyserial/pyserial)


##### Update 2018-11-26

* Using simple method to identify when the value read is stable
  * Will be used when persist the values in database.

##### Update 2018-11-26

* Fix it bug when the 3100 weighing indicator is turned off, freezing the application.
  * Solution used: Threads

* Some code refactor
  * Using python properties, make variables private...

##### Update 2018-11-16

* Starts collect data from 3100 family weighing indicators' serial

 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)