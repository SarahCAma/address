from tkinter import *
from tkinter import ttk, font
import sqlite3
from sqlite3 import Error
from functools import partial


root = Tk()
root.title("Address Book")
root.iconbitmap('book2.ico')
root.geometry("600x425")

db = "address_book.db"

# photo = PhotoImage(file = 'm-logo.png')
# root.iconphoto(True, photo)

# ttk.Style().configure("frameStyle.TFrame", background="black", borderwidth=15, width=500)
font_style = font.Font(family="Calibri Light", size=10, weight="bold")

s = ttk.Style()
s.configure('font.TButton', font=font_style)
s.configure('font.Treeview.Heading', font=font_style)
s.configure('font.Treeview', font=('Calibri Light', '9'))
s.configure('error.TLabel', font=font_style, foreground='red')
s.configure('error2.TLabel', font=('Calibri Light', '9', 'bold'), foreground='red')

mainframe = ttk.Frame(root, padding=20)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=2)
mainframe.pack()

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')

frame2 = ttk.Frame(root, padding=20)
frame2.columnconfigure(0, weight=2)
frame2.columnconfigure(1, weight=1)
frame2.pack()

find_record_text = ttk.Label(frame2, text="Find record by ID:", font=font_style).grid(column=0, row=0, sticky=E, pady=5)
find_record = ttk.Entry(frame2)
find_record.grid(column=1, row=0, sticky=E, padx=(25,0), pady=5)

searchframe = ttk.Frame(root, padding=20)
searchframe.rowconfigure(0, weight=1)
searchframe.rowconfigure(1, weight=2)
searchframe.rowconfigure(2, weight=1)
searchframe.rowconfigure(3, weight=1)
searchframe.rowconfigure(4, weight=1)
searchframe_title = ttk.Label(searchframe, font=font_style)

error_msg1 = ttk.Label(mainframe, text="Please complete all fields to add record", style='error.TLabel')
error_msg2 = ttk.Label(searchframe, style='error2.TLabel')



result_id_l = ttk.Label(searchframe, text="Record ID: ")
result_id = ttk.Label(searchframe)

result_table = ttk.Treeview(searchframe, columns=('ID', 'f_name', 'l_name', 'address', 'city', 'postcode'), height=1, style='font.Treeview')

delete_btn = ttk.Button(searchframe, text="Delete Record", style="font.TButton")
homepage_btn = ttk.Button(searchframe, text="Back to Main Page")


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    

    return conn


def create_table(conn, create_table_sql):
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    
    create_addresses_table = """ CREATE TABLE IF NOT EXISTS addresses (
                                    id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    address text NOT NULL,
                                    city text NOT NULL,
                                    postcode text NOT NULL
                            ) """

    
    conn = create_connection(db)

    if conn is not None:
        create_table(conn, create_addresses_table)
    else:
        print("Error! Cannot create db connection.")



def submit():

    entries = [f_name, l_name, address, city, postcode]
 
    if any(entry.get() == '' for entry in entries):
        error_msg1.grid_forget()
        error_msg1.grid(column=1, row=7)
        print("Record cannot be added with blank fields!")
    else:
        print("Record can be added!")
    
        db = "address_book.db"

        conn = create_connection(db)

        with conn:
            c = conn.cursor()
            c.execute("INSERT INTO addresses (first_name, last_name, address, city, postcode) VALUES (?, ?, ?, ?, ?)",
                    (f_name.get(), l_name.get(), address.get(), city.get(), postcode.get())
                    )
            conn.commit()
            # conn.close()
            print(f"Record addedd successfully. New record ID: {c.lastrowid}")

            search2('display', c.lastrowid)    

    for entry in entries:
        entry.delete(0, END)

        


def index():
  
    searchframe.pack_forget()
    error_msg1.grid_forget()
    error_msg2.grid_forget()
    find_record.delete(0, END)


    for row in result_table.get_children():
        result_table.delete(row)
        
    result_table.grid_forget()
    # for result in record_results:
    #     result.grid_forget()

    mainframe.pack()
    separator.pack(fill='x')
    frame2.pack()



def delete():

    for child in result_table.get_children():
        # for value in result_table.item(child)['values']:
        record_id = result_table.item(child)['values'][0]
        print(record_id)

    conn = create_connection(db)

    with conn:
        c = conn.cursor()
        c.execute("DELETE FROM addresses WHERE id=?", (record_id,))
        print(f"Record number {record_id} successfully deleted from db")
        conn.commit()


