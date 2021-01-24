from qaPersistence import *

import sys
import os
import random

repo = Repository()


def add_vaccines(splittedline):
    repo.Vaccine.insert(Vaccine(*splittedline))


def add_supplier(splittedline):
    repo.Supplier.insert(Supplier(*splittedline))


def add_clinics(splittedline):
    repo.Clinic.insert(Clinic(*splittedline))


def add_logistics(splittedline):
    repo.Logistic.insert(Logistic(*splittedline))


def outr(outline):
    # inventory
    inv = 0
    s = repo.Vaccine.find_all()
    for line in s:
        inv += line.quantity
    # demand
    dem = 0
    s = repo.Clinic.find_all()
    for line in s:
        dem += line.demand
    # received
    re = 0
    s = repo.Logistic.find_all()
    for line in s:
        re += line.count_received
    # sent
    se = 0
    s = repo.Logistic.find_all()
    for line in s:
        se += line.count_sent

    ans = "{},{},{},{}".format(inv, dem, re, se)
    # print(ans)
    return ans


def recieve(name, amount, date):
    s = repo.Supplier.find(**{"name": name})  # s is a list of Supplier
    supp, logi_id = s[0].id, s[0].logistic
    # id = random.randint(0,10000)
    # id = repo.Vaccine.find_all()[-1].id + 1
    # add_vaccines([str(id), date, str(supp), amount])
    vac = repo.Vaccine.find_all()
    if len(vac) == 0:
        add_vaccines([1, s[0].id, date, amount])
    else:
        id = vac[-1].id + 1
        add_vaccines([str(id), s[0].id, date, amount])
    logis = repo.Logistic.find(**{'id': logi_id})
    repo.Logistic.delete(**{'id': logi_id})

    for logi in logis:
        logi.count_received += int(amount)
        repo.Logistic.insert(logi)


def send(location, amount):
    # 1
    s = repo.Clinic.find(**{"location": location})
    clic = repo.Clinic.find(**{'location': location})
    repo.Clinic.delete(**{'location': location})

    for cl in clic:
        cl.demand -= int(amount)
        repo.Clinic.insert(cl)

    # 2
    logi_id = s[0].logistic
    logis = repo.Logistic.find(**{'id': logi_id})
    repo.Logistic.delete(**{'id': logi_id})

    for logi in logis:
        logi.count_sent += int(amount)
        repo.Logistic.insert(logi)

    # 3
    amou = int(amount)
    v = repo.Vaccine.find_all()
    for v1 in v:
        if amou == 0:
            break
        else:
            repo.Vaccine.delete(**{'id': v1.id})
            if v1.quantity > amou:
                v1.quantity = v1.quantity - amou
                repo.Vaccine.insert(v1)
                amou = 0
            else:
                k = v1.quantity
                v1.quantity = 0
                amou = amou - k


def main(args):
    inputfilename = args[1]
    repo.create_tables()
    v = 0
    c = 0
    l = 0
    s = 0
    k = 0
    arr = []
    with open(inputfilename) as inputfile:
        i = 0
        for line in inputfile:
            lst = line.strip().split(",")
            if i == 0:
                v = int(lst[0])
                s = int(lst[1])
                c = int(lst[2])
                l = int(lst[3])
            if 0 < i < v + 1:
                arr.append(Vaccine(*lst))
            if v < i < s + v + 1:
                add_supplier(lst)
            if v + s < i < s + v + c + 1:
                add_clinics(lst)
            if v + s + c < i < s + v + c + l + 1:
                add_logistics(lst)
            k = k + 1
            i = i + 1
        arr = sorted(arr, key=lambda k: int(k.date.replace("-", "").replace("_", "")))
        for g in arr:
            repo.Vaccine.insert(g)

  
    output = ""
    with open(args[2], 'r') as order:
        for line in order.readlines():
            lst = line.strip().split(',')
            if len(lst) == 3:
                recieve(*lst)
                output += outr(output)
                output += "\n"

            else:
                send(*lst)
                output += outr(output)
                output += "\n"

    f = open(args[3], "w+")
    f.write(output)


if __name__ == '__main__':
    main(sys.argv)
