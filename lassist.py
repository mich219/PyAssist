import os
import sys
import glob
import pandas as pd
from datetime import datetime


#path = "/media/michael/NEW VOLUME/notes/Goals/LearningLog"
path = "/home/michael/Desktop/PyAssist"
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
							'Date': datetime.now().date(),
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


if len(sys.argv) > 2:
    print("-r or -a or -ra")
    sys.exit(1)

if sys.argv[1] == "-r":
	filtered_df = df.loc[df['Known'] == False,['Date','Recall']]
	print(filtered_df)

if sys.argv[1] == "-a":
	filtered_df = df.loc[df['Known'] == False,['Date','Recall','Awnser',"Known"]]
	print(filtered_df)

if sys.argv[1] == "-all":
	print(df)

if sys.argv[1] == "-ra":
	for index, row in df.iterrows():
		if row['Known'] == False:
			os.system('clear')
			print(f"Row {index + 1}:")
			for column in ['Date','Recall']:
				print(f"{column}: {row[column]}")
			new_value = input("Known(y/n):")
			for column in ['Awnser']:
				print(f"{column}: {row[column]}")
			if new_value == 'y':
				df.at[index, "Known"] = True
			input("Press Enter to continue...")
	df.to_csv(CSV_file, index=False)

