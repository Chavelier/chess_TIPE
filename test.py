from tkinter import *



class BankManager(object):

    root = Tk()

    lblName = Label(root, text="Name")
    lblPin = Label(root, text="Pin")
    lblBalance = Label(root, text="Balance R")
    lblStatus = Label(root, text="Status")

    tbName = Entry(root)
    tbPin = Entry(root)
    tbBalance = Entry(root)
    tbStatus = Entry(root)

    def __init__(self):
        self.bank = None
        self.app = None
        self.current_index = 0
        self.create_bank()
        self.populate_gui(self.current_index)

    def new_account(self, event):
        name = self.app.getEntry('name')
        pin = self.app.getEntry('pin')
        balance = self.app.getEntry('balance')
        account = self.bank.get(pin)
        if account:
            self.app.setEntry("status", "Account with pin exists")
        else:
            self.bank.add(SavingsAccount(name, pin, float(balance)))
            self.app.setEntry("status", "New account created")
            self.current_index = self.bank.getPins().index(pin)

    btnNewAcc = Button(root,text="New Account")
    btnNewAcc.bind("<Button>",new_account)

    def update_account(self, event):
        name = self.app.getEntry('name')
        pin = self.app.getEntry('pin')
        balance = self.app.getEntry('balance')
        account = self.bank.get(pin)
        if account:
            account._name = name
            account._balance = balance
            self.app.setEntry("status", "Account updated")
        else:
            self.app.setEntry("status", "Account with pin doesn't exist")

    btnUpdateAcc = Button(root, text="Update Account")
    btnUpdateAcc.bind("<Button>",update_account)

    def remove_account(self, event):
        pin = self.app.getEntry('pin')
        account = self.bank.get(pin)
        if account:
            self.bank.remove(pin)
            self.app.setEntry("status", "Account removed")
            self.current_index = 0
        else:
            self.app.setEntry("status", "Account with pin doesn't exist")

    btnRemoveAcc = Button(root,text="Remove Account")
    btnRemoveAcc.bind("<Button>",remove_account)

    def compute_interest(self, event):
        self.bank.computeInterest()
        pin = self.app.getEntry('pin')
        account = self.bank.get(pin)
        if account:
            self.app.setEntry("status", "Interest updated")
            self.app.setEntry("balance", str(account.getBalance()))
        else:
            self.app.setEntry("status", "Account with pin doesn't exist")

    btnConputeInterest = Button(root,text="Compute Interest")
    btnConputeInterest.bind("<Button>",compute_interest)

    def press_navigator(self, event):
        if button == "Previous":
            if self.current_index == 0:
                self.current_index = len(self.bank.getPins()) - 1
            else:
                self.current_index -= 1
        elif button == "Next":
            if self.current_index == len(self.bank.getPins()) - 1:
                self.current_index = 0
            else:
                self.current_index += 1
        self.populate_gui(self.current_index)

    btnPrevious = Button(root,text="Previous")
    btnPrevious.bind("<Button>",press_navigator)

    btnNext = Button(root,text="Next")
    btnNext.bind("<Button>",press_navigator)

    lblName.grid(row=0)
    lblPin.grid(row=1)
    lblBalance.grid(row=2)
    lblStatus.grid(row=3)

    tbName.grid(row=0, column=1)
    tbPin.grid(row=1, column=1)
    tbBalance.grid(row=2, column=1)
    tbStatus.grid(row=3, column=1)

    btnNewAcc.grid(row=0, column=2)
    btnUpdateAcc.grid(row=1, column=2)
    btnRemoveAcc.grid(row=2, column=2)
    btnConputeInterest.grid(row=3, column=2)
    btnPrevious.grid(row=4, column=0)
    btnNext.grid(row=4, column=1)

    root.mainloop()

    def create_bank(self):
        self.bank = Bank()
        a1 = SavingsAccount('zzz', '111', 100)
        a2 = SavingsAccount('yyy', '222', 200)
        a3 = SavingsAccount('xxx', '333', 300)
        self.bank.add(a1)
        self.bank.add(a3)
        self.bank.add(a2)

    def populate_gui(self, index):
        account = self.bank.get(self.bank.getPins()[index])
        tbName.set("tbName", account.getName())
