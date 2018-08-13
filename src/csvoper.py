import csv
import os
import copy

FIELD_NAME = ['image_name', 'pool_name', 'snapshot_period', \
                    'retain_period', 'retain_count', 'last_snapshot']

class CSVOper(object):
    @classmethod
    def create(cls, file_name = '../image_info.csv'):
        if os.path.exists(file_name):
            os.remove(file_name)
        os.mknod(file_name)
        with open(file_name, 'a') as f: 
            w_csv = csv.DictWriter(f, fieldnames = FIELD_NAME)
            w_csv.writeheader()
        return True

    @classmethod
    def read(cls, file_name = '../image_info.csv'):
        with open(file_name, 'r') as f:
            res = []
            r_csv = csv.DictReader(f)
            for row in r_csv:
                res.append(dict(row))
            return res

    @classmethod
    def writerow(cls, entry, file_name = '../image_info.csv'):
        write_success = True
        with open(file_name, 'r') as rf:
            r_csv = csv.DictReader(rf)
            for row in r_csv:
                if entry['image_name'] == row['image_name'] and \
                        entry['pool_name'] == row['pool_name']:
                            write_success = False
                            break
        if write_success:
            with open(file_name, 'a') as wf:
                w_csv = csv.writer(wf)
                w_csv.writerow([entry['image_name'], entry['pool_name'], \
                        entry['snapshot_period'], entry['retain_period'], \
                        entry['retain_count'], entry['last_snapshot']])

        return write_success

    @classmethod
    def updaterow(cls, entry, file_name = '../image_info.csv'):
        op_list = []
        updated = False
        with open(file_name, 'r') as rf:
            r_csv = csv.DictReader(rf)
            for row in r_csv:
                op_list.append(dict(row))

        for ele in op_list:
            if ele['image_name'] == entry['image_name'] and \
                    ele['pool_name'] == entry['pool_name']:
                        ele['snapshot_period'] = entry['snapshot_period']
                        ele['retain_period'] = entry['retain_period']
                        ele['retain_count'] = entry['retain_count']
                        if entry['last_snapshot'] != '-':
                            ele['last_snapshot'] = entry['last_snapshot']
                        updated = True

        if updated:
            with open(file_name, 'w') as wf:
                w_csv = csv.DictWriter(wf, fieldnames = FIELD_NAME)
                w_csv.writeheader()
                w_csv.writerows(op_list)

        return updated

    @classmethod
    def deleterow(cls, entry, file_name = '../image_info.csv'):
        op_list = []
        deleted = False
        with open(file_name, 'r') as rf:
            r_csv = csv.DictReader(rf)
            for row in r_csv:
                op_list.append(dict(row))

        for ele in op_list:
            if ele['image_name'] == entry['image_name'] and \
                    ele['pool_name'] == entry['pool_name']:
                op_list.remove(ele)
                deleted = True

        if deleted:
            with open(file_name, 'w') as wf:
                w_csv = csv.DictWriter(wf, fieldnames = FIELD_NAME)
                w_csv.writeheader()
                w_csv.writerows(op_list)

        return deleted
