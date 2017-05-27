from decimal import Decimal
import account
import database
from datetime import date, time, datetime


def main_menu():
    print("\nPersonal Finance Management")
    print("1. Show Accounts Summary")
    print("2. Add money to Cash Account")
    print("3. Create Bank Account")
    print("4. Delete Bank Account")
    print("5. Deposit to Bank Account")
    print("6. Withdraw from Bank Account")
    print("7. Transfer between Bank Account")
    print("8. Payment with Credit Bank Account")
    print("9. Payment with Cash Account")
    print("10. Check Balance")
    print("11. Check Log")
    print("12. Reset Program")
    print("13. Exit Program")
    ans = 0
    flag_exit = False
    while not (ans in range(1,14)):
        flag_exit = False
        ans = input("\tPlease choose (1-13) : ").strip()
        if not(ans.isdigit()):
            ans = 0
        elif eval(ans) <= 0 or eval(ans) > 13:
            ans = 0
        else:
            ans = eval(ans)
            options = {1: menu_list_account,
                       2: menu_add_money_to_cash_account,
                       3: menu_create_bank_account,
                       4: menu_delete_bank_account,
                       5: menu_deposit_to_bank_account,
                       6: menu_withdraw_from_bank_account,
                       7: menu_transfer_between_bank_account,
                       8: menu_payment_with_credit_bank_account,
                       9: menu_payment_with_cash_account,
                       10: menu_check_balance,
                       11: menu_check_log,
                       12: menu_reset_program,
                       13: menu_exit_program
                       }
            if ans == 13:
                flag_exit = options[ans]()
            else:
                options[ans]()
    return flag_exit

def menu_deposit_to_bank_account():
    print("\n\n")
    cash_acc = read_account_info('Cash')
    print("----- Deposit Money to Bank Account -----")
    print("Please choose item number for deposit")
    acc_no_list = show_list_account('Bank')
    flag_cancel = False
    ans1 = ""
    ans2 = ""
    if len(acc_no_list) == 0:
        print("\tNo avaliable account.")
        flag_cancel = True
    else:
        if len(acc_no_list) == 1:
            ans1 = input("\tChoose (only 1 or other for cancel) : ")
        else:
            ans1 = input("\tChoose ({}-{} or other for cancel ) : ".format(1, len(acc_no_list)))
        if ans1.isdigit():
            ans1 = eval(ans1) - 1
            if ans1 in range(len(acc_no_list)):
                ans2 = input("\tCash to deposit amount : ")
                try:
                    ans2 = Decimal(ans2)
                except ValueError:
                    print("\tInvalid value cash amount.")
                    flag_cancel = True
                if ans2 > cash_acc.acc_balance:
                    print("\tNot enough cash to deposit (you have cash only {:,.2f})".format(cash_acc.acc_balance))
                    flag_cancel = True
            else:
                flag_cancel = True
        else:
            flag_cancel = True
    if not flag_cancel:
        acc_no = acc_no_list[ans1][0]
        my_acc = read_account_info(acc_no)
        result1 = my_acc.deposit(ans2)
        result2 = cash_acc.withdraw(ans2)
        if result1 and result2:
            db = database.Database()
            db.update_account_balance(acc_no,my_acc.acc_balance)
            db.update_account_balance('Cash',cash_acc.acc_balance)
            db.insert_transaction_log(datetime.now(),'Deposit',ans2,'Cash',acc_no,cash_acc.acc_balance,my_acc.acc_balance)
            print("\t... Transaction successful ...")
        else:
            print("\tError deposit, transaction cancel")
    else:
        print("\tCancel Deposit")


def menu_withdraw_from_bank_account():
    print("\n\n")
    print("----- Withdraw Money From Bank Account -----")
    print("Please choose item number for withdraw")
    acc_no_list = show_list_account('Bank')
    flag_cancel = False
    ans1 = ""
    ans2 = ""
    if len(acc_no_list) == 0:
        print("\tNo avaliable account.")
        flag_cancel = True
    else:
        if len(acc_no_list) == 1:
            ans1 = input("\tChoose (only 1 or other for cancel) : ")
        else:
            ans1 = input("\tChoose ({}-{} or other for cancel ) : ".format(1, len(acc_no_list)))
        if ans1.isdigit():
            ans1 = eval(ans1) - 1
            if ans1 in range(len(acc_no_list)):
                ans2 = input("\tPlease enter withdraw amount : ")
                try:
                    ans2 = Decimal(ans2)
                except ValueError:
                    print("\tInvalid amount value.")
                    flag_cancel = True
            else:
                flag_cancel = True
        else:
            flag_cancel = True
    if not flag_cancel:
        acc_no = acc_no_list[ans1][0]
        saving_acc = read_account_info(acc_no)
        ans = saving_acc.withdraw(ans2)
        if ans:
            db = database.Database()
            db.update_account_balance(acc_no, saving_acc.acc_balance)
            print("\t... Transaction successful ...")
        else:
            print("\tNot enough money or credit, transaction cancel")
    else:
        print("\tCancel Withdraw")


