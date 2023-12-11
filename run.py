import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """Get sales figures input from the user
    added a while loop so if incorrect data is added 
    the user does not need to run the program again, it automatically
    re-runs until the data is valid, using the return True or False values"""
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, seperated by commas.')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input("Enter your data here:")
   
        sales_data =data_str.split(',')
        #spilts the inputted data at the , and adds to a list
    
        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data
        


def validate_data(values):
    """Inside the try, converts all string values in integers.
    Raises a valueError if strings cannot be converted into int,
    or if there aren't excatly 6 values.
    """
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True


#def update_sales_worksheet(data): refactored below
    """update sales worksheet, 
    add new row with the list data provded
    """
    print("updating sales worksheet...\n")

    sales_worksheet = SHEET.worksheet("sales") 
    #.worksheet() is a built in method to access the work sheets 
    sales_worksheet.append_row(data)
    #.append_row() is a built in method to add the data to a new row inthe worksheet.
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """Compare sales with stock and calculate 
    the surplus for each item type.
    
    The surplus is defined as the sales figures subtraced from the stock:
    -positive surplus indicates waste
    -negative surplus indicates extra made to meet demand
    """

    print('Calculating surplus data...\n')
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1] # requests the last line in the list - slice method
    
    surplus_data =[]
    for stock, sales in zip(stock_row, sales_row): # iterating over two lists at the same time
        surplus = int(stock) - sales #converting stock into int 
        surplus_data.append(surplus) #adding to empty list above

    return surplus_data
          

#def update_surplus_worksheet(info): refactored below
    """update surplus worksheet, 
    add new row with the list data provded
    """
    print("updating surplus worksheet...\n")

    surplus_worksheet = SHEET.worksheet("surplus") 
    #.worksheet() is a built in method to access the work sheets 
    surplus_worksheet.append_row(info)
    #.append_row() is a built in method to add the data to a new row inthe worksheet.
    print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """Received a list of integers to be inserted into a worksheet 
    updates the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """

    sales = SHEET.worksheet('sales')
    
    columns =[]
    for ind in range(1, 7):
        column = sales.col_values(ind) #col_values is a built in method from gspread.
    #this returns the column data, accessing the 3rd column in the spreadsheet
    #counting the column index starts from 1 not 0.
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculates the average stock for each item type, adding 10%
    """

    print('Calculating stock data...\n')

    new_stock_data =[]
    for column in data:
        int_column =[int(num) for num in column]
        average = sum(int_column) / len(int_column) #using the len() gives functionality
        #if we don't know how long the list is.

        stock_num = average *1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data



def main():
    """moved all function calls into it's own function
    to tidy up the code space
    """
    data = get_sales_data()#returned data from user input
    sales_data = [int(num) for num in data] # convert returned data into int
    update_worksheet(sales_data, 'sales') #add int data to worksheet
    new_surplus_data = calculate_surplus_data(sales_data) 
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')

print('Welcome to Love Sandwiches Data\n')
main()
