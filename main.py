import random


def customer_document(file):
    with open(file) as file_input:
        table = {}
        for i in file_input:

            if i.split(" ")[0] not in table:
                table[i.split(" ")[0]] = [i.split(" ")[1], i.split(" ")[2]]
            else:
                table[(i.split(" ")[0]) + "+"] = [i.split(" ")[1], i.split(" ")[2]]

    return table


def gas_document(file):
    with open(file) as file_azs:
        info = {}
        for i in file_azs:

            info[i.split(" ")[0]] = [i.split(" ")[0], i.split(" ")[1], i.split(" ")[2:], ""]

    return info


def time():
    times = []
    for hour in range(0, 24):
        if len(str(hour)) < 2:
            h = str("0" + str(hour))
        else:
            h = str(hour)
        for minutes in range(0, 60):
            if len((str(minutes))) < 2:
                s = str("0" + str(minutes))
            else:
                s = str(minutes)
            now = h + ":" + s
            times.append(now)
    return times


def presentation_station(data):
    print("Автомат №" + data["1"][0] + "." + " Максимальная очередь: " + data["1"][1] + ". " + " Марки бензина: " +
          str(data["1"][2][0]) + " ->" + data["1"][3])

    print("Автомат №" + data["2"][0] + "." + " Максимальная очередь: " + data["2"][1] + ". " + " Марки бензина: " +
          str(data["2"][2][0]) + " ->" + data["2"][3])

    print("Автомат №" + data["3"][0] + "." + " Максимальная очередь: " + data["3"][1] + ". " + " Марки бензина: " +
          " ".join(data["3"][2]) + " ->" + data["3"][3])
    print("")


def refueling_time(data, times):
    minutes = [-1, 0, 1]
    onStation = int(data[times][0]) // 10 + random.choice(minutes)
    if onStation <= 0:
        onStation = 1
    return onStation


"""
Функция "отсева" клиентов из-за нехватки мест на заправке.

"""


"""
Функция вывода завершения заправки.

"""

def gas_station():
    customers = customer_document("input.txt")
    station = gas_document("azs.txt")
    for min in time():
        for buyer_time in customers:
            if buyer_time == min:
                for number in station:
                    if customers[buyer_time][1] in station[number][2]:


                        station[number][3] += "*" # временная строка (до функции "отсева")


                        print("В " + buyer_time + " новый клиент: " + buyer_time + " " +
                              customers[buyer_time][1] + " " + customers[buyer_time][0] + " " +
                              str(refueling_time(customers, buyer_time)) + " " + " встал в очередь к автомату №" + number)
                        presentation_station(station)


gas_station()