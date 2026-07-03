from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()


class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Book")
        self.resizable(False, False)

        # ── frames ──────────────────────────────────────────────
        self.topframe = Frame(self, height=150, bg="white")
        self.topframe.pack(fill=X)

        self.bottomframe = Frame(self, height=600, bg="#fcc324")
        self.bottomframe.pack(fill=X)

        # ── header ──────────────────────────────────────────────
        self.top_image = PhotoImage(file="icons/addbook.png")
        Label(self.topframe, image=self.top_image, bg="white").place(x=120, y=10)
        Label(self.topframe, text=" Add Book ", font="arial 22 bold",
              fg="#003f8a", bg="white").place(x=290, y=60)

        # ── entry fields ────────────────────────────────────────
        Label(self.bottomframe, text="Name :", font="arial 15 bold",
              bg="#fcc324", fg="white").place(x=40, y=40)
        self.ent_name = Entry(self.bottomframe, width=30, bd=4)
        self.ent_name.place(x=150, y=45)

        Label(self.bottomframe, text="Author :", font="arial 15 bold",
              bg="#fcc324", fg="white").place(x=40, y=80)
        self.ent_author = Entry(self.bottomframe, width=30, bd=4)
        self.ent_author.place(x=150, y=85)

        Label(self.bottomframe, text="Page :", font="arial 15 bold",
              bg="#fcc324", fg="white").place(x=40, y=120)
        self.ent_page = Entry(self.bottomframe, width=30, bd=4)
        self.ent_page.place(x=150, y=125)

        Label(self.bottomframe, text="Language :", font="arial 15 bold",
              bg="#fcc324", fg="white").place(x=40, y=160)
        self.ent_language = Entry(self.bottomframe, width=30, bd=4)
        self.ent_language.place(x=150, y=165)

        Button(self.bottomframe, text="Add Book", font="arial 12 bold",
               bg="#003f8a", fg="white",
               command=self.addBook).place(x=250, y=210)

    def addBook(self):
        name     = self.ent_name.get().strip()
        author   = self.ent_author.get().strip()
        page     = self.ent_page.get().strip()
        language = self.ent_language.get().strip()

        # Fixed: each field checked individually against empty string
        if name == "" or author == "" or page == "" or language == "":
            messagebox.showerror("Error", "Fields can't be empty", icon="warning")
            return

        try:
            query = """INSERT INTO books
                       (book_name, book_author, book_page, book_language)
                       VALUES (?, ?, ?, ?)"""
            cur.execute(query, (name, author, page, language))
            con.commit()
            messagebox.showinfo("Success", "Successfully add in database!")
            # Clear fields after success
            self.ent_name.delete(0, END)
            self.ent_author.delete(0, END)
            self.ent_page.delete(0, END)
            self.ent_language.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Can't add to database:\n{e}",
                                 icon="warning")