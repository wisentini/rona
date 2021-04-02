from bs4 import BeautifulSoup
import requests
import os

file_path = os.path.join(os.path.expanduser('~'), 'rona', 'data.txt')
file_exists = os.path.isfile(file_path)

def read_values_from_file():
    file = open(file_path, 'r')
    old_values = file.read().splitlines()
    file.close()

    old_values = [int(x) for x in old_values]
    return old_values

def write_values_to_file():
    f = open(file_path, 'w')

    for value in values:
        f.write('%d\r\n' % value)

    f.close()

def get_data():
    url = 'https://silveiramartins.rs.gov.br/coronavirus/boletim-epidemiologico'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    data = soup.find('div', class_='row no-margin')

    return data

def parse_data():
    titles = data.find_all('b', class_='title')
    titles = [title.text.strip() for title in titles]

    values = data.find_all('font', class_='Numbers')
    values = [int(value.text) for value in values]

    return (titles, values)

def get_updates():
    updates = []

    for i in range(len(values)):
        if values[i] > old_values[i]:
            data = '+{}' .format(values[i] - old_values[i])
        elif values[i] < old_values[i]:
            data = '{}' .format(values[i] - old_values[i])
        else:
            data = ''

        updates.append(data)

    return updates

def print_data():
    emoji = ['\U0001F914', '\U0001F622', '\U0001F64C', '\U0001F440', '\U0001F973', '\U0001F635', '\U0001F40A']

    print('\n%12s %14s %15s\n' % ('SITUAÇÃO', 'NÚMEROS', 'ATUALIZAÇÃO'))

    for i in range(len(titles)):
        print('%-2s %-14s %6d %13s' % (emoji[i], titles[i], values[i], updates[i]))

    print()

old_values = read_values_from_file()
data = get_data()
(titles, values) = parse_data()

if file_exists:
    updates = get_updates()

print_data()
write_values_to_file()