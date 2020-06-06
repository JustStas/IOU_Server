import pandas as pd
from paths import trx_log_path, users_db_path


def process_data(input):
    output = None
    command = input[0]
    print('Command: ', command)
    data = input[1]
    if command == 'list_users':
        output = list_users()
    if command == 'list_trx':
        output = list_trx()
    if command == 'save_trx':
        save_trx(data)
    if command == 'save_users':
        save_users(data)
    if command == 'update_iou':
        update_iou(data)
    if command == 'amount_check':
        output = amount_check(data)
    if command == 'write_user':
        write_user(data)
    if command == 'check_user':
        output = check_user(data)
    if command == 'allocate_iou_id':
        output = allocate_iou_id()

    return output


def list_users(full_info=False):
    users = pd.read_hdf(users_db_path, key='df')
    if not full_info:
        users = users['user_id']
    return users


def save_users(users):
    users.to_hdf(users_db_path, key='df')



def list_trx():
    transactions = pd.read_hdf(trx_log_path, key='df')

    return transactions


def save_trx(trx_list):
    trx_list.to_hdf(trx_log_path, key='df')



def allocate_iou_id():
    transactions = list_trx()
    new_iou_id = transactions['IOU_id'].max() + 1
    row = pd.Series({'trx_id': new_iou_id, 'IOU_id': None, 'creditor_id': None, 'debtor_id': None,
                     'currency': None, 'amount': None, 'date': None})
    transactions = transactions.append(row, ignore_index=True)
    save_trx(transactions)

    return new_iou_id


def update_iou(iou_dict):
    transactions = list_trx()
    row = pd.Series(iou_dict)
    transactions = transactions.loc[transactions['IOU_id'] != iou_dict['IOU_id']].append(row, ignore_index=True)
    save_trx(transactions)


def amount_check(user_pair):
    debtor_id = user_pair['debtor_id']
    creditor_id = user_pair['creditor_id']
    log = list_trx()
    if debtor_id is not None:
        log = log.loc[log['debtor_id'] == debtor_id]
    if creditor_id is not None:
        log = log.loc[log['creditor_id'] == creditor_id]
    log = log.loc[log['creditor_id'] != log['debtor_id']]
    return round(log['amount'].sum(), 2)

def check_user(user_id):
    user_credentials = None
    users = list_users(full_info=True)
    user_line = users.loc[users['user_id'] == user_id].iloc[0]
    if user_line.shape[0] > 0:
        f_name = user_line['f_name']
        l_name = user_line['l_name']
        user_credentials = {'f_name': f_name, 'l_name': l_name}
    return user_credentials


def write_user(user):
    user_id = user['user_id']
    f_name = user['f_name']
    l_name = user['l_name']
    users = list_users(full_info=True)
    if user_id is not None:
        if user_id in users['user_id']:
            users.loc[users['user_id'] == user_id] = {'user_id': user_id, 'f_name': f_name, 'l_name': l_name}
        else:
            row = pd.Series({'user_id': user_id, 'f_name': f_name, 'l_name': l_name})
            users = users.append(row, ignore_index=True)
    else:
        user_id = users['user_id'].max() + 1
        row = pd.Series({'user_id': user_id, 'f_name': f_name, 'l_name': l_name})
        users = users.append(row, ignore_index=True)

    save_users(users)

    return user_id

