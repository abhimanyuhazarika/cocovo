Cocovo (Django)
================


check python version by running the following command
```
$ python --version
Python 2.7.11
```
If python is installed, run the below commands:
```
pip install virtualenv
cd cocovo [ go to the directory in which you have the cocovo files]
virtualenv .
source ./bin/activate # or .\Scripts\activate on Windows
pip install -r requirements.txt
./manage.py syncdb
./manage.py runserver
```

Open another terminal window in this directory and run:
```
./testapp
```

It'll run another web server on port 8008. You can view the test app at http://127.0.0.1:8008/

Open another terminal and execute the below triggers in database:

To access sqlite db in the third terminal:

./manage.py dbshell


trigger for correct answers update
CREATE TRIGGER IF NOT EXISTS UPDATE_CORRECT_ANSWERS AFTER INSERT ON minicom_uservocab FOR EACH ROW BEGIN UPDATE minicom_user SET correct_answers= correct_answers + NEW.is_correct WHERE minicom_user.id =NEW.user_id; END;

trigger for user level update
CREATE TRIGGER IF NOT EXISTS UPDATE_USER_LEVEL AFTER UPDATE OF correct_answers ON minicom_user FOR EACH ROW WHEN NEW.CORRECT_ANSWERS/NEW.LEVEL=10 BEGIN UPDATE minicom_user SET level=OLD.level + 1 WHERE id =NEW.id; END;

CREATE TRIGGER UPDATE_USER_LEVEL AFTER UPDATE OF correct_answers ON minicom_user FOR EACH ROW WHEN (NEW.CORRECT_ANSWERS/NEW.LEVEL=3 AND NEW.AVG_TIME<5) OR (NEW.CORRECT_ANSWERS/NEW.LEVEL=2 AND NEW.AVG_TIME<3) BEGIN UPDATE minicom_user SET level=OLD.level + 1 WHERE id =NEW.id; END;
COMMIT;



Additional notes for cocovo:
[TODO TASKS]:

INSERT INTO minicom_vocab VALUES(1,'opinion','a view or judgement formed about something, not necessarily based on fact or knowledge',1,1);
INSERT INTO minicom_vocab VALUES(2,'serpentine','move or lie in a winding path or line',4,1);
INSERT INTO minicom_vocab VALUES(3,'intricate','very complicated or detailed',3,1);
INSERT INTO minicom_vocab VALUES(4,'coward','a person who is contemptibly lacking in the courage to do or endure dangerous or unpleasant things',2,1);
INSERT INTO minicom_vocab VALUES(5,'bungalow','a low house having only one storey or, in some cases, upper rooms set in the roof, typically with dormer windows',1,1);

CHANGE BACKGROUND DEPENDING ON AGE, GENDER
CHANGE TIME TAKEN WEIGHT FOR DIFFERENT AGE
IF TWO SYNONYMS ARE ANSWERED THEN NO MORE SYNONYMS

levels different for different age group 

name, age ,gender, email, interest area sign up form
interest area + if answers wrong, then probability increases
