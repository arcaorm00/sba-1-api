Data Dictionary
(Variable = feature = parameter = axis)

Variable        	Definition	            Key
0. survival	        Survival	            0 = No, 1 = Yes
1. pclass	        Ticket class	        1 = 1st, 2 = 2nd, 3 = 3rd
2. sex	            Sex	
3. Age	            Age in years	
4. sibsp	        # of siblings / spouses aboard the Titanic	
5. parch	        # of parents / children aboard the Titanic	
6. ticket	        Ticket number	
7. fare	            Passenger fare	
8. cabin	        Cabin number	
9. embarked	        Port of Embarkation	    C = Cherbourg, Q = Queenstown, S = Southampton


Variable Notes
pclass: A proxy for socio-economic status (SES)
1st = Upper
2nd = Middle
3rd = Lower

age: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5

sibsp: The dataset defines family relations in this way...
Sibling = brother, sister, stepbrother, stepsister
Spouse = husband, wife (mistresses and fiancés were ignored)

parch: The dataset defines family relations in this way...
Parent = mother, father
Child = daughter, son, stepdaughter, stepson
Some children travelled only with a nanny, therefore parch=0 for them.