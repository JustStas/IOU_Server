import datetime
from core import server_conn


class Trx:
    def __init__(self,
                 creditor_id,
                 trx_id=-1,
                 trx_name='Empty name',
                 currency='RUB',
                 full_amount=100.00,
                 date=datetime.datetime.now()):
        if trx_id == -1:
            self.trx_id = server_conn('allocate_trx_id')
        else:
            self.trx_id = trx_id
        self.trx_name = trx_name
        self.creditor_id = creditor_id
        self.debtors_id = None
        self.currency = currency
        self.full_amount = full_amount
        self.date = date

    def save(self):
        server_conn('update_trx', {'trx_id': self.trx_id, 'trx_name': self.trx_name, 'creditor_id': self.creditor_id,
                                   'debtors_id': self.debtors_id, 'currency': self.currency, 'amount': self.full_amount,
                                   'date': self.date})

    def load(self):
        details = server_conn('check_trx', self.trx_id)
        if details is not None:
            self.trx_name = details['trx_name']
            self.creditor_id = details['creditor_id']
            self.debtors_id = details['debtors_id']
            self.currency = details['currency']
            self.amount = details['amount']
            self.date = details['date']

        else:
            print('No transaction found with this ID')

    def describe(self):
        print('Transaction ID:', self.trx_id)
        print('Creditor ID:', self.creditor_id)
        print('Debtors:', self.debtors_id)
        print('Volume:', self.full_amount, self.currency)

    def equal_split(self, debtors=-1):
        if debtors == -1:
            print('Debtors None')
            self.debtors_id = [self.creditor_id]
        else:
            self.debtors_id = debtors
        share = self.full_amount / len(self.debtors_id)
        for debtor in self.debtors_id:
            i_iou = IOU(trx_id=self.trx_id,
                        creditor_id=self.creditor_id,
                        debtor_id=debtor,
                        currency=self.currency,
                        iou_amount=share,
                        date=self.date)
            i_iou.save()


class IOU:
    def __init__(self,
                 trx_id=0,
                 creditor_id=0,
                 debtor_id=1,
                 currency='RUB',
                 iou_amount=100.00,
                 date=datetime.datetime.now()):
        self.trx_id = trx_id
        self.creditor_id = creditor_id
        self.debtor_id = debtor_id
        self.currency = currency
        self.iou_amount = iou_amount
        self.date = date

        self.iou_id = server_conn('allocate_iou_id')

    def save(self):
        server_conn('update_iou', {'trx_id': self.trx_id, 'IOU_id': self.iou_id, 'creditor_id': self.creditor_id,
                                   'debtor_id': self.debtor_id, 'currency': self.currency, 'amount': self.iou_amount,
                                   'date': self.date})


class User:
    def __init__(self,
                 user_id=-1,
                 f_name=None,
                 l_name=None):
        self.user_id = user_id
        self.f_name = f_name
        self.l_name = l_name

    def load(self):
        credentials = server_conn('check_user', self.user_id)
        if credentials is not None:
            self.f_name = credentials['f_name']
            self.l_name = credentials['l_name']
        else:
            y_n = None
            while y_n not in ['y', 'Y', 'n', 'N']:
                y_n = input('No such user found. Create new user? (y/n) ')
            if y_n in ['n', 'N']:
                print('Leaving without user creation.')

            if y_n in ['y', 'Y']:
                self.user_id = max(server_conn('list_users')) + 1
                self.f_name = input('Enter user first name: ')
                self.l_name = input('Enter user last name: ')
                self.write()

    def write(self):
        user = {'user_id': self.user_id, 'f_name': self.f_name, 'l_name': self.l_name}
        self.user_id = server_conn('write_user', user)

    def balance(self,
                counterpart_id=-1):  # todo currently I/O happens on every balance query - maybe, create attribute with all possible balances in case of slow I/O
        if counterpart_id == -1:
            user_pair = {'debtor_id': self.user_id, 'creditor_id': None}
            debt = server_conn('amount_check', user_pair)
            user_pair = {'debtor_id': None, 'creditor_id': self.user_id}
            receivables = server_conn('amount_check', user_pair)
        else:
            user_pair = {'debtor_id': self.user_id, 'creditor_id': counterpart_id}
            debt = server_conn('amount_check', user_pair)
            user_pair = {'debtor_id': counterpart_id, 'creditor_id': self.user_id}
            receivables = server_conn('amount_check', user_pair)
        return [debt, receivables]

    def describe(self, short=True):
        if short:
            print('First name:', self.f_name)
        else:
            print('ID:', self.user_id)
            print('First name:', self.f_name)
            print('Last name:', self.l_name)
