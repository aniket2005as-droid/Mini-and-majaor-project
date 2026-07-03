from tkinter import *
from tkinter import ttk
import sqlite3
import addbook
import addmember
import lendbook          


con = sqlite3.connect("library.db")
cur = con.cursor()



class Main(object):

    def __init__(self, master):
        self.master = master

        # ── frames ──────────────────────────────────────────────
        mainFrame = Frame(self.master)
        mainFrame.pack()

        topFrame = Frame(mainFrame, width=1350, height=70,
                         bg="#f8f8f8", relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP, fill=X, padx=20)

        centerFrame = Frame(mainFrame, width=1350, height=680,
                            bg="#e0f0f0", relief=RIDGE)
        centerFrame.pack(side=TOP)

        centerLeftFrame = Frame(centerFrame, width=900, height=700,
                                bg="#e0f0f0", relief="sunken", borderwidth=2)
        centerLeftFrame.pack(side=LEFT)

        centerRightFrame = Frame(centerFrame, width=450, height=700,
                                 bg="#e0f0f0", relief="sunken", borderwidth=2)
        centerRightFrame.pack()

        # ── search bar ──────────────────────────────────────────
        search_bar = LabelFrame(centerRightFrame, width=440, height=75,
                                text="Search Box", bg="#9bc9ff")
        search_bar.pack(fill=BOTH)

        self.lbl_search = Label(search_bar, text="Search :",
                                font="arial 12 bold", bg="#9bc9ff", fg="white")
        self.lbl_search.grid(row=0, column=0, padx=20, pady=10)

        self.ent_search = Entry(search_bar, width=30, bd=10)
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        self.bnt_search = Button(search_bar, text="Search",
                                 font="arial 12 bold", bg="#fcc324", fg="white",
                                 command=self.searchBooks)
        self.bnt_search.grid(row=0, column=4, padx=20, pady=10)

        # ── list/filter bar ─────────────────────────────────────
        list_bar = LabelFrame(centerRightFrame, width=440, height=175,
                              text="List Box", bg="#fcc324")
        list_bar.pack(fill=BOTH)

        lbl_list = Label(list_bar, text="Sort By",
                         font="times 16 bold", bg="#fcc324", fg="#2488ff")
        lbl_list.grid(row=0, column=2)

        self.listChoice = IntVar(value=1)
        Radiobutton(list_bar, text="All books",      variable=self.listChoice,
                    value=1, bg="#fcc324").grid(row=1, column=0)
        Radiobutton(list_bar, text="In Library",     variable=self.listChoice,
                    value=2, bg="#fcc324").grid(row=1, column=1)
        Radiobutton(list_bar, text="Borrowed books", variable=self.listChoice,
                    value=3, bg="#fcc324").grid(row=1, column=2)

        Button(list_bar, text="List Books", font="arial 12",
               bg="#2488ff", fg="white",
               command=self.listBooks).grid(row=1, column=3, padx=40, pady=10)

        # ── title / image ───────────────────────────────────────
        image_bar = Frame(centerRightFrame, width=440, height=350)
        image_bar.pack(fill=BOTH)

        Label(image_bar, text="Welcome to our Library",
              font="arial 16 bold").grid(row=0)
        self.image_library = PhotoImage(file="icons/library.png")
        Label(image_bar, image=self.image_library).grid(row=1)

        # ── toolbar buttons ─────────────────────────────────────
        self.iconbook = PhotoImage(file="icons/add_book.png")
        Button(topFrame, image=self.iconbook, text="Add Book",
               compound=LEFT, font="arial 12 bold",
               command=self.addBook).pack(side=LEFT, pady=10)

        self.iconmember = PhotoImage(file="icons/users.png")
        self.btnmember = Button(topFrame, text="Add Member",
                                font="arial 12 bold", padx=10,
                                command=self.addMember)
        self.btnmember.configure(image=self.iconmember, compound=LEFT)
        self.btnmember.pack(side=LEFT)

        # ── Give Book button (NOW CONNECTED) ────────────────────
        self.icongive = PhotoImage(file="icons/givebook.png")
        Button(topFrame, text="Give Book", font="arial 12 bold", padx=10,
               image=self.icongive, compound=LEFT,
               command=self.giveBook).pack(side=LEFT)   # ← command added

        # ── tabs ────────────────────────────────────────────────
        self.tabs = ttk.Notebook(centerLeftFrame, width=900, height=660)
        self.tabs.pack()

        self.tab1_icon = PhotoImage(file="icons/books.png")
        self.tab2_icon = PhotoImage(file="icons/members.png")
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Library Management",
                      image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text="Statistics",
                      image=self.tab2_icon, compound=LEFT)

        # ── Tab 1 – book listboxes ───────────────────────────────
        self.list_books = Listbox(self.tab1, width=40, height=30,
                                  bd=5, font="times 12 bold")
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.list_books.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=0, sticky=N+S+E)

        self.list_details = Listbox(self.tab1, width=80, height=30,
                                    bd=5, font="times 12 bold")
        self.list_details.grid(row=0, column=1, padx=(10, 0),
                               pady=10, sticky=N)

        # bind click on book list → show details
        self.list_books.bind("<<ListboxSelect>>", self.bookInfo)

        # ── Tab 2 – statistics labels ────────────────────────────
        self.lbl_book_count = Label(self.tab2, text="",
                                    pady=20, font="verdana 14 bold")
        self.lbl_book_count.grid(row=0, sticky=W)

        self.lbl_member_count = Label(self.tab2, text="",
                                      pady=20, font="verdana 14 bold")
        self.lbl_member_count.grid(row=1, sticky=W)

        self.lbl_taken_count = Label(self.tab2, text="",
                                     pady=20, font="verdana 14 bold")
        self.lbl_taken_count.grid(row=2, sticky=W)

        # bind tab change → refresh statistics
        self.tabs.bind("<<NotebookTabChanged>>", self.displayStatistics)

        # ── initial data load ────────────────────────────────────
        self.displayBooks()
        self.displayStatistics()

    # ── methods ──────────────────────────────────────────────────

    def displayBooks(self):
        books = cur.execute("SELECT * FROM books").fetchall()
        self.list_books.delete(0, END)
        for count, book in enumerate(books):
            self.list_books.insert(count, str(book[0]) + " - " + book[1])

    def bookInfo(self, evt):
        if not self.list_books.curselection():
            return
        value = self.list_books.get(self.list_books.curselection())
        book_id = value.split(" - ")[0]
        book_info = cur.execute(
            "SELECT * FROM books WHERE book_id=?", (book_id,)
        ).fetchall()

        if not book_info:
            return

        self.list_details.delete(0, END)
        self.list_details.insert(END, "Book Name : " + book_info[0][1])
        self.list_details.insert(END, "Author    : " + book_info[0][2])
        self.list_details.insert(END, "Pages     : " + str(book_info[0][3]))
        self.list_details.insert(END, "Language  : " + book_info[0][4])
        status = "Available" if book_info[0][5] == 0 else "Not Available"
        self.list_details.insert(END, "Status    : " + status)

    def displayStatistics(self, evt=None):
        count_books   = cur.execute("SELECT count(book_id) FROM books").fetchone()[0]
        count_members = cur.execute("SELECT count(member_id) FROM members").fetchone()[0]
        taken_books   = cur.execute(
            "SELECT count(book_status) FROM books WHERE book_status=1"
        ).fetchone()[0]

        self.lbl_book_count.config(
            text="Total : " + str(count_books) + " books in library")
        self.lbl_member_count.config(
            text="Total members : " + str(count_members))
        self.lbl_taken_count.config(
            text="Taken books : " + str(taken_books))

    def addBook(self):
        addbook.AddBook()

    def addMember(self):
        addmember.AddMember()

    def giveBook(self):               
        lendbook.LendBook()

    def searchBooks(self):
        value = self.ent_search.get()
        search = cur.execute(
            "SELECT * FROM books WHERE book_name LIKE ?",
            ('%' + value + '%',)
        ).fetchall()
        self.list_books.delete(0, END)
        for count, book in enumerate(search):
            self.list_books.insert(count, str(book[0]) + " - " + book[1])

    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            rows = cur.execute("SELECT * FROM books").fetchall()
        elif value == 2:
            rows = cur.execute(
                "SELECT * FROM books WHERE book_status=?", (0,)).fetchall()
        else:
            rows = cur.execute(
                "SELECT * FROM books WHERE book_status=?", (1,)).fetchall()

        self.list_books.delete(0, END)
        for count, book in enumerate(rows):
            self.list_books.insert(count, str(book[0]) + " - " + book[1])


def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1350x750+350+200")
    root.iconbitmap("icons/icon.ico")
    root.mainloop()


if __name__ == "__main__":
    main()