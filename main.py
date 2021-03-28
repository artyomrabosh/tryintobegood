import openpyxl
import datetime
import config

groups = config.groups
channels = config.channels


def init():
    book = openpyxl.load_workbook(filename='timetable.xlsx')
    sheet = book['Table 1']
    return sheet


def make_timetable(sheet):
    times = []
    for v in sheet[3]:
        if v.value is None:
            times.append(None)
        else:
            times.append(v.value)
    for i in range(len(times)):
        if i > 2 and times[i] is None:
            times[i] = times[i - 1]
    day = 1
    table = [None, None, [9, 1]]
    for i in range(len(times))[3:-2]:
        if int(times[i][:-3]) < int(times[i - 1][:-3]):
            day += 1
        table.append([int(times[i][:-3]), day])
    return table


def user_input(group):
    return {
        'group': group,
        'day': (datetime.datetime.utcnow()+datetime.timedelta(hours=3)).weekday()+1,
        'time': int('{}'.format(datetime.datetime.utcnow() + datetime.timedelta(hours=3))[11:-13])
    }


def distant(lesson):
    answer = ''
    if lesson.find('Канал') != -1:
        number = int(lesson[lesson.find('№') + 1])
        answer = 'Канал: {} '.format(channels[number - 1])
    return answer


def answer_weekend(answer, user):
    i = 2
    line = groups[user['group']]
    answer.append('weekend')
    answer.append('next lesson: ')
    while sheet[line][i].value is None:
        i = i + 1
    answer.append(sheet[line][i].value)
    answer.append(sheet[3][i].value)
    answer.append(distant(sheet[line][i].value))
    return answer


def answer_evening(answer, user, i):
    line = groups[user['group']]
    while table[i][1] == user['day'] or sheet[groups[user['group']]][i].value is None:
        i += 1
    answer.append('no more lessons today')
    answer.append('next lesson tomorrow:')
    answer.append(sheet[groups[user['group']]][i].value)
    answer.append(sheet[3][i].value)
    answer.append(distant(sheet[line][i].value))
    return answer


def answer_day(answer, user, i):
    line = groups[user['group']]
    answer.append(sheet[groups[user['group']]][i].value)
    answer.append(sheet[3][i].value)
    answer.append(distant(sheet[line][i].value))
    while sheet[groups[user['group']]][i + 1].value is None:
        i = i + 1
    if table[i][1] > user['day']:
        answer.append('next lesson tomorrow:')
    else:
        answer.append('next lesson:')
    answer.append(sheet[groups[user['group']]][i + 1].value)
    answer.append(sheet[3][i + 1].value)
    answer.append(distant(sheet[line][i].value))
    return answer


def main(group):
    user = user_input(group)
    answer = []
    if user['time'] > 18 and user['day'] == 6 or user['day'] == 7:
        answer = answer_weekend(answer, user)
    for i in range(2, len(table)):
        if table[i][1] == user['day']:
            if table[i][0] >= user['time']:
                answer = answer_day(answer, user, i)
                break
            if user['time'] > 18:
                answer = answer_evening(answer, user, i)
                break
    if answer == []:
        answer.append('no more lessons today')
    return answer


sheet = init()
table = make_timetable(sheet)
