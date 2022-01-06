
## IP Management System

a simple IP management system developed using Python, Sqlachemy. Intended to be very minimal only 3 depdendency and you are good to go.


### Features

- Manages and shows information about subnets.
- Vlan management. Delete/add/modify a vlan.
- Displays stats related to vlan and subnets.
- Displays stats related to clients and shows ip information.


### System prerequisits

- python 3.8 is recommended
- python requirements included in requirements.txt
- sql alchemey 1.4.29 prerequisits

### Backend

Backend is mainly python. System was intended to be extendable byeond a single interface. System was designed with extendability in mind. you can extend models and other class and implement your interface fairly easily. 

### Database

Database included with the system is a simple sqllite3 database. With the power of sql alchemey you can connect to many other database types.

### CLI

This app has a user friendly command user interface

### Web
Not done yet :(
### System internals
- System is designed to be extendable.
- IBaseModel is the base class for all models. has some basic methods ready to be used/ overridden.

![Class Diagram](https://i.postimg.cc/FKkQNH6m/class-diagram.png "Class Diagram")

![Screenshot1](https://i.postimg.cc/QtLZtrL7/main-screen.png "interface")

![Screenshot2](https://i.postimg.cc/Bb4WTcnQ/Screenshot.png "interface")

### installation
- go to the root directory of the project and run `pip install -r requiremnts.txt`
- make sure you are on the root directory then run `python main.py`


