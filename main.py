from customtkinter import *
import webbrowser
from tkinter import filedialog as fd
from tkinter import StringVar
from process_data import process_data
from extract_values import extract_values
import csv
import threading
import queue

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

progress_queue = queue.Queue()

def callback(url):
    webbrowser.open_new(url)

def select_file():
    global file_path
    filetypes = (
        ('text files', '*.json'),
        ('All files', '*.*')
    )
    file_path.set(fd.askopenfilename(
        title='Open a file',
        filetypes=filetypes)
    )
    
    print(file_path)

def check_progress():
    global app, progress_label, progress_bar, dump
    try:
        while True:
            value = progress_queue.get_nowait()
            print(value)
            progress_bar.set(value)  # CTk progress bar expects 0.0–1.0
            progress_label.configure(text=f"{(value*100):.2f}%")
            if progress_bar.get() == 100.00:
                dump.configure(state="normal")
    except queue.Empty:
        pass
    app.after(50, check_progress)  # Keep checking

def button_thread():
    global app, progress_frame, dump
    app.geometry("500x350")
    dump.pack_forget()
    progress_frame.pack(pady=20)
    dump.pack(pady=(0,20))
    dump.configure(state="disabled")
    threading.Thread(target=button_event, daemon=True).start()
    check_progress()


def button_event():
    global file_path
    global id_user
    marketHistory = file_path.get()
    idUser = id_user.get()
    file = open(marketHistory, "r", encoding="utf8")
    file = file.read()
    pd = process_data(file).process()
    vd = extract_values(idUser).process(progress_queue)

    with open('result.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(['Item', 'Valor Pago', 'Valor Atual', 'Diferença'])
        index = 1
        for key in vd:
            # print(key)
            # progress_queue.put(index)
            index = index + 1
            spamwriter.writerow([key, pd.get(key, 'R$ 0,00'), vd[key], f"=SEERRO((C{index}-B{index})/B{index};0)"])

        spamwriter.writerow([])
        last_row = index + 2
        spamwriter.writerow([
            'Total',
            f'=SUM(B2:B{index})',
            f'=SUM(C2:C{index})',
            f'=SEERRO((C{last_row}-B{last_row})/B{last_row}; 0)'
        ])

app = CTk()
app.geometry("500x250")
app.title("CS Inventory Dumper")
app.resizable(False, False)

file_path = StringVar(master=app, value='File')
label_guide = CTkLabel(app, text='Click on link below, and save the content with Ctrl+s on your browser', width=40, height=28, fg_color='transparent')
label_guide.pack(padx=20, pady=(20,0))

click_me =  CTkLabel(app, text='click me', width=40, height=28, fg_color='transparent', cursor="hand2", text_color="blue")
click_me.pack(padx=20)
click_me.bind("<Button-1>", lambda e: callback("https://steamcommunity.com/market/myhistory?count=500"))

frame = CTkFrame(app, fg_color="transparent")
frame.pack(padx=20, pady=20)
file_entry = CTkEntry(frame, placeholder_text='File', textvariable=file_path, width=300, height=28, state='disabled')
file_entry.pack(side='left',padx=(0, 20))

button = CTkButton(frame, text="Open File", command=select_file)
button.pack(side='right')

id_user = CTkEntry(app, placeholder_text='ID User', width=300)
id_user.pack(pady=(0,20), padx=20, fill='x')

progress_frame = CTkFrame(app, fg_color="transparent")
progress_label = CTkLabel(progress_frame, text="0%")
progress_label.pack()

progress_bar = CTkProgressBar(progress_frame, width=300)
progress_bar.pack()
progress_bar.set(0)


dump = CTkButton(app, text='Dump', command=button_thread)
dump.pack(pady=(0,20))

app.mainloop()