import pandas as pd
from paths import trx_log_path, iou_log_path, users_db_path
from admin_functions import reset_databases


def server_conn(command, data=None):
    data_source = [command, data]
    data_output = None
    try:
        data_output = process_data(data_source)
    except Exception:
        print(Exception)

    return data_output


def process_data(input):
    output = None
    command = input[0]
    print('Command: ', command)
    data = input[1]
    if command == 'list_users':
        output = list_users()
    if command == 'save_users':
        save_users(data)
    if command == 'list_ious':
        output = list_ious()
    if command == 'list_trx':
        output = list_trx()
    if command == 'save_trx':
        save_trx(data)
    if command == 'allocate_iou_id':
        output = allocate_iou_id()
    if command == 'allocate_trx_id':
        output = allocate_trx_id()
    if command == 'update_iou':
        update_iou(data)
    if command == 'update_trx':
        update_trx(data)
    if command == 'amount_check':
        output = amount_check(data)
    if command == 'check_user':
        output = check_user(data)
    if command == 'write_user':
        output = write_user(data)
    if command == 'check_trx':
        output = check_trx(data)
    if command == 'check_username_availability':
        output = check_username_availability(data)

    if command == 'reset_databases':
        reset_databases()

    return output


def list_users(full_info=False):
    users = pd.read_hdf(users_db_path, key='df')
    if not full_info:
        print(users.head())
        users = users['username']
    return users


def save_users(users):
    users.to_hdf(users_db_path, key='df')


def list_ious():
    ious = pd.read_hdf(iou_log_path, key='df')

    return ious


def list_trx():
    transactions = pd.read_hdf(trx_log_path, key='df')

    return transactions


def save_trx(trx_list):
    trx_list.to_hdf(trx_log_path, key='df')


def allocate_iou_id():
    ious = list_ious()
    new_iou_id = ious['IOU_id'].max() + 1
    row = pd.Series({'trx_id': None, 'IOU_id': new_iou_id, 'creditor_id': None, 'debtor_id': None,
                     'currency': None, 'amount': None, 'date': None})
    ious = ious.append(row, ignore_index=True)
    save_iou(ious)

    return new_iou_id


def allocate_trx_id():
    transactions = list_trx()
    new_trx_id = transactions['trx_id'].max() + 1
    row = pd.Series({'trx_id': new_trx_id, 'trx_name': None, 'creditor_id': None, 'debtors_id': None,
                     'currency': None, 'amount': None, 'date': None})
    transactions = transactions.append(row, ignore_index=True)
    save_trx(transactions)

    return new_trx_id


def update_iou(iou_dict):
    ious = list_ious()
    row = pd.Series(iou_dict)
    ious = ious.loc[ious['IOU_id'] != iou_dict['IOU_id']].append(row, ignore_index=True)
    save_iou(ious)


def update_trx(trx_dict):
    transactions = list_trx()
    row = pd.Series(trx_dict)
    transactions = transactions.loc[transactions['trx_id'] != trx_dict['trx_id']].append(row, ignore_index=True)
    save_trx(transactions)


def amount_check(user_pair):
    debtor_id = user_pair['debtor_id']
    creditor_id = user_pair['creditor_id']
    log = list_ious()
    if debtor_id is not None:
        log = log.loc[log['debtor_id'] == debtor_id]
    if creditor_id is not None:
        log = log.loc[log['creditor_id'] == creditor_id]
    log = log.loc[log['creditor_id'] != log['debtor_id']]
    return round(log['amount'].sum(), 2)


def check_user(username):
    users = list_users(full_info=True)
    try:
        user_line = users.loc[users['username'] == username].iloc[0]
        f_name = user_line['f_name']
        l_name = user_line['l_name']
        user_credentials = {'f_name': f_name, 'l_name': l_name}
    except IndexError:
        user_credentials = None
    return user_credentials


def write_user(user):
    user_id = user['user_id']
    f_name = user['f_name']
    l_name = user['l_name']
    users = list_users(full_info=True)
    if user_id != -1:
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


def check_trx(trx_id):
    trx_list = list_trx()
    try:
        trx_details = trx_list.loc[trx_list['trx_id'] == trx_id].iloc[0]
    except IndexError:
        trx_details = None
    return trx_details


def save_iou(iou_list):
    iou_list.to_hdf(iou_log_path, key='df')


def check_username_availability(test_username):
    if test_username in list_users():
        return False
    else:
        return True
