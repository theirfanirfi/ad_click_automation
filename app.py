import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from utils import read_input_data, write_input_data, read_keywords, write_keywords, read_account, write_account
from login import login_chrome
import random

def login():
    login_chrome()

def execute():

    from_time= from_time_entry.get()
    to_time= to_time_entry.get()

    iterations = iterations_entry.get()
    website = website_entry.get()
    keywords = keywords_entry.get()
    use_randomness = randomness_var.get()

    email= email_entry.get()
    password= password_entry.get()

    input_data_from_file = read_input_data()
    keywords_in_file = read_keywords()


    # print(account)


    print(keywords_in_file)
    iterations_in_file = input_data_from_file[0] if iterations == "" else iterations
    website_in_file = input_data_from_file[1] if website == "" else website
    from_time_selection_in_file = input_data_from_file[2] if from_time == "" else from_time
    to_time_selection_in_file = input_data_from_file[3] if to_time == "" else to_time
    is_randomness_in_file = input_data_from_file[4] if use_randomness == "" else use_randomness
    keywordss = keywords_in_file if keywords == "" else keywords

    email_from_file = email_from_file if email == "" else email
    password_from_file = password_from_file if password == "" else password


    print(keywordss)
    write_keywords(keywordss)
    input_to_be_written = f"{iterations_in_file}\t{website_in_file}\t{from_time}\t{to_time}\t{is_randomness_in_file}"
    write_input_data(input_to_be_written)

    write_account(f"{email_from_file}\t{password_from_file}")

    # from_t = from_time[:2]
    # to_t = to_time[:2]
    # print(random.randint(int(from_t), int(to_t)))
    
    # cron_command = f"00 12 * * * main.py"
    subprocess.run(["python3", "main.py", "&"])
    
   
    # existing_cron_jobs = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    # if cron_command in existing_cron_jobs:
    #     # Remove existing cron job
    #     subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE)
    #     subprocess.run(["crontab", "-r"], stdout=subprocess.PIPE)
    #     print("Existing cron job removed.")

   
    # subprocess.run(["echo", cron_command], stdout=subprocess.PIPE)
    # subprocess.run(["crontab", "-"], input=cron_command.encode(), stdout=subprocess.PIPE)

    # if use_randomness:
    #     print("Cron job with randomness added successfully.")
    # else:
    #     print("Cron job without randomness added successfully.")

def create_app():
    app = tk.Tk()
    app.title("Ad Click Automation bot")

    # Input fields
    global email_text, password_text,email_entry,password_entry,from_time_entry,to_time_entry, iterations_entry, website_entry, keywords_entry, randomness_var
    
    email_text = tk.StringVar()
    password_text = tk.StringVar()

    form_text = tk.StringVar()
    to_text = tk.StringVar()

    iterations_text = tk.StringVar()
    website_text = tk.StringVar()

    keywords_text = tk.StringVar()

    account = read_account()

    email_text.set(account.split('\t')[0])
    password_text.set(account.split('\t')[1])

    keywords_text.set(read_keywords())

    inputs = read_input_data()
    print('inputs', inputs[0])
    iterations_text.set(inputs[0])
    form_text.set(inputs[2])
    to_text.set(inputs[3])

    website_text.set(inputs[1])


    from_time_label = ttk.Label(app, text="From Time")
    from_time_label.grid(row=0, column=0, padx=5, pady=5)
    times = [f"{i:02d}:00" for i in range(24)]  # Generate list of times in HH:00 format
    from_time_entry = ttk.Combobox(app, values=times)
    from_time_entry.grid(row=0, column=1, padx=5, pady=5)

    to_time_label = ttk.Label(app, text="To Time")
    to_time_label.grid(row=1, column=0, padx=5, pady=5)
    to_time_entry = ttk.Combobox(app, values=times, textvariable=to_text)
    to_time_entry.grid(row=1, column=1, padx=5, pady=5)

    iterations_label = ttk.Label(app, text="Number of Iterations:")
    iterations_label.grid(row=2, column=0, padx=5, pady=5)
    iterations_entry = ttk.Entry(app, textvariable=iterations_text)
    iterations_entry.grid(row=2, column=1, padx=5, pady=5)

    website_label = ttk.Label(app, text="Website:")
    website_label.grid(row=3, column=0, padx=5, pady=5)
    website_entry = ttk.Entry(app, textvariable=website_text)
    website_entry.grid(row=3, column=1, padx=5, pady=5)

    keywords_label = ttk.Label(app, text="Keywords:")
    keywords_label.grid(row=4, column=0, padx=5, pady=5)
    keywords_entry = ttk.Entry(app, textvariable=keywords_text)
    keywords_entry.grid(row=4, column=1, padx=5, pady=5)

    # Switch for randomness
    randomness_label = ttk.Label(app, text="ad click to be random?:")
    randomness_label.grid(row=5, column=0, padx=5, pady=5)
    randomness_var = tk.BooleanVar()
    randomness_switch = ttk.Checkbutton(app, variable=randomness_var)
    randomness_switch.grid(row=5, column=1, padx=5, pady=5)

    email = ttk.Label(app, text="Email")
    email.grid(row=6, column=0, padx=5, pady=5)
    email_entry = ttk.Entry(app,textvariable=email_text)
    email_entry.grid(row=6, column=1, padx=5, pady=5)

    password = ttk.Label(app, text="Password")
    password.grid(row=7, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(app,textvariable=password_text)
    password_entry.grid(row=7, column=1, padx=5, pady=5)

    # Buttons
    login_button = ttk.Button(app, text="Login", command=login)
    login_button.grid(row=8, column=0, padx=5, pady=5)

    execute_button = ttk.Button(app, text="Execute", command=execute)
    execute_button.grid(row=8, column=1, padx=5, pady=5)

    return app

if __name__ == "__main__":
    app = create_app()
    app.mainloop()
