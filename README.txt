PyAssit will do the following tasks: 

It will read all the (text) filesfrom the notes 
It will check each line's first character for: "+" and "*"
If "+" it will create row in the csv file with a DataFrame and it will add line to Recall column
If "*" it will add the the latest created row in the column Awnser

Depending on the arguments parsed when the program is called(using the csv file):

-r > Print all rows (without the awnser) with the Known column == False.
-a > Print all rows (with the awnser) with the Known column = False.
-ra >   Print one row at a time without the awnser and Known = False.
		then input (y or n) if y then: Known = True
		Print the awnser

