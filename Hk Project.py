import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",            
        password="techboyhk0005@",  
        database="school_db"    
    )

def add_teacher():
    name = name_entry.get()
    subject = subject_entry.get()
    dept = dept_entry.get()
    years_of_experience = years_entry.get()
    salary = salary_entry.get()

    if not (name and subject and dept and years_of_experience and salary):
        messagebox.showerror("Input Error", "Please fill all fields")
        return

    try:
        years_of_experience = int(years_of_experience)
        salary = float(salary)
    except ValueError:
        messagebox.showerror("Input Error", "Years of experience must be an integer and salary must be a number")
        return

    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO teachers (name, subject, dept, years_of_experience, salary)
        VALUES (%s, %s, %s, %s, %s)
    ''', (name, subject, dept, years_of_experience, salary))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Teacher added successfully")
    display_teachers()
    clear_fields()

def modify_teacher():
    teacher_id = id_entry.get()
    name = name_entry.get()
    subject = subject_entry.get()
    dept = dept_entry.get()
    years_of_experience = years_entry.get()
    salary = salary_entry.get()

    if not (teacher_id and name and subject and dept and years_of_experience and salary):
        messagebox.showerror("Input Error", "Please fill all fields")
        return

    try:
        years_of_experience = int(years_of_experience)
        salary = float(salary)
    except ValueError:
        messagebox.showerror("Input Error", "Years of experience must be an integer and salary must be a number")
        return

    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE teachers
        SET name = %s, subject = %s, dept = %s, years_of_experience = %s, salary = %s
        WHERE id = %s
    ''', (name, subject, dept, years_of_experience, salary, teacher_id))
    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showerror("Update Error", "No record found with the given ID")
    else:
        messagebox.showinfo("Success", "Record updated successfully")

    conn.close()
    display_teachers()
    clear_fields()

def delete_teacher():
    teacher_id = id_entry.get()

    if not teacher_id:
        messagebox.showerror("Input Error", "Please provide an ID to delete")
        return

    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM teachers WHERE id = %s', (teacher_id,))
    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showerror("Delete Error", "No record found with the given ID")
    else:
        messagebox.showinfo("Success", "Teacher deleted successfully")

    conn.close()
    display_teachers()
    clear_fields()

def display_teachers():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM teachers')
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)
    conn.close()

def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    years_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Teacher Information")

tk.Label(root, text="ID").grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

tk.Label(root, text="Name:").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="Subject:").grid(row=2, column=0)
subject_entry = tk.Entry(root)
subject_entry.grid(row=2, column=1)

tk.Label(root, text="Dept:").grid(row=3, column=0)
dept_entry = tk.Entry(root)
dept_entry.grid(row=3, column=1)

tk.Label(root, text="Years of Experience:").grid(row=4, column=0)
years_entry = tk.Entry(root)
years_entry.grid(row=4, column=1)

tk.Label(root, text="Salary:").grid(row=5, column=0)
salary_entry = tk.Entry(root)
salary_entry.grid(row=5, column=1)

# Buttons in a single horizontal row
button_frame = tk.Frame(root)
button_frame.grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(button_frame, text="Add Teacher", command=add_teacher).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Modify Teacher", command=modify_teacher).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete Teacher", command=delete_teacher).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Clear Fields", command=clear_fields).pack(side=tk.LEFT, padx=5)

columns = ("id", "name", "subject", "dept", "years_of_experience", "salary")
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=100)

tree.grid(row=7, column=0, columnspan=2, pady=10)

display_teachers()

root.mainloop
