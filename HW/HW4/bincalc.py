import tkinter as tk
from hw4 import Binary

class Data:
    ''' The model. '''
    def __init__(self):
        self.bins = [Binary(), Binary(), Binary()]

class Calculator(tk.Frame):
    ''' The view. '''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.grid()  # the grid geometry manager

        tk.Label(self, text='Binary 1: ').grid(row=3, column=0)
        tk.Label(self, text='Binary 2: ').grid(row=7, column=0)
        tk.Label(self, text='Result:   ').grid(row=9, column=0)
        tk.Label(self, text='Type number,').grid(row=1, column=1)
        tk.Label(self, text='then hit enter:').grid(row=2, column=1)
        self.blank_rows([0, 1, 2, 4, 5, 6, 8, 10])
        self.binflds = [self.make_entry(3), self.make_entry(7), self.make_entry(9)]
        self.active_flds = [False, False, False]
        self.decs = [self.make_button(3, 3, "Decimal"), self.make_button(7, 3, "Decimal"), self.make_button(9, 3, "Decimal")]
        self.bins = [self.make_button(3, 5, "Binary"), self.make_button(7, 5, "Binary"), self.make_button(9, 5, "Binary")]
        self.negs = [self.make_button(3, 7, "Neg"), self.make_button(7, 7, "Neg"), self.make_button(9, 7, "Neg")]
        self.abss = [self.make_button(3, 9, "Abs"), self.make_button(7, 9, "Abs"), self.make_button(9, 9, "Abs")]
        self.make_op_buttons()
        tk.Button(self, text="QUIT", fg="red", command=root.destroy).grid(row=11, column=1)
        tk.Label(self, text='          ').grid(row=12, column=0)
        tk.Label(self, text=' ').grid(row=5, column=16)
        tk.Label(self, text='-'*23).grid(row=8, column=1)
        
    def blank_rows(self, rows):
        for i in rows:
            tk.Label(self, text='          ').grid(row=i, column=0)
        
    def make_entry(self, row_num):
        txtfield = tk.Entry(self, width=17, justify='right')
        txtfield.grid(row=row_num, column=1)
        txtfield.insert('end', "0")
        return txtfield
    
    def make_button(self, row_num, col, txt):
        tk.Label(self, text=' ').grid(row=row_num, column=col - 1)
        btn = tk.Button(self, text=txt)
        btn.grid(row=row_num, column=col)
        return btn
        
    def make_op_buttons(self):
        self.plus = self.make_button(5, 1, "        +        ")
        self.minus = self.make_button(5, 3, "   -   ")
        self.eq = self.make_button(5, 5, "  ==  ")
        self.ne = self.make_button(5, 7, "!= ")
        self.lt = self.make_button(5, 9, " < ")
        self.gt = self.make_button(5, 11, ">")
        self.le = self.make_button(5, 13, "<=")
        self.ge = self.make_button(5, 15, ">=")
        
class Controller:
    def __init__(self, root):
        self.data = Data() # the model
        self.calculator = Calculator(root) # the view
        for i in range(len(self.calculator.binflds)):
            # Must use this format - event gets passed to lambda no matter what.
            self.calculator.binflds[i].bind('<Button-1>', lambda event, arg=i: self.activate_fld(event, arg))
            self.calculator.binflds[i].bind('<Return>', lambda event, arg=i: self.binfld(event, arg))
            self.calculator.decs[i].config(command=lambda arg=i: self.dec(arg))
            self.calculator.bins[i].config(command=lambda arg=i: self.save_and_restore(arg))
            self.calculator.negs[i].config(command=lambda arg=i: self.neg(arg))
            self.calculator.abss[i].config(command=lambda arg=i: self.abs(arg))
        self.calculator.plus.config(command=lambda: self.plus_minus(self.data.bins[0] + self.data.bins[1]))
        self.calculator.minus.config(command=lambda: self.plus_minus(self.data.bins[0] - self.data.bins[1]))
        self.calculator.eq.config(command=lambda: self.logical(self.data.bins[0] == self.data.bins[1]))
        self.calculator.ne.config(command=lambda: self.logical(self.data.bins[0] != self.data.bins[1]))
        self.calculator.lt.config(command=lambda: self.logical(self.data.bins[0] < self.data.bins[1]))
        self.calculator.gt.config(command=lambda: self.logical(self.data.bins[0] > self.data.bins[1]))
        self.calculator.le.config(command=lambda: self.logical(self.data.bins[0] <= self.data.bins[1]))
        self.calculator.ge.config(command=lambda: self.logical(self.data.bins[0] >= self.data.bins[1]))
    
    def activate_fld(self, event, index):
        # Activate the relevant field.
        if not self.calculator.active_flds[index]:
            self.calculator.binflds[index].delete(0, "end")
            self.calculator.binflds[index].focus()
            self.calculator.active_flds[index] = True
            
        # Restore the other fields if necessary.
        for i in range(3):
            if self.calculator.active_flds[i] and i != index:
                self.calculator.binflds[i].delete(0, "end")
                self.calculator.binflds[i].insert('end', repr(self.data.bins[i]))
                self.calculator.active_flds[i] = False
            
    def restore_flds(self, index):
        '''
        This method maintains the view so that the user
        knows the current state of the machine.  Partially 
        completed but abandoned changes are erased.  Changes
        are not saved until return is pressed.
        '''
        self.calculator.active_flds[index] = False
        for i in range(3):
            if self.calculator.active_flds[i]:
                self.calculator.binflds[i].delete(0, "end")
                self.calculator.binflds[i].insert('end', repr(self.data.bins[i]))
                self.calculator.active_flds[i] = False
    
    def save_and_restore(self, index):
        '''
        '''
        self.calculator.active_flds[index] = True
        for i in range(3):
            if self.calculator.active_flds[i]:
                self.calculator.binflds[i].delete(0, "end")
                self.calculator.binflds[i].insert('end', repr(self.data.bins[i]))
                self.calculator.active_flds[i] = False
    
    def binfld(self, event, index):
        txt = self.calculator.binflds[index].get()
        self.data.bins[index] = Binary(txt)
        self.calculator.binflds[index].delete(0, "end")
        self.calculator.binflds[index].insert('end', repr(self.data.bins[index]))
        self.restore_flds(index)
    
    def dec(self, index):
        self.calculator.binflds[index].delete(0, "end")
        self.calculator.binflds[index].insert('end', int(self.data.bins[index]))
        self.restore_flds(index)

    def neg(self, index):
        self.data.bins[index] = -self.data.bins[index]  # update the model
        self.save_and_restore(index)                    # update the view
        
    def abs(self, index):
        self.data.bins[index] = abs(self.data.bins[index])
        self.save_and_restore(index)
        
    def plus_minus(self, result):
        self.data.bins[2] = result
        self.save_and_restore(2)
        
    def logical(self, result):
        #result = 'True' if self.data.bins[0] <logical op> self.data.bins[1] else 'False'
        self.calculator.binflds[2].delete(0, "end")
        self.calculator.binflds[2].insert('end', repr(result))
        self.restore_flds(2)
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Binary Calculator")
    Controller(root)
    root.mainloop()
