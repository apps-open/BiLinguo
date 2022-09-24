import json
import sqlite3

def main():
	conn = sqlite3.connect("vocab.db")
	cur = conn.cursor()
	with open("vocabulary.json") as jsonfile:
		dict_ = json.load(jsonfile)

	for k, v in dict_.items():
		print(k, v)
		cur.execute(f"INSERT INTO Russ_Eng VALUES (\"{k}\", \"{v}\", \"\")")
		conn.commit()
	conn.close()

if __name__ == '__main__':
	main()
