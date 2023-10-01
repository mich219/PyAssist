import os
import glob
import pandas as pd
from datetime import datetime


#path = "/media/michael/NEW VOLUME/notes/Goals/LearningLog"
path = "/home/michael/Desktop/PyAssist"
target_file_name = "test.txt"
CSV_file = "learns.csv"


df = pd.read_csv(CSV_file)
	
for root, dirs, files in os.walk(path):
	for text_file in files:
		if text_file.endswith(".txt"):
			file_path = os.path.join(root, text_file)

			with open(file_path, 'r+') as file:
				lines = file.readlines()  # Read all lines into a list
				for i, line in enumerate(lines):

					if line[0] == "+":
						new_row = pd.DataFrame([{
							'Date': datetime.now(),
							'Recall': line[1:].strip(),
							'Awnser':"",
							'Known': False
							}])
						df = pd.concat([df, new_row], ignore_index=True)
						df.to_csv(CSV_file,index=False)
						newline = "-" + line[1:]
						lines[i] = newline

					if line[0] == "*":
						df.iloc[-1, df.columns.get_loc('Awnser')] = line[1:].strip()	
						df.to_csv(CSV_file,index=False)
						newline = "-" + line[1:]
						lines[i] = newline

				file.seek(0)
				file.writelines(lines)


filtered_df = df.loc[df['Known'] == False,['Recall','Awnser']]
print(filtered_df)