def search2(arg1, arg2=''):
    mainframe.pack_forget()
    separator.pack_forget()
    frame2.pack_forget()

    searchframe.pack()
    searchframe_title.grid(row=0, pady=20)
    result_table.grid(row=1)

    result_table.column("#0", width=0, stretch=NO)
    result_table.column('ID', anchor='center', width=50)
    result_table.column('f_name', anchor='center', width=100)
    result_table.column('l_name', anchor='center', width=100)
    result_table.column('address', anchor='center', width=100)
    result_table.column('city', anchor='center', width=100)
    result_table.column('postcode', anchor='center', width=100)

    result_table.heading('ID', text="ID")
    result_table.heading('f_name', text="First Name")
    result_table.heading('l_name', text="Surname")
    result_table.heading('address', text="Address")
    result_table.heading('city', text="City")
    result_table.heading('postcode', text="Postcode")


    delete_btn.configure(command=partial(search2, 'delete'))
    homepage_btn.configure(command=index, style="font.TButton")
    homepage_btn.grid(row=4, pady=20)
    
    conn = create_connection(db)

    if arg1 == 'display':
        searchframe_title.configure(text="Record Added")
        delete_btn.grid(row=3, sticky=E, pady=(20,0))
        # searchframe_title.grid(row=0, pady=20)
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM addresses WHERE id=?", [arg2])
            row = c.fetchall()
            print(row)

            result_table.insert('', index='end', text='', values=(row[0][0], row[0][1], row[0][2], row[0][3], row[0][4], row[0][5]))

    elif arg1 == 'search':
        searchframe_title.configure(text="Search Results")
        delete_btn.grid(row=3, sticky=E, pady=(20,0))
        arg2 = find_record.get()
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM addresses WHERE id=?", [arg2])
            row = c.fetchall()
            print(row)

            try:
                result_table.insert('', index='end', text='', values=(row[0][0], row[0][1], row[0][2], row[0][3], row[0][4], row[0][5]))
            except IndexError:
                print("This record does not exist!")
                error_msg2.configure(text=f"Record ( ID:{find_record.get()} ) does not exist")
                error_msg2.grid(row=2, pady=(20,0))
                delete_btn.grid_forget()

    elif arg1 == 'delete':
        for child in result_table.get_children():
            # for value in result_table.item(child)['values']:
            record_id = result_table.item(child)['values'][0]
        
        arg2 = record_id
        print(f"LINE 306 {record_id}")

        searchframe_title.configure(text=f"Record (ID:{arg2}) Deleted")

        # searchframe_title.grid(row=0, pady=20)
        with conn:
            c = conn.cursor()
            c.execute("DELETE FROM addresses WHERE id=?", [arg2])
            print(f"Record number {arg2} successfully deleted from db")
            conn.commit()

        for row in result_table.get_children():
            result_table.delete(row)
    else:
        print("This record does not exist!")
        error_msg2.configure(text=f"Record ( ID:{find_record.get()} ) does not exist")
        error_msg2.grid(row=2, pady=(20,0))
    return



## MAINFRAME ##

# Create entry textbox labels
f_name_l = ttk.Label(mainframe, text="First Name:", font=font_style).grid(column=0, row=0, sticky=E, padx=5, pady=5)
l_name_l = ttk.Label(mainframe, text="Surname:", font=font_style).grid(column=0, row=1, sticky=E, padx=5, pady=5)
address_l = ttk.Label(mainframe, text="Address:", font=font_style).grid(column=0, row=2, sticky=E, padx=5, pady=5)
city_l = ttk.Label(mainframe, text="City:", font=font_style).grid(column=0, row=3, sticky=E, padx=5, pady=5)
postcode_l = ttk.Label(mainframe, text="Postcode:", font=font_style).grid(column=0, sticky=E, padx=5, pady=5)


# Create entry textboxes
f_name = ttk.Entry(mainframe, width=30)
f_name.grid(column=1, row=0, sticky=E, padx=5, pady=5)

l_name = ttk.Entry(mainframe, width=30)
l_name.grid(column=1, row=1, sticky=E, padx=5, pady=5)

address = ttk.Entry(mainframe, width=30)
address.grid(column=1, row=2, sticky=E, padx=5, pady=5)

city = ttk.Entry(mainframe, width=30)
city.grid(column=1, row=3, sticky=E, padx=5, pady=5)

postcode = ttk.Entry(mainframe, width=30)
postcode.grid(column=1, row=4, sticky=E, padx=5, pady=5)

# Create buttons

submit_btn = ttk.Button(mainframe, text="Add Record", style="font.TButton", command=submit).grid(column=1, row=6, sticky=E, ipadx=5, padx=5, pady=5)
# quit_btn = ttk.Button(mainframe, text="Quit", width=20, command=root.destroy).grid(column=1, row=6, pady=10)

search_btn = ttk.Button(frame2, text="Search", command=partial(search2, 'search'), style="font.TButton").grid(column=1, row=1, sticky=E, padx=(25,0), pady=5)



if __name__ == '__main__':
    main()



root.mainloop()
