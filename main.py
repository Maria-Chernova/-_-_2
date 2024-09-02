
import csv
import re
from pprint import pprint
from collections import defaultdict

def parse_name(name_parts):
    full_name = " ".join(name_parts[:3]).split()
    if len(full_name) == 3:
        return full_name[0], full_name[1], full_name[2]
    elif len(full_name) == 2:
        return full_name[0], full_name[1], ''
    else:
        return full_name[0], '', ''

def format_phone_number(phone):
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(?:.*доб\.*\s*(\d+))?"
    match = re.match(pattern, phone)
    if match:
        formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(6):
            formatted_phone += f" доб.{match.group(6)}"
        return formatted_phone
    return phone

def process_contacts(contacts):
    merged_contacts = defaultdict(lambda: ['', '', '', '', '', '', ''])

    for contact in contacts:
        lastname, firstname, surname = parse_name(contact[:3])
        organization = contact[3]
        position = contact[4]
        phone = format_phone_number(contact[5])
        email = contact[6]

        key = (lastname, firstname)

        if not merged_contacts[key][0]:
            merged_contacts[key][0] = lastname
        if not merged_contacts[key][1]:
            merged_contacts[key][1] = firstname
        if not merged_contacts[key][2]:
            merged_contacts[key][2] = surname
        if not merged_contacts[key][3]:
            merged_contacts[key][3] = organization
        if not merged_contacts[key][4]:
            merged_contacts[key][4] = position
        if not merged_contacts[key][5]:
            merged_contacts[key][5] = phone
        if not merged_contacts[key][6]:
            merged_contacts[key][6] = email

    return list(merged_contacts.values())

# Чтение CSV
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Обработка контактов
header = contacts_list[0]
contacts = contacts_list[1:]
processed_contacts = process_contacts(contacts)

# Запись обработанных данных в новый CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(header)
    datawriter.writerows(processed_contacts)

# Вывод обработанных данных
pprint([header] + processed_contacts)
