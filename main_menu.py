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
    ans = 0
    while not (ans in range(1,10)):
        ans = input("\tPlease choose (1-7) : ").strip()
        if not(ans.isdigit()):
            ans = 0
        elif eval(ans) <= 0 or eval(ans) > 10:
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
                       }
            options[ans]()


def menu_delete_bank_account():
    pass


def menu_deposit_to_bank_account():
    pass


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


def menu_create_bank_account():
    print("\nPlease input account information.")
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
    if acc_type == 'c':
        print("4. For credit bank account only")
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
    if acc_type == 'c':
        print("\tCredit Limit : {:,.2f}".format(acc_credit))
    ans = ''
    while not (ans in ['y','n']):
        ans = input("\tConfirm create (y or n) : ").lower()
    if ans == 'y':
        pass


if __name__ == '__main__':
    db = database.Database()
    db.init_database()

    main_menu()
    #menu_create_bank_account()