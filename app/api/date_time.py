'''
Created on 20171208

@author: zhou
'''

'''
generate date list
'''


import datetime

def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result

if __name__ == "__main__":
    print datelist((2017, 1, 1), (2017, 11, 30))
