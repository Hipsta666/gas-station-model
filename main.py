import random


def customer_document(file):
    with open(file, encoding="utf8") as file_input:
        table = {}
        for i in file_input:

            if i.split(" ")[0] not in table:
                table[i.split(" ")[0]] = [i.split(" ")[1], i.split(" ")[2]]
            else:
                table[(i.split(" ")[0]) + "+"] = [i.split(" ")[1], i.split(" ")[2]]
    return table


def gas_document(file):
    with open(file, encoding="utf8") as file_azs:
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


def change_time(time, min):
    a = str(int(time[3:]) + int(min))

    if int(a) < 10:
        fin = time[:4] + a
        return fin
    elif 9 < int(a) < 61:
        fin = time[:3] + a
        return fin
    elif int(a) > 60:
        d = ""
        c = int(a) - 60
        if c < 10:
            d = "0" + str(c)
        elif c > 9:
            d = str(c)

        b = str(int(time[:2]) + 1)

        if int(b) < 10:
            fin = time[:1] + b + ":" + d
            return fin
        elif 9 < int(b) < 24:
            fin = b + ":" + d
            return fin

        elif int(b) > 23:
            fin = "00" + ":" + d
            return fin


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


def message(data_1, time, point, dict, num, passiv):
    if point == "lose_customer":
        rand = str(refueling_time(data_1, time))
        print("В " + time + " новый клиент: " \
              + time + " " + data_1[time][1][:5] \
              + " " + data_1[time][0] + " " \
              + rand \
              + " " + "не смог заправить автомобиль и покинул АЗС.")
        dict[change_time(time, rand)] = [time, rand, data_1[time][1][:5], data_1[time][0], num]
        passiv["покинули с " + data_1[time][1][:5]] += 1
        
    if point == "new_customer":
        rand = str(refueling_time(data_1, time))
        print("В " + time + " новый клиент: " \
              + time + " " + data_1[time][1][:5] \
              + " " + data_1[time][0] + " " \
              + rand \
              + " " + " встал в очередь к автомату №" + num)
        dict[change_time(time, rand)] = [time, rand, data_1[time][1][:5], data_1[time][0], num]
        passiv[data_1[time][1][:5]] += int(data_1[time][0])


def refueling_condition(data_1, data_2, time, dict_1, dict_2, point_1, point_2, passive):
    if data_1[time][1][:5] in data_2["1"][2]:

        if len(data_2["1"][3]) < int(data_2["1"][1]):
            data_2["1"][3] += "*"
            message(data_1, time, point_1, dict_2, "1", passive)
            presentation_station(data_2)

        elif len(data_2["1"][3]) >= int(data_2["1"][1]):
            message(data_1, time, point_2, dict_2, "1", passive)
            dict_1["покинули"] += 1

            presentation_station(data_2)
    elif data_1[time][1][:5] in data_2["2"][2]:

        if len(data_2["2"][3]) < int(data_2["2"][1]):
            data_2["2"][3] += "*"
            message(data_1, time, point_1, dict_2, "2", passive)
            presentation_station(data_2)

        elif len(data_2["2"][3]) >= int(data_2["2"][1]):
            if data_1[time][1][:5] in data_2["3"][2]:

                if len(data_2["3"][3]) < int(data_2["3"][1]):
                    data_2["3"][3] += "*"
                    message(data_1, time, point_1, dict_2, "3", passive)
                    presentation_station(data_2)

                elif len(data_2["3"][3]) >= int(data_2["3"][1]):
                    message(data_1, time, point_2, dict_2, "3", passive)
                    dict_1["покинули"] += 1
                    presentation_station(data_2)
            else:
                message(data_1, time, point_2, dict_2, "3", passive)
                dict_1["покинули"] += 1

    elif data_1[time][1][:5] in data_2["3"][2]:

        if len(data_2["3"][3]) < int(data_2["3"][1]):
            data_2["3"][3] += "*"
            message(data_1, time, point_1, dict_2, "3", passive)
            presentation_station(data_2)

        elif len(data_2["3"][3]) >= int(data_2["3"][1]):
            message(data_1, time, point_2, dict_2, "3", passive)
            dict_1["покинули"] += 1
            presentation_station(data_2)
    else:
        message(data_1, time, point_2, dict_2, "3", passive)
        presentation_station(data_2)
        dict_1["покинули"] += 1


def main():
    possive = {"покинули": 0, "АИ-80": 0, "АИ-92": 0, "АИ-95": 0,
               "АИ-98": 0, "цена АИ-80": 50, "цена АИ-92": 51, "цена АИ-95": 48, "цена АИ-98": 53,
               "покинули с АИ-80": 0, "покинули с АИ-92": 0, "покинули с АИ-95": 0, "покинули с АИ-98": 0}
    have_customers = dict()
    customers = customer_document("input.txt")
    station = gas_document("azs.txt")
    for min in time():
        for buyer_time in customers:
            if buyer_time == min:
                refueling_condition(customers, station, buyer_time,
                                    possive, have_customers, 'new_customer',
                                    'lose_customer', possive)

        for num in have_customers:
            if num == min:
                print("В " + num + " клиент:", have_customers[num][0],
                      have_customers[num][2], have_customers[num][3],
                      have_customers[num][1], "заправил свой автомобиль и покинул АЗС.")
                station[have_customers[num][4]][3] = station[have_customers[num][4]][3][:-1]
                presentation_station(station)

    print("\nКоличество литров, проданное за сутки АИ-80: " + str(possive["АИ-80"]) + "л" + "\n" +
          " " * 38 + "АИ-92: " + str(possive["АИ-92"]) + "л" + "\n" +
          " " * 38 + "АИ-95: " + str(possive["АИ-95"]) + "л" + "\n" +
          " " * 38 + "АИ-98: " + str(possive["АИ-98"]) + "л")
    profit = possive["АИ-80"] * possive["цена АИ-80"] + possive["АИ-92"]\
             * possive["цена АИ-92"] + possive["АИ-95"] * possive["цена АИ-95"]\
             + possive["АИ-98"] * possive["цена АИ-98"]
    print("\nОбщая сумма продаж за сутки составила " + str(profit) + " рублей.")

    print("\nИз-за очереди, не заправив автомобиль" + " АИ-80 " + "уехало " + str(possive["покинули с АИ-80"])
          + "\n" + " " * 37 + " АИ-92 " + "уехало " + str(possive["покинули с АИ-92"])
          + "\n" + " " * 38 + "АИ-95 " + "уехало " + str(possive["покинули с АИ-95"])
          + "\n" + " " * 38 + "АИ-98 " + "уехало " + str(possive["покинули с АИ-98"])
          + "\n" + " " * 38 + "Всего: " + str(possive["покинули"]))


if __name__ == "__main__":
    main()
