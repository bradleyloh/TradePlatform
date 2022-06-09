buyOrder = []
sellOrder = []


def limitOrder(order):
    tradeOrder = order[2]
    tradeID = order[3]
    tradeQty = int(order[4])
    tradePrice = int(order[5])
    totalcost = 0
    # Buy Order
    if tradeOrder == "B":
        # If sellOrder not empty
        if sellOrder:
            totalcost = 0
            i = 0
            while (tradePrice >= sellOrder[i][5]):
                if tradeQty <= sellOrder[i][4]:
                    sellOrder[i][4] = sellOrder[i][4] - tradeQty
                    totalcost = totalcost + (tradeQty * sellOrder[i][5])
                    tradeQty = 0
                else:
                    tradeQty = tradeQty - sellOrder[i][4]
                    totalcost = totalcost + (sellOrder[i][4] * sellOrder[i][5])
                    sellOrder[i][4] = 0
                i += 1
                if i == len(sellOrder) or tradeQty == 0:
                    break
            # print(totalcost)
            updatedTrade = [order[0], order[1], order[2], order[3], tradeQty, tradePrice]
            buyOrder.append(updatedTrade)
        # If sellOrder empty
        else:
            order = ["SUB"] + order[1:4] + [tradeQty] + [tradePrice]
            buyOrder.append(order)
    if tradeOrder == "S":
        # If buyOrder not empty
        if buyOrder:
            i = 0
            while (tradePrice <= buyOrder[i][5]):
                if tradeQty <= buyOrder[i][4]:
                    buyOrder[i][4] = buyOrder[i][4] - tradeQty
                    totalcost = totalcost + (tradeQty * buyOrder[i][5])
                    tradeQty = 0
                else:
                    tradeQty = tradeQty - buyOrder[i][4]
                    totalcost = totalcost + (buyOrder[i][4] * tradePrice)
                    buyOrder[i][4] = 0
                i += 1
                if i == len(buyOrder) or tradeQty == 0:
                    break
            # print(totalcost)
            updatedTrade = [order[0], order[1], order[2], order[3], tradeQty, tradePrice]
            sellOrder.append(updatedTrade)
        # If sellOrder empty
        else:
            order = ["SUB"] + order[1:4] + [tradeQty] + [tradePrice]
            sellOrder.append(order)
    print(totalcost)


# S [['SUB', 'LO', 'S', 'IpD8', 150, 14], ['SUB', 'LO', 'S', 'y93N', 190, 15]]
# Bubble sort
def sortAndRemoveOrder(orderList):
    i = 0
    length = len(orderList)
    while i != length:
        if orderList[i][4] == 0:
            orderList.remove(orderList[i])
            length = len(orderList)
        else:
            break
    sorted = False
    while not sorted:
        sorted = True
        for order in range(0, len(orderList) - 1):
            if orderList[order][5] > orderList[order + 1][5]:
                sorted = False
                hold = orderList[order + 1]
                orderList[order + 1] = orderList[order]
                orderList[order] = hold
    return orderList


def marketOrder(orderSplit):
    tradeOrder = orderSplit[2]
    tradeID = orderSplit[3]
    tradeQty = int(orderSplit[4])
    totalcost = 0
    if tradeOrder == "B":
        # if sellOrder is not empty
        if sellOrder:
            for order in sellOrder:
                # print(order)
                if tradeQty <= order[4]:
                    order[4] = order[4] - tradeQty
                    totalcost = totalcost + (tradeQty * order[5])
                    tradeQty = 0
                if tradeQty > order[4] and order[4] != 0:
                    totalcost = totalcost + (order[4] * order[5])
                    tradeQty = tradeQty - order[4]
                    order[4] = 0
                if tradeQty == 0:
                    break
    if tradeOrder == "S":
        # if buyOrder is not empty
        if buyOrder:
            for order in buyOrder:
                if tradeQty <= order[4]:
                    order[4] = order[4] - tradeQty
                    totalcost = totalcost + (tradeQty * order[5])
                    tradeQty = 0
                if tradeQty > order[4] and order[4] != 0:
                    tradeQty = tradeQty - order[4]
                    totalcost = totalcost + (tradeQty * order[5])
                    order[4] = 0
                if tradeQty == 0:
                    break
    print(totalcost)


def cancelOrder(orderSplit):
    orderID = orderSplit[1]
    for order in sellOrder:
        if orderID == order[3]:
            sellOrder.remove(order)
            break
    for order in buyOrder:
        if orderID == order[3]:
            buyOrder.remove(order)
            break


# Quantity@Price#OrderID
# 5,4,3
def formatOutput(buy, sell):
    buy = buy[::-1]
    buy_output = []
    sell_output = []
    for order in buy:
        order = str(order[4]) + "@" + str(order[5]) + "#" + order[3]
        buy_output.append(order)
    for order in sell:
        order = str(order[4]) + "@" + str(order[5]) + "#" + order[3]
        sell_output.append(order)
    return " ".join(buy_output), " ".join(sell_output)


def main(input):
    orderSplit = input.split()
    # Cancel Order
    if orderSplit[0] == "CXL":
        cancelOrder(orderSplit)
    if orderSplit[0] == "SUB":
        # Limit Order
        if orderSplit[1] == "LO":
            limitOrder(orderSplit)
        # Market Order
        if orderSplit[1] == "MO":
            marketOrder(orderSplit)
    sortAndRemoveOrder(buyOrder)
    sortAndRemoveOrder(sellOrder)
    # print("B", buyOrder)
    # print("S", sellOrder)


if __name__ == "__main__":
    text = ""
    while text != "END":
        text = input()
        main(text)
    buyOrder, sellOrder = formatOutput(buyOrder, sellOrder)
    print("B:", buyOrder)
    print("S:", sellOrder)
