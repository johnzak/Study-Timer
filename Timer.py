# # Vaccum Code
from tkinter import *
from tkinter import ttk
import time
import threading
import os
from datetime import date
from tkinter import messagebox


class gui_test:
    def __init__(self,root):
        
        self.root = root
        self.root.title("Study Timer")
        self.root.geometry("350x240+0+0")
        self.root.resizable(False,False)
        
        self.hours = IntVar()
        self.minutes = IntVar()
        self.todo = StringVar()

        self.minutes.set(20)

        frame_change = LabelFrame(self.root, bd=2, width=340, height=80, relief=RIDGE, text="Timer", font=('tahoma', 14))

        frame_change.place(x=5, y=5, width=340, height=80)

        self.choose_time()
        self.lbl = Label(frame_change, text="", font=('tahoma', 14))
        self.lbl.pack(pady=8)

        lbl2 = Label(self.root, text="To Do", font=('arial', 10))
        lbl2.place(x=2, y = 95)

        todo = ttk.Entry(self.root, width=28, textvariable=self.todo, font=('arial', 12))
        todo.place(x=42, y = 93)

        add_btn = ttk.Button(self.root, text="Add", width=6,command=self.add_data)
        add_btn.place(x=300, y=90, height=32)


        
        #?      -----------Data TreeView------------------


        data_table = Frame(self.root, bd=2, relief=RIDGE)
        data_table.place(x=5, y=125, width=340, height=110)


        scroll_x = ttk.Scrollbar(data_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(data_table, orient=VERTICAL)

        self.cli_table = ttk.Treeview(data_table, columns=('User-Name'), xscrollcommand=scroll_x.set)

        scroll_y.pack(side=RIGHT, fill=Y)


        scroll_x.config(command=self.cli_table.xview)



        self.cli_table.heading('User-Name', text='To Do')



        self.cli_table['show'] = 'headings'



        self.cli_table.pack(fill=BOTH, expand=1)

        self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        try:
            todo_file = open(f"{self.desktop_path}\\todo.txt", "a")
        except FileNotFoundError:
            new_path = self.desktop_path[:14] + "\\OneDrive" + self.desktop_path[14:]
            todo_file = open(f"{new_path}\\todo.txt", "a")


        today = date.today().strftime("%d-%m-%Y")

        todo_file.write(f"\n\n\n######## {today} ########\n")



        todo_file.close()

    def add_data(self):
        self.cli_table.insert("", END, values=[self.todo.get()])


        try:
            todo_file = open(f"{self.desktop_path}\\todo.txt", "a")
        except FileNotFoundError:
            new_path = self.desktop_path[:14] + "\\OneDrive" + self.desktop_path[14:]
            todo_file = open(f"{new_path}\\todo.txt", "a")


        todo_file.write(f"\n- {self.todo.get()}")

        todo_file.close()

        self.todo.set("")

    def choose_time(self):

        self.top = Toplevel()

        self.top.geometry('240x140+650+250')
        self.top.title("Set Time")
        self.top.resizable(False,False)
        
        
        frame_change = Frame(self.top, bd=2, width=400, height=80)

        frame_change.place(x=30, y=10)


        lbl_cli_address1 = Label(frame_change, text="Hrs", font=('tahoma', 14), padx=10, pady=6)
        lbl_cli_address1.grid(row=1, column=4)

        entry_cli_address1 = ttk.Entry(frame_change, width=6, textvariable=self.hours, font=('arial', 16))
        entry_cli_address1.grid(row=2, column=4, padx=5,pady=5)
        lbl_cli_label = Label(frame_change, text="Mins", font=('tahoma', 14), padx=10, pady=6)
        lbl_cli_label.grid(row=1, column=6)

        entry_cli_address1 = ttk.Entry(frame_change, width=6, textvariable=self.minutes, font=('arial', 16))
        entry_cli_address1.grid(row=2, column=6)
        save_btn = ttk.Button(self.top, text="Start", width=16,command=lambda:[self.start_thread(), self.top.destroy()])

        save_btn.place(x=60, y=100,height=30)


    def start_thread(self):
        if int(self.hours.get()) == 0 and int(self.minutes.get()) == 0:
            messagebox.showerror("Error", "Can't set timer to 0 !!")
            self.top.destroy()
            self.choose_time()
        thr = threading.Thread(target=self.timer, daemon=True)
        thr.start()



    def timer(self, inhrs = 0, inmins = 0):

        inhrs = self.hours.get()
        inmins = self.minutes.get()

        print(inhrs, inmins)



        start = time.ctime(time.time())[11:16]
            
        hrs = int(start[0:2])
        mins = int(start[3:5])



        if mins + inmins == 60:
            inhrs += 1
            mins = 0

        elif mins + inmins > 60:
            mod = int((mins + inmins) / 60)
            hrs += mod
            mins -= 60 * mod


        if mins + inmins < 10:
            end = f'{hrs + inhrs}:0{mins + inmins}'
        
        else:
            end = f'{hrs + inhrs}:{mins + inmins}'



        printed = ""

        print(end)

        inmins -= 1


        while  time.ctime(time.time())[11:16] != end:
        
            time.sleep(0.2)
            timenow = time.ctime(time.time())[11:19]
            secs = 60 - int(time.ctime(time.time())[17:19])
            if secs == 60:
                secs = 0
            if secs < 10:
                secs = f"0{secs}"
            if timenow != printed:
                if inmins < 10:
                    self.lbl['text'] = f"0{inhrs}:0{inmins}:{secs}"
                else:
                    self.lbl['text'] = f"0{inhrs}:{inmins}:{secs}"





                if int(secs) == 0:
                    inmins -= 1
                    if inmins == -1:
                        inmins = 59
                        inhrs -= 1
                printed = timenow


        while True:
            if self.lbl['fg'] == "red":
                time.sleep(0.5)
                self.lbl['fg'] = "black"
            else:
                time.sleep(0.5)
                self.lbl['fg'] = "red"





#?--------------variables-------------



if __name__ == "__main__":
    root = Tk()
    app = gui_test(root)
    root.mainloop()








#! I did it befor project