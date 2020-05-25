from tkinter import ttk
from tkinter import * 

import sqlite3

class Product: 

    dbName = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')

        #Creating a Frame Container
        frame = LabelFrame(self.wind, text = 'Register a new Product')
        frame.grid(row = 0, column  = 0, columnspan = 3, pady = 20)

        #Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Price Input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Output Messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Table 
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)
        
        #Button Add Product
        ttk.Button(frame, text = "Save Product", command = self.AddProduct).grid(row = 3, columnspan = 2, sticky = W + E)

        #Button Delete Product
        ttk.Button(text = 'DELETE', command = self.DeleteProduct).grid(row = 5, column = 0, sticky = W + E)
        
        #Button Edit Product
        ttk.Button(text = 'EDIT', command = self.EditProduct).grid(row = 5, column = 1, sticky = W + E)

        #Filling the Rows
        self.GetProducts()

    
    def RunQuery(self, query, parameters = ()):
        #Interact with DB
        with sqlite3.connect(self.dbName) as conn: 
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def Validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

###########################################################################################################################################
###############################################################---CRUD---##################################################################
###########################################################################################################################################

    def GetProducts(self): 
        #Cleaning Table
    
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        #Querying Data

        query = 'SELECT * FROM product ORDER BY name DESC'
        dbRows = self.RunQuery(query)
        for row in dbRows:
            self.tree.insert('', 0, text = row[1], value = row[2])

    def AddProduct(self):   
        if self.Validation(): 
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.RunQuery(query, parameters)
            self.message['text'] = 'Product {} added Succesfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else: 
            self.message['text'] = 'Name or Price Required'
        self.GetProducts()

    def DeleteProduct(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            print(e)
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.RunQuery(query, (name, ))
        self.message['text'] = 'Record {} deleted Succesfully'.format(name)
        self.GetProducts()

    def EditProduct(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            print(e)
            return
        name = self.tree.item(self.tree.selection())['text']
        oldPrice = self.tree.item(self.tree.selection())['values'][0]
        self.editWind = Toplevel()
        self.editWind.title = 'Edit Product'

        #Old Name
        Label(self.editWind, text = 'Old Name: ').grid(row = 0, column = 1)
        Entry(self.editWind, textvariable = StringVar(self.editWind, value = name), state = 'readonly').grid(row = 0, column = 2)

        #New Name
        Label(self.editWind, text = 'New Name: ').grid(row = 1, column = 1)
        newName = Entry(self.editWind)
        newName.grid(row = 1, column = 2)

        #Old Price
        Label(self.editWind, text = 'Old Price: ').grid(row = 2, column = 1)
        Entry(self.editWind, textvariable= StringVar(self.editWind, value = oldPrice), state = 'readonly').grid(row = 2, column = 2)

        #New Price
        Label(self.editWind, text = 'New Price: ').grid(row = 3, column = 1)
        newPrice = Entry(self.editWind)
        newPrice.grid(row = 3, column = 2)

        #Update Button
        Button(self.editWind, text = 'Update', command = lambda: self.EditRecords(newName.get(), name, newPrice.get(), oldPrice)).grid(row = 4, column = 2, sticky = W)

    def EditRecords(self, newName, name, newPrice, oldPrice): 
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?' 
        parameters = (newName, newPrice, name, oldPrice)
        self.RunQuery(query, parameters)
        self.editWind.destroy()
        self.message['text'] = 'Record {} updated Successfully'.format(name)
        self.GetProducts()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()  