def menu_transfer_between_bank_account():
    print("\n\n")
    print("----- Transfer Money Between Bank Account -----")
    print("Please choose item number for transfer")
    acc_no_list = show_list_account('Bank')
    flag_cancel = False
    ans1 = ""
    ans2 = ""
    ans3 = ""
    if len(acc_no_list) == 0:
        print("\tNo avaliable account.")
        flag_cancel = True
    elif len(acc_no_list) == 1:
        print("\tOnly one account can't transfer")
        flag_cancel = True
    else:
        ans1 = input("\tTransfer from account item ({}-{} or other for cancel ) : ".format(1, len(acc_no_list)))
        ans2 = input("\tTo account item ({}-{} or other for cancel ) : ".format(1, len(acc_no_list)))
        if ans1.isdigit() and ans2.isdigit():
            ans1 = eval(ans1) - 1
            ans2 = eval(ans2) - 1
            if ans1 in range(len(acc_no_list)) and ans2 in range(len(acc_no_list)):
                if ans1 != ans2 :
                    ans3 = input("\tCash amount for transfer : ")
                    try:
                        ans3 = Decimal(ans3)
                    except ValueError:
                        print("\tInvalid value cash amount.")
                        flag_cancel = True
                else:
                    print("\n\tCan't transfer to same account")
                    flag_cancel = True
            else:
                flag_cancel = True
        else:
            flag_cancel = True
    if not flag_cancel:
        acc_no1 = acc_no_list[ans1][0]
        acc_no2 = acc_no_list[ans2][0]
        acc_from = read_account_info(acc_no1)
        acc_to = read_account_info(acc_no2)
        result1 = acc_from.transfer_from(ans3)
        result2 = acc_to.transfer_to(ans3)
        if result1 and result2:
            db = database.Database()
            db.update_account_balance(acc_no1, acc_from.acc_balance)
            db.update_account_balance(acc_no2,acc_to.acc_balance)
            print("\t... Transaction successful ...")
        else:
            print("\tNot enough money or credit, transaction cancel")
    else:
        print("\tCancel Transfer")


def menu_payment_with_credit_bank_account():
    print("\n\n")
    print("----- Make Payment with your Credit Account -----")
    print("Please choose account item number for the payment")
    acc_no_list = show_list_account('Credit')
    flag_cancel = False
    ans1 = ""
    ans2 = ""
    if len(acc_no_list) == 0:
        print("\tNo avaliable account.")
        flag_cancel = True
    else:
        if len(acc_no_list) == 1:
            ans1 = input("\tChoose (only 1 or other for cancel) : ")
        else:
            ans1 = input("\tChoose ({}-{} or other for cancel ) : ".format(1, len(acc_no_list)))
        if ans1.isdigit():
            ans1 = eval(ans1) - 1
            if ans1 in range(len(acc_no_list)):
                ans2 = input("\tPayment amount : ")
                try:
                    ans2 = Decimal(ans2)
                except ValueError:
                    print("\tInvalid amount value.")
                    flag_cancel = True
            else:
                flag_cancel = True
        else:
            flag_cancel = True
    if not flag_cancel:
        acc_no = acc_no_list[ans1][0]
        saving_acc = read_account_info(acc_no)
        ans = saving_acc.payment_by_credit(ans2)
        if ans:
            db = database.Database()
            db.update_account_balance(acc_no, saving_acc.acc_balance)
            print("\t... Transaction successful ...")
        else:
            print("Not enough money or credit, transaction cancel")
    else:
        print("\tCancel Payment")


def menu_payment_with_cash_account():
    flag_cancel = False
    print("\n\n")
    print("----- Make Payment with Cash -----")
    ans = input("\tPayment amount : ")
    try:
        ans = Decimal(ans)
    except ValueError:
        print("\tInvalid amount value.")
        flag_cancel = True
    if not flag_cancel:
        cash_acc = read_account_info('Cash')
        ans = cash_acc.withdraw(ans)
        if ans:
            db = database.Database()
            db.update_account_balance('Cash', cash_acc.acc_balance)
            print("\t... Transaction successful ...")
        else:
            print("\tNot enough cash, transaction cancel")
    else:
        print("\tCancel Payment")


def menu_add_money_to_cash_account():
    flag_cancel = False
    print("\n\n")
    print("----- Add Money to Cash Account -----")
    ans = input("\tCash amount : ")
    try:
        ans = Decimal(ans)
    except ValueError:
        print("\tInvalid value cash amount.")
        flag_cancel = True
    if not flag_cancel:
        my_acc = read_account_info('Cash')
        ans = my_acc.deposit(ans)
        if ans:
            db = database.Database()
            db.update_account_balance('Cash', my_acc.acc_balance)
            print("\t... Transaction successful ...")
        else:
            print("\tError add money, transaction cancel")
    else:
        print("\tCancel add money to cash")


