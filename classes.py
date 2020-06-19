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
        self.save()

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
            self.full_amount = details['amount']
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
        self.save()


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
        print('allocating')
        self.iou_id = server_conn('allocate_iou_id')
        print('allocated')

    def save(self):
        server_conn('update_iou', {'trx_id': self.trx_id, 'IOU_id': self.iou_id, 'creditor_id': self.creditor_id,
                                   'debtor_id': self.debtor_id, 'currency': self.currency, 'amount': self.iou_amount,
                                   'date': self.date})


class User:
    def __init__(self,
                 user_id=-1,
                 f_name=None,
                 l_name=None,
                 username='',
                 telegram_id=-1):
        self.user_id = user_id
        self.f_name = f_name
        self.l_name = l_name
        self.username = username
        self.telegram_id = telegram_id
        self.description = self.describe(short=False)

    def load(self):
        credentials = server_conn('check_user', self.username)
        if credentials is not None:
            self.user_id = credentials['user_id']
            self.f_name = credentials['f_name']
            self.l_name = credentials['l_name']
            self.telegram_id = credentials['telegram_id']
        else:
            self.create_new_user()

        self.description = self.describe(short=False)

    def allocate_user_id(self):
        self.user_id = max(server_conn('list_users', True))['user_id'] + 1

    def create_new_user(self):
        y_n = None
        while y_n not in ['y', 'Y', 'n', 'N']:
            y_n = input('No such user found. Create new user? (y/n) ')
        if y_n in ['n', 'N']:
            print('Leaving without user creation.')

        if y_n in ['y', 'Y']:
            self.user_id = max(server_conn('list_users')) + 1
            good_username = False
            while not good_username:
                test_username = input('Enter username: ')
                if len(test_username) < 4:
                    print('Username should be at least 4 symbols long')
                elif server_conn('check_username_availability', test_username):
                    good_username = True
                    self.username = test_username

            self.f_name = input('Enter user first name: ')
            self.l_name = input('Enter user last name: ')
            self.write()


    def write(self):
        user = {'user_id': self.user_id,
                'f_name': self.f_name,
                'l_name': self.l_name,
                'username': self.username,
                'telegram_id': self.telegram_id}
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
        to_print = ''
        if short:
            to_print += ('\nFirst name: ' + str(self.f_name))
        else:
            to_print += ('\nID: ' + str(self.user_id))
            to_print += ('\nFirst name: ' + str(self.f_name))
            to_print += ('\nLast name: ' + str(self.l_name))
            to_print += ('\nUsername: ' + str(self.username))
            to_print += ('\nTelegram_ID: ' + str(self.telegram_id))

        print(to_print)
        return to_print
