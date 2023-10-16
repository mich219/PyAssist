import random
import subprocess
import os
import sys
import glob
import pandas as pd
from datetime import datetime


path = "/media/michael/NEW VOLUME/notes/Goals/LearningLog"
CSV_file = "/media/michael/NEW VOLUME/notes/learns.csv"
Mod_file = "/media/michael/NEW VOLUME/notes/ModifTemp.md"


df = pd.read_csv(CSV_file)
df = df.sample(frac=1).reset_index(drop=True)

	
for root, dirs, files in os.walk(path):
	for text_file in files:
		if text_file.endswith(".md"):
			file_path = os.path.join(root, text_file)

			with open(file_path, 'r+') as file:
				lines = file.readlines()  # Read all lines into a list
				for i, line in enumerate(lines):

					if line[0] == "+":
						new_row = pd.DataFrame([{
							'Date': datetime.now().date(),
							'Recall': line[1:].strip(),
							'Awnser':"",
							'Known': False,
							'Familiarity':0			
							}])
						df = pd.concat([df, new_row], ignore_index=True)
						df.to_csv(CSV_file,index=False)
						newline = "-" + line[1:]
						lines[i] = newline

					if line[0] == "*":
						df.iloc[-1, df.columns.get_loc('Awnser')] += line[1:].strip() + '\n'
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
		random_value = random.randint(0, row["Familiarity"])
		if row['Known'] == False and  row["Familiarity"] == random_value:

			os.system('clear')
			for column in ['Date','Recall']:
				print(f"{column}: {row[column]}")
			new_value = input(":")
			for column in ['Awnser']:
				print(f"{column}: {row[column]}")
			
			modify = input("Known(y!) Familiar(y) Modify(m) New(n) Swap(s) or Press Enter to continue...") 
			if new_value == 'y!':
				df.at[index, "Known"] = True
			if new_value == 'y':
				df.at[index, "Familiarity"] += 1
			if modify == "s":
				df.at[index, "Awnser"], df.at[index, "Recall"] = df.at[index, "Recall"], df.at[index, "Awnser"]
			if modify == "m":
				df.at[index, "Known"] = True
				with open(Mod_file, "w") as temp_file:
					temp_file.write("+"+str(row['Recall'])+"\n")
					temp_file.write("* "+str(row['Awnser']))
				subprocess.run(["vim", Mod_file]) #PUT IT ALL IN THE SAME DIRECTORY
			if modify == "n":
				Question = input ("Question:")
				awnser = input ("Awnser:")
				new_row = pd.DataFrame([{
					'Date': datetime.now().date(),
					'Recall': Question,
					'Awnser':awnser,
					'Known': False,
					'Familiarity':0			
					}])
				df = pd.concat([df, new_row], ignore_index=True)
			if sys.argv[1] in ["-a", "-r", "-ra", "-all", "-ra"]:
				df.to_csv(CSV_file, index=False)