def menu_check_balance():
    pass

def menu_check_log():
    db = database.Database()
    results = db.db_read_all_transaction('All')
    print()
    print("{:10s}\t\t{:10s}\t{:10s}\t{:10s}\t{:10s}\t{:10s}\t{:10s}\t{:10s}".format('Transaction ID', 'Date Time', 'Action', 'Amount', 'From Account', 'From Balance', 'To Account', 'To Balance'))
    #trans_id, trans_datetime, trans_action, trans_amount, from_acc, to_acc, from_acc_balance, to_acc_balance
    print('-' * 105)
    for res in results:
        trans_id = res[0]
        trans_datetime = res[1]
        trans_action = res[2]
        trans_amount = res[3]
        from_acc = res[4]
        to_acc = res[5]
        from_acc_balance = res[6]
        to_acc_balance = res[7]
        print("{:d}\t\t{}\t{:>10s}\t{:10,.2f}\t{:10s}\t{:10,.2f}\t{:10s}\t{:10,.2f}".format(trans_id, trans_datetime, trans_action, trans_amount, from_acc, from_acc_balance, to_acc, to_acc_balance))


def menu_exit_program():
    print("\n\n")
    print("----- Exit Program -----")
    ans = input("\tDo you want to exit program? (y/n) : ").lower()
    if ans in ['y','yes']:
        return True
    else:
        return False

def menu_reset_program():
    print("\n\n")
    print("----- Reset Program -----")
    print("Reset program will erease all your data.")
    ans = input("\tPlease type 'confirm' to confirm reset otherwise cancel : ").lower()
    if ans == 'confirm':
        db = database.Database()
        db.db_drop_tables()
        print("\t... Program reset successful ...")
    else:
        print("\tCancel reset program")

def read_account_info(acc_no):
    db = database.Database()
    res = db.db_read_one_account(acc_no)
    #acc_id = res[0]
    #acc_provider = res[1]
    #acc_no = res[2]
    #acc_name = res[3]
    acc_type = res[4]
    #acc_create_datetime = res[5]
    #acc_status = res[6]
    acc_credit = res[7]
    acc_balance = res[8]
    if acc_type == 'Saving':
        acc1 = account.Saving_Account()
        acc1.acc_no = acc_no
        acc1.acc_balance = acc_balance
    elif acc_type == 'Credit':
        acc1 = account.Credit_Account()
        acc1.acc_no = acc_no
        acc1.acc_balance = acc_balance
        acc1.acc_credit = acc_credit
    elif acc_type == 'Income':
        acc1 = account.Income_Account()
        acc1.acc_no = acc_no
        acc1.acc_balance = acc_balance
    elif acc_type == 'Cash':
        acc1 = account.Cash_Account()
        acc1.acc_no = acc_no
        acc1.acc_balance = acc_balance
    elif acc_type == 'Shop':
        acc1 = account.Shop_Account()
        acc1.acc_no = acc_no
        acc1.acc_balance = acc_balance
    else:
        acc1 = account.Account()
    return acc1

def show_list_account(acc_type):
    db = database.Database()
    results = db.db_read_all_account(acc_type)
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
        print("{}. Account: {:15} Name: {:15} Type: {:10} Bank: {:10} Credit: {:<10,.2f} Balance: {:10,.2f}".format(num,acc_no,acc_name,acc_type,acc_provider,acc_credit,acc_balance))
    return acc_no_list

def menu_list_account():
    db = database.Database()
    results = db.db_read_all_account('All')
    print()
    print("{:15s} {:15s} {:20s} {:15s} {:>15s} {:>15s}".format('Bank Name', 'Account Type', 'Account Number',
                                                             'Account Name','Credit Limit', 'Balance'))
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
        print("{:15s} {:15s} {:20s} {:15s} {:15,.2f} {:15,.2f}".format(acc_provider,acc_type,acc_no,acc_name,acc_credit,acc_balance))


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
    print("\nConfirm Create Account")
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


def menu_delete_bank_account():
    print("\n\n")
    print("----- Delete Bank Account -----")
    print("Please choose item number to delete")
    acc_no_list = show_list_account('Bank')
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
                acc_no = acc_no_list[ans][0]
                db = database.Database()
                db.delete_account(str(acc_no))
            else:
                print("\tCancel Delete")
        else:
            print("\tCancel Delete")

def print_enter_to_continue():
    input("\nPress Enter to continue...")



if __name__ == '__main__':

    status = database.db_check_connection()
    if status:
        db = database.Database()
        db.init_database()
        flag_exit = False
        while not flag_exit:
            flag_exit = main_menu()
            if not flag_exit:
                print_enter_to_continue()
    else:
        print("Database connection error.\nPlease check mySQL database is running.")


    #menu_create_bank_account()