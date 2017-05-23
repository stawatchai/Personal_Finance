from decimal import Decimal
import account
import database


def main_menu():
    print("\nPersonal Finance Management")
    print("1. Create Bank Account")
    print("2. Delete Bank Account")
    print("3. Deposit to Bank Account")
    print("4. Withdraw from Bank Account")
    print("5. Transfer between Bank Account")
    print("6. Payment with Credit Bank Account")
    print("7. Payment with Cash Account")
    print("8. Add money to Cash Account")
    print("9. Check Balance")
    print("10. Exit Program")
    print("11. Reset Program")
    print("12. List Account")
    ans = 0
    while not (ans in range(1,13)):
        ans = input("\tPlease choose (1-12) : ").strip()
        if not(ans.isdigit()):
            ans = 0
        elif eval(ans) <= 0 or eval(ans) > 12:
            ans = 0
        else:
            ans = eval(ans)
            options = {1: menu_create_bank_account,
                       2: menu_delete_bank_account,
                       3: menu_deposit_to_bank_account,
                       4: menu_withdraw_from_bank_account,
                       5: menu_transfer_between_bank_account,
                       6: menu_payment_with_credit_bank_account,
                       7: menu_payment_with_cash_account,
                       8: menu_add_money_to_cash_account,
                       9: menu_check_balance,
                       10: menu_exit_program,
                       11: menu_reset_program,
                       12: menu_list_account
                       }
            options[ans]()


def menu_delete_bank_account():
    print("\n\n")
    print("----- Delete Bank Account -----")
    print("Please choose item number to delete")
    acc_no_list = show_list_account()
    if len(acc_no_list)==0:
        print("\tNo avaliable account for delete")
    else:
        if len(acc_no_list)==1:
            ans = input("\tChoose (only 1 or other for cancel) : ")
        else:
            ans = input("\tChoose ({}-{} or other for cancel ) : ".format(1,len(acc_no_list)))
        if ans.isdigit():
            ans = eval(ans) - 1
            if ans in range(len(acc_no_list)):
                acc_no = acc_no_list[ans]
                db = database.Database()
                db.delete_account(str(acc_no))
            else:
                print("\tCancel Delete")
        else:
            print("\tCancel Delete")

def menu_deposit_to_bank_account():
    print("\n\n")
    print("----- Deposit Money to Bank Account -----")
    print("Please choose item number for deposit")
    acc_no_list = show_list_account()
    if len(acc_no_list) == 0:
        print("\tNo avaliable account.")
    else:
        if len(acc_no_list) == 1:
            ans = input("\tChoose (only 1 or other for cancel) : ")
        else:
            ans = input("\tChoose ({}-{} or other for cancel ) : ".format(1, len(acc_no_list)))
        if ans.isdigit():
            ans = eval(ans) - 1
            if ans in range(len(acc_no_list)):
                acc_no = acc_no_list[ans]
                db = database.Database()
                db.update_account_amount_credit(acc_no,100)
            else:
                print("\tCancel Deposit")
        else:
            print("\tCancel Delete")


def menu_withdraw_from_bank_account():
    pass


def menu_transfer_between_bank_account():
    pass


def menu_payment_with_credit_bank_account():
    pass


def menu_payment_with_cash_account():
    pass


def menu_add_money_to_cash_account():
    pass


def menu_check_balance():
    pass


def menu_exit_program():
    pass


def menu_reset_program():
    print("\n\n")
    print("----- Reset Program -----")
    print("Reset program will erease all your data.")
    ans = input("\tPlease type 'confirm' to confirm reset otherwise cancel : ").lower()
    if ans == 'confirm':
        db = database.Database()
        db.db_drop_tables()
        print("Program reset successful")
    else:
        print("Cancel reset program")

