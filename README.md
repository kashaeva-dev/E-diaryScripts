# E-diary Scripts
These are scripts for working with a database of a school. 
They allow you to fix grades, remove chastisements, and create commendations for schoolkids in the database.
The scripts are written in Python and use the Django framework to interact with the database. 
They use three models from the **datacenter app**: Schoolkid, Lesson, Subject and Commendation.

## How to install

To use these scripts, you need to have the e-diary Django project installed.
You can find the instructions for installing the e-diary project [here](https://github.com/devmanorg/e-diary/tree/master).
Once you have the e-diary project installed, copy the **scripts.py** file to the root directory of the project 
(where the **manage.py** file is located).
Note that you should find the **schoolbase.sqlite3** file somewhere and copy it
to the root directory of the Django project as well.

## How to use


The **scripts.py** file provides three functions that can be used to fix the marks, remove the chastisements, 
and create commendations for a specific schoolkid in the e-diary project.

1. **Fix_marks** function can be used to fix the marks of a schoolkid with a given name. 
The function searches for all marks with a score of 2 or 3 and changes them to 5.
2. **Remove_chastisements** function can be used to remove all chastisements of a schoolkid with a given name.
3. **Create_commendation** function can be used to create a commendation for a schoolkid with a given name and for a specific subject.
It takes the latest lesson of the given subject and creates a commendation for it.

To run these scripts, follow these steps:

1. Navigate to the root directory of your Django project in your terminal.

2. Enter the Django shell by typing:
```
python manage.py shell
```

3. Import the functions by typing:
```
from scripts import fix_marks, remove_chastisements, create_commendation
```
4. Call the functions with the appropriate arguments, like so:

- to fix marks: 
```
fix_marks('<Фамилия Имя ученика>')
```
- to remove chastisements:
```
remove_chastisements('<Фамилия Имя ученика>')
```
- to create a commendation:
```
create_commendation('<Фамилия Имя ученика>', '<Название предмета>')
```
