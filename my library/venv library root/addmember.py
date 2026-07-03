from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()


class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Member")
        self.resizable(False, False)

        # ── frames ──────────────────────────────────────────────
        self.topframe = Frame(self, height=150, bg="white")
        self.topframe.pack(fill=X)

        self.bottomframe = Frame(self, height=600, bg="#fcc324")
        self.bottomframe.pack(fill=X)

        # ── header ──────────────────────────────────────────────
        self.top_image = PhotoImage(file="icons/addperson.png")
        Label(self.topframe, image=self.top_image, bg="white").place(x=120, y=10)
        Label(self.topframe, text=" Add Member ", font="arial 22 bold",
              fg="#003f8a", bg="white").place(x=290, y=60)

        # ── entry fields ────────────────────────────────────────
        Label(self.bottomframe, text="Name :", font="arial 15 bold",
              bg="#fcc324", fg="white").place(x=40, y=40)
        self.ent_name = Entry(self.bottomframe, width=30, bd=4)
        self.ent_name.place(x=150, y=45)

        Label(self.bottomframe, text="Phone :", font="arial 15 bold",
              bg="#fcc324", fg="white").place(x=40, y=80)
        self.ent_phone = Entry(self.bottomframe, width=30, bd=4)
        self.ent_phone.place(x=150, y=85)

        Button(self.bottomframe, text="Add Member", font="arial 12 bold",
               bg="#003f8a", fg="white",
               command=self.addMember).place(x=250, y=130)

    def addMember(self):
        name  = self.ent_name.get().strip()
        phone = self.ent_phone.get().strip()

        # Fixed: each field checked individually
        if name == "" or phone == "":
            messagebox.showerror("Error", "Fields can't be empty", icon="warning")
            return

        try:
            query = "INSERT INTO members (member_name, member_phone) VALUES (?, ?)"
            cur.execute(query, (name, phone))
            con.commit()
            messagebox.showinfo("Success", "Member added successfully!")
            # Clear fields after success
            self.ent_name.delete(0, END)
            self.ent_phone.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Can't add to database:\n{e}",
                                 icon="warning")