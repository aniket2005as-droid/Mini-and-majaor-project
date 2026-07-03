from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
from datetime import date

con = sqlite3.connect("library.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS lend (
    lend_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    book_name TEXT,
    member_id INTEGER,
    member_name TEXT,
    issue_date TEXT,
    status TEXT DEFAULT 'Lent'
)""")
con.commit()


class LendBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("750x650+400+50")   # ← wider and taller window
        self.title("Lend Book")
        self.resizable(True, True)         # ← allow resize
        self.config(bg="#f8f8f8")

        self.selected_book_id   = None
        self.selected_member_id = None

        # ── header ──────────────────────────────────────────────
        topFrame = Frame(self, height=60, bg="#003f8a")
        topFrame.pack(fill=X)
        Label(topFrame, text="📚  Lend Book", font="arial 18 bold",
              bg="#003f8a", fg="white").pack(pady=10)

        # ── SCROLLABLE CANVAS SETUP ──────────────────────────────
        canvas = Canvas(self, bg="#f8f8f8")
        scrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # inner frame inside canvas
        bodyFrame = Frame(canvas, bg="#f8f8f8")
        canvas_window = canvas.create_window((0, 0), window=bodyFrame, anchor=NW)

        # update scroll region when frame changes size
        def onFrameConfigure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def onCanvasConfigure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        bodyFrame.bind("<Configure>", onFrameConfigure)
        canvas.bind("<Configure>", onCanvasConfigure)

        # mousewheel scroll
        def onMouseWheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", onMouseWheel)

        # ── BOOK SEARCH ─────────────────────────────────────────
        book_frame = LabelFrame(bodyFrame, text="Search Book",
                                font="arial 11 bold",
                                bg="#fcc324", fg="white", padx=8, pady=8)
        book_frame.pack(fill=X, padx=20, pady=8)

        Label(book_frame, text="Book Name :", font="arial 10 bold",
              bg="#fcc324", fg="white").grid(row=0, column=0, padx=5, pady=4)
        self.ent_book_search = Entry(book_frame, width=28, bd=3)
        self.ent_book_search.grid(row=0, column=1, padx=5, pady=4)
        Button(book_frame, text="Search", font="arial 9 bold",
               bg="#003f8a", fg="white",
               command=self.searchBook).grid(row=0, column=2, padx=8)

        self.list_books = Listbox(book_frame, width=55, height=4,   # ← smaller height
                                  font="times 10", bd=3)
        self.list_books.grid(row=1, column=0, columnspan=3, pady=4)
        self.list_books.bind("<<ListboxSelect>>", self.selectBook)

        self.lbl_selected_book = Label(book_frame,
                                       text="Selected Book : None",
                                       font="arial 10 bold",
                                       bg="#fcc324", fg="white")
        self.lbl_selected_book.grid(row=2, column=0, columnspan=3, pady=4)

        # ── MEMBER SEARCH ────────────────────────────────────────
        member_frame = LabelFrame(bodyFrame, text="Search Member",
                                  font="arial 11 bold",
                                  bg="#9bc9ff", fg="white", padx=8, pady=8)
        member_frame.pack(fill=X, padx=20, pady=8)

        Label(member_frame, text="Member Name :", font="arial 10 bold",
              bg="#9bc9ff", fg="white").grid(row=0, column=0, padx=5, pady=4)
        self.ent_member_search = Entry(member_frame, width=28, bd=3)
        self.ent_member_search.grid(row=0, column=1, padx=5, pady=4)
        Button(member_frame, text="Search", font="arial 9 bold",
               bg="#003f8a", fg="white",
               command=self.searchMember).grid(row=0, column=2, padx=8)

        self.list_members = Listbox(member_frame, width=55, height=4,  # ← smaller height
                                    font="times 10", bd=3)
        self.list_members.grid(row=1, column=0, columnspan=3, pady=4)
        self.list_members.bind("<<ListboxSelect>>", self.selectMember)

        self.lbl_selected_member = Label(member_frame,
                                         text="Selected Member : None",
                                         font="arial 10 bold",
                                         bg="#9bc9ff", fg="white")
        self.lbl_selected_member.grid(row=2, column=0, columnspan=3, pady=4)

        # ── ISSUE DATE ───────────────────────────────────────────
        date_frame = LabelFrame(bodyFrame, text="Issue Date",
                                font="arial 11 bold",
                                bg="#e0f0f0", padx=8, pady=8)
        date_frame.pack(fill=X, padx=20, pady=8)

        Label(date_frame, text="Issue Date :", font="arial 10 bold",
              bg="#e0f0f0").grid(row=0, column=0, padx=5)
        self.ent_issue_date = Entry(date_frame, width=20, bd=3)
        self.ent_issue_date.insert(0, str(date.today()))
        self.ent_issue_date.grid(row=0, column=1, padx=5)

        # ── ACTION BUTTONS ───────────────────────────────────────
        btn_frame = Frame(bodyFrame, bg="#f8f8f8")
        btn_frame.pack(pady=15)

        Button(btn_frame, text="✅  Lend Book",
               font="arial 12 bold", bg="#003f8a", fg="white",
               width=14, command=self.lendBook).grid(row=0, column=0, padx=15)

        Button(btn_frame, text="🔄  Return Book",
               font="arial 12 bold", bg="#e74c3c", fg="white",
               width=14, command=self.returnBook).grid(row=0, column=1, padx=15)

        # ── LEND RECORDS TABLE ───────────────────────────────────
        record_frame = LabelFrame(bodyFrame, text="Current Lend Records",
                                  font="arial 11 bold", bg="#f8f8f8",
                                  padx=5, pady=5)
        record_frame.pack(fill=BOTH, padx=20, pady=8)

        cols = ("Lend ID", "Book", "Member", "Issue Date", "Status")
        self.tree = ttk.Treeview(record_frame, columns=cols,
                                 show="headings", height=5)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor=CENTER)

        # scrollbar for table
        tree_scroll = Scrollbar(record_frame, orient=HORIZONTAL,
                                command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_scroll.set)
        self.tree.pack(fill=BOTH)
        tree_scroll.pack(fill=X)

        self.loadRecords()

    # ── BOOK SEARCH ──────────────────────────────────────────────
    def searchBook(self):
        value = self.ent_book_search.get().strip()
        results = cur.execute(
            "SELECT * FROM books WHERE book_name LIKE ? AND book_status=0",
            ('%' + value + '%',)
        ).fetchall()
        self.list_books.delete(0, END)
        if not results:
            self.list_books.insert(END, "No available books found.")
            return
        for book in results:
            self.list_books.insert(END, str(book[0]) + " - " + book[1]
                                   + " | Author: " + book[2])

    def selectBook(self, evt):
        if not self.list_books.curselection():
            return
        value = self.list_books.get(self.list_books.curselection())
        if "No available" in value:
            return
        self.selected_book_id = value.split(" - ")[0]
        book_name = value.split(" - ")[1].split(" | ")[0]
        self.lbl_selected_book.config(text="Selected Book : " + book_name)

    # ── MEMBER SEARCH ─────────────────────────────────────────────
    def searchMember(self):
        value = self.ent_member_search.get().strip()
        results = cur.execute(
            "SELECT * FROM members WHERE member_name LIKE ?",
            ('%' + value + '%',)
        ).fetchall()
        self.list_members.delete(0, END)
        if not results:
            self.list_members.insert(END, "No members found.")
            return
        for member in results:
            self.list_members.insert(END, str(member[0]) + " - " + member[1]
                                     + " | Phone: " + member[2])

    def selectMember(self, evt):
        if not self.list_members.curselection():
            return
        value = self.list_members.get(self.list_members.curselection())
        if "No members" in value:
            return
        self.selected_member_id = value.split(" - ")[0]
        member_name = value.split(" - ")[1].split(" | ")[0]
        self.lbl_selected_member.config(text="Selected Member : " + member_name)

    # ── LEND BOOK ─────────────────────────────────────────────────
    def lendBook(self):
        if not self.selected_book_id:
            messagebox.showerror("Error", "Please select a book first!")
            return
        if not self.selected_member_id:
            messagebox.showerror("Error", "Please select a member first!")
            return

        issue_date = self.ent_issue_date.get().strip()
        if issue_date == "":
            messagebox.showerror("Error", "Please enter an issue date!")
            return

        book   = cur.execute("SELECT book_name FROM books WHERE book_id=?",
                             (self.selected_book_id,)).fetchone()
        member = cur.execute("SELECT member_name FROM members WHERE member_id=?",
                             (self.selected_member_id,)).fetchone()

        try:
            cur.execute("""INSERT INTO lend
                           (book_id, book_name, member_id, member_name, issue_date, status)
                           VALUES (?, ?, ?, ?, ?, 'Lent')""",
                        (self.selected_book_id, book[0],
                         self.selected_member_id, member[0], issue_date))
            cur.execute("UPDATE books SET book_status=1 WHERE book_id=?",
                        (self.selected_book_id,))
            con.commit()
            messagebox.showinfo("Success",
                                f"'{book[0]}' lent to '{member[0]}' successfully!")
            self.resetSelection()
            self.loadRecords()

        except Exception as e:
            messagebox.showerror("Error", f"Could not lend book:\n{e}")

    # ── RETURN BOOK ───────────────────────────────────────────────
    def returnBook(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error",
                                 "Please select a record from the table to return!")
            return

        record    = self.tree.item(selected[0])["values"]
        lend_id   = record[0]
        book_name = record[1]

        lend = cur.execute("SELECT book_id FROM lend WHERE lend_id=?",
                           (lend_id,)).fetchone()
        if not lend:
            messagebox.showerror("Error", "Record not found!")
            return

        try:
            cur.execute("UPDATE lend SET status='Returned' WHERE lend_id=?",
                        (lend_id,))
            cur.execute("UPDATE books SET book_status=0 WHERE book_id=?",
                        (lend[0],))
            con.commit()
            messagebox.showinfo("Success", f"'{book_name}' returned successfully!")
            self.loadRecords()

        except Exception as e:
            messagebox.showerror("Error", f"Could not return book:\n{e}")

    # ── LOAD RECORDS ──────────────────────────────────────────────
    def loadRecords(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        records = cur.execute(
            "SELECT lend_id, book_name, member_name, issue_date, status FROM lend"
        ).fetchall()
        for record in records:
            self.tree.insert("", END, values=record)

    # ── RESET ─────────────────────────────────────────────────────
    def resetSelection(self):
        self.selected_book_id   = None
        self.selected_member_id = None
        self.lbl_selected_book.config(text="Selected Book : None")
        self.lbl_selected_member.config(text="Selected Member : None")
        self.list_books.delete(0, END)
        self.list_members.delete(0, END)
        self.ent_book_search.delete(0, END)
        self.ent_member_search.delete(0, END)
        self.ent_issue_date.delete(0, END)
        self.ent_issue_date.insert(0, str(date.today()))