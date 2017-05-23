def demo_tuple():
    p12 = "Joe","Gomez",12
    print(p12)
    print(p12[1])

def demo_dict():
    p12 = {"fname":"Joe","lname":"Gemez","number":12}
    print(p12)
    print(p12["lname"])


class Player:
    pass


def demo_sample_player_class():
    p12 = Player()
    p12.fname = "Joe"
    p12.lname = "Gomez"
    print(p12.lname)


class Person:
    def __init__(self):
        self.fname = ""
        self.lname = ""
        self.country = "Thailand"


class Person2:
    def __init__(self,fname,lname,country):
        self.fname = fname
        self.lname = lname
        self.country = country

class Person3:
    def __init__(self,fname=None,lname=None,country="Thailand"):
        self.fname = fname
        self.lname = lname
        self.country = country

    def __str__(self):
        return "fname: {} lname:{} country:{}".format(self.fname,self.lname,self.country)

class Account():
    def __init__(
            self,acc_id,acc_provider,acc_no,acc_name,acc_type,
            acc_create_datetime,acc_status,acc_credit,acc_balance):
        #acc_id - Running Number
        #acc_provider - Bank, Finace or Cash Pocket
        #acc_no - Account Number (for Bank Reference)
        #acc_name - Account Owner
        #acc_type - Account Type (Cash,Saving,Current,Credit)
        #acc_create_date - Date of Account Created
        #acc_status - Account Status (Active, Disable, Closed)
        #acc_balance - Balance of this account

        self.acc_id = acc_id
        self.acc_provider = acc_provider
        self.acc_no = acc_no
        self.acc_name = acc_name
        self.acc_type = acc_type
        self.acc_create_datetime = acc_create_datetime
        self.acc_status = acc_status
        self.acc_credit = acc_credit
        self.acc_balance = acc_balance

class acc(Account):
    def __init__(self,acc_id, acc_provider, acc_no, acc_name, acc_type, acc_create_datetime, acc_status,
                 acc_credit, acc_balance):
        super().__init__(acc_id, acc_provider, acc_no, acc_name, acc_type, acc_create_datetime, acc_status, acc_credit,
                         acc_balance)




if __name__ == '__main__':
    # demo_tuple()
    # demo_dict()
    # demo_sample_player_class()
    # p1 = Person()
    # print(p1.fname)
    # print(p1.lname)
    # print(p1.country)
    P3 = Person3("Alek","Sriruji","USA")
    print(P3)

