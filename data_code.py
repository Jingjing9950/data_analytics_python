import unicodecsv
import datetime as dt

enrollments_filename = 'enrollments.csv'
engagement_filename = 'daily_engagement.csv'
submissions_filename = 'project_submissions.csv'

def readfile(file):
    with open(file, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        enrollments = list(reader)
    return enrollments

def parse_date(date):
    if date == '':
        return None
    else:
        return dt.datetime.strptime(date,'%Y-%m-%d')

def parse_bool(bool):
    if bool == '':
        return None
    else:
        return True

def parse_int(i):
    if i == '':
        return None
    else:
        return int(i)


enrollments = readfile(enrollments_filename)
daily_engagement = readfile(engagement_filename)  # Replace this with your code
project_submissions = readfile(submissions_filename)  # Replace this with your code

for enrollment in enrollments:
    enrollment['days_to_cancel'] = parse_int(enrollment['days_to_cancel'])
    enrollment['is_udacity'] = parse_bool(enrollment['is_udacity'])
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    enrollment['is_canceled'] = parse_bool(enrollment['is_canceled'])

    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])


def unique_number(file):
    unique_num = []
    for enrollment in file:
        unique_num.append(enrollment['account_key'])
    unique_num = set(unique_num)
    return unique_num

enrollment_unique_data = unique_number(enrollments)
engagement_unique_data = unique_number(daily_engagement)

# for enrollment1 in enrollments:
#     student = enrollment1['account_key']
#     days_to_cancel = enrollment1['days_to_cancel']
#     if student not in engagement_unique_data and days_to_cancel != 0:
#         print(enrollment1)

paid_student = {}
number_is_udacity = []
for enrollment1 in enrollments:
    daystocancel = enrollment1['days_to_cancel']
    is_udacity = enrollment1['is_udacity']

    if daystocancel == None or daystocancel > 7 :
        account_key = enrollment1['account_key']
        paid_student[account_key] = enrollment1['join_date']

print(len(paid_student))
print(len(number_is_udacity))