def read_account_info():
    db = database.Database()
    results = db.db_list_all_account('Saving')
    #read Saving account
    saving = account.saving_account()
    savings = []
    for res in results:
        saving.acc_id = res[0]
        saving.acc_provider = res[1]
        saving.acc_no = res[2]
        saving.acc_name = res[3]
        saving.acc_type = res[4]
        saving.acc_create_datetime = res[5]
        saving.acc_status = res[6]
        saving.acc_credit = res[7]
        saving.acc_balance = res[8]
        savings.append(saving)


def show_list_account():
    db = database.Database()
    results = db.db_list_all_account('All')
    num = 0
    acc_no_list=[]
    for res in results:
        num += 1
        acc_id = res[0]
        acc_provider = res[1]
        acc_no = res[2]
        acc_name = res[3]
        acc_type = res[4]
        acc_create_datetime = res[5]
        acc_status = res[6]
        acc_credit = res[7]
        acc_balance = res[8]
        data = [acc_no,acc_balance,acc_credit]
        acc_no_list.append(data)
        print("{}. Account: {:15} Name: {:15} Type: {:10} Bank: {:10} Balance: {:,.2f}".format(num,acc_no,acc_name,acc_type,acc_provider,acc_balance))
    return acc_no_list

def menu_list_account():
    db = database.Database()
    results = db.db_list_all_account('All')
    print()
    print("{:15s} {:15s} {:20s} {:20s} {:>15s} {:>15s}".format('Bank Name', 'Account Type', 'Account Number',
                                                             'Account Name', 'Balance', 'Credit Limmit'))
    print('-'*105)

    for res in results:
        acc_id = res[0]
        acc_provider = res[1]
        acc_no = res[2]
        acc_name = res[3]
        acc_type = res[4]
        acc_create_datetime = res[5]
        acc_status = res[6]
        acc_credit = res[7]
        acc_balance = res[8]
        print("{:15s} {:15s} {:20s} {:20s} {:15,.2f} {:15,.2f}".format(acc_provider,acc_type,acc_no,acc_name,acc_balance,acc_credit))

def menu_create_bank_account():
    print("\n\n")
    print("----- Create Bank Account -----")
    print("Please input account information.")
    print("1. Bank Name of the account")
    acc_bank = ''
    while acc_bank == '':
        acc_bank = input("\tEnter Bank name : ")
    print("2. Bank Account type (s for Saving account, c for Credit account)")
    acc_type = ''
    while not (acc_type in ['s','c']):
        acc_type = input("\tEnter type (s or c): ").strip().lower()
    print("3. Bank Account Number")
    acc_no = ''
    acc_credit = '0'
    while not acc_no.isdigit():
        acc_no = input("\tEnter Account number (only numeric) : ")
        acc_no = acc_no.lower()
    print("4. Bank Account Name")
    acc_name = ''
    while acc_name == '':
        acc_name = input("\tEnter Account name : ")
    if acc_type == 'c':
        print("5. For credit bank account only")
        while Decimal(acc_credit) <= 0:
            try:
                acc_credit = Decimal(input("\tEnter credit limit (Positive decimal) : "))
            except:
                acc_credit = '0'
    print("Confirm Create Account Summary")
    print("\tBank Name : {}".format(acc_bank))
    dic_type = {"s":"Saving Account","c":"Credit Account"}
    print("\tAccount Type : {}".format(dic_type[acc_type]))
    print("\tAccount Number : {}".format(acc_no))
    print("\tAccount Name : {}".format(acc_name))
    if acc_type == 'c':
        print("\tCredit Limit : {:,.2f}".format(acc_credit))
    ans = ''
    while not (ans in ['y','n']):
        ans = input("\tConfirm create (y or n) : ").lower()

    if ans == 'y':
        db = database.Database()
        if acc_type == 'c':
            db.db_insert_current_account(acc_bank, acc_no, acc_name, acc_credit)
        else:
            db.db_insert_saving_account(acc_bank, acc_no, acc_name)


if __name__ == '__main__':

    status = database.db_check_connection()
    if status:
        db = database.Database()
        db.init_database()
        main_menu()
    else:
        print("Database connection error")


    #menu_create_bank_account()