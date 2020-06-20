import pandas as pd
from paths import trx_log_path, iou_log_path, users_db_path, groups_db_path
import datetime


def reset_databases():
    trx_log = pd.DataFrame(columns=['trx_id', 'trx_name', 'creditor_id', 'debtors_id', 'currency', 'amount', 'date'],
                           data=[[0, 'Dummy transaction', 0, [0], 'RUB', 0.00, datetime.datetime.now()]])
    iou_log = pd.DataFrame(columns=['trx_id', 'IOU_id', 'creditor_id', 'debtor_id', 'currency', 'amount', 'date'],
                           data=[[0, 0, 0, 0, 'RUB', 0.00, datetime.datetime.now()]])
    users_db = pd.DataFrame(columns=['user_id', 'f_name', 'l_name', 'username', 'telegram_id'],
                            data=[[0, 'Stanislav', 'Nosulenko', 'JustStas', -1],
                                  [1, 'Oleg', 'Cock', 'Sereas', -1],
                                  [2, 'Andrey', 'Artyushin', 'BigBelly', -1]])
    groups_db = pd.DataFrame(columns=['group_id', 'group_name', 'member_ids'],
                             data=[[0, 'Shtab', [0, 1, 2]],
                                   [0, 'NotShtab', [0, 1]]])

    trx_log.to_hdf(trx_log_path, key='df')
    iou_log.to_hdf(iou_log_path, key='df')
    users_db.to_hdf(users_db_path, key='df')
    groups_db.to_hdf(groups_db_path, key='df')
