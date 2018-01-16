import subjects
import mp_cat

def run():
	while True:
		print("1. Categorize emails\n2. Show emails(categorized) of a particular category\n3. Exit")
		choice = input("Enter selection: ")
		if choice=="1":
			subjects.read_emails()
		elif choice=="2":
			subjects.disp_emails()
		else:
			exit()

if __name__=="__main__":
	run()
