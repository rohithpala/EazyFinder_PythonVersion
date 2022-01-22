import os
import sys
import random
import datetime

maxPasswordLength = 16
noOfPlaces = 0
places = []
metro = []
city_adj_mat = [[]]  # 2d list
city: str
username: str
password: str
vehicles = ["Bus", "Bike", "Auto", "Metro", "Cab"]  # Vehicles available
cost_per_km = [2, 3, 4, 5, 6]  # This is the cost per km per vehicle in order
noOfVehicles = 5
timeString: str
dateString: str

dirname, filename = os.path.split(os.path.abspath(__file__))
db = dirname + "\\LogInSignUpDatabase.txt"
th: str


class ModeOfTransport:
    def __init__(self, source, destination, transport, cost):
        self.source = source
        self.destination = destination
        self.transport = transport
        self.cost = cost

    def getValues(self):
        return self.source, self.destination, self.transport, self.cost


def loadDetails(source, destination, cost, couponName, couponDiscount, totalCost):
    global th, timeString, dateString
    with open(th, "a") as userFilePointer:
        userFilePointer.write("City: " + city.upper() + ", From: " + source.upper() + ", To: " + destination.upper() +
                              ", Actual Cost: " + str(cost) + ", Coupon Code: " + couponName +
                              ", Discount: " + str(couponDiscount) + ", Total Cost: " + str(totalCost) +
                              ", Booking Date: " + dateString + ", Booking Time: " + timeString + "\n")


def discount(mst, cost):
    global dirname, th, username
    discountsPath = dirname + "\\discountCoupons.txt"
    noOfCoupons = 0
    couponName, couponDiscount, couponPrice = [], [], []

    with open(discountsPath) as discountFilePointer:
        for line in discountFilePointer:
            lst = line.split()
            couponName.append(lst[0])
            couponDiscount.append(int(lst[1]))
            couponPrice.append(int(lst[2]))
            noOfCoupons += 1

    couponApplicable, welcome = False, False

    for i in range(1, noOfCoupons):
        if cost >= couponPrice[i]:
            couponApplicable = True
            break

    if os.path.getsize(th) == 0:
        welcome = True

    if couponApplicable:
        print("Coupons Applicable for you are:")
        if welcome:
            print("Coupon Code: " + couponName[0] + "\tDiscount: " + str(couponDiscount[0]) + "%\ton bookings of Rs." +
                  str(couponPrice[0]) + " or above")
        for i in range(1, noOfCoupons):
            if cost >= couponPrice[i]:
                print(
                    "Coupon Code: " + couponName[i] + "\tDiscount: " + str(couponDiscount[i]) + "%\ton bookings of Rs."
                    + str(couponPrice[i]) + " or above")

        applyCoupon = input("Do you want to add any coupon[Y/N]? ")
        if applyCoupon.lower() == 'y':
            couponCode = input("Enter Coupon Code: ")
            if couponCode == "WELCOME" and (not welcome):
                return 0

            ind = couponName.index(couponCode)
            if couponCode in couponName and cost >= couponPrice[ind]:
                applyCoupon = input("Do You Want to Proceed[Y/N]? ")
                if applyCoupon.lower() == 'y':
                    print("Coupon Applied successfully")
                    totalCost = cost - (couponDiscount[ind] / 100) * cost
                    print("Total Cost After Coupon is Applied: %.2f" % totalCost)
                    loadDetails(mst[0].source, mst[len(mst) - 1].destination, cost, couponName[ind],
                                couponDiscount[ind], totalCost)
                    return 1
        else:
            print("No Coupon Applied\nTotal Cost: %.2f\n" % cost)
            return -1
    else:
        print("No Coupons Applicable")
        return -1
    return 0


def generateBill(mst):
    cost = 0
    length = len(mst)
    print("Mode of Transport      From\t\t    To\t\t     Price")
    for i in range(length):
        print("%-20s %-20s %-20s %d" % (mst[i].transport, mst[i].source, mst[i].destination, mst[i].cost))
        cost += mst[i].cost
    print("Total Cost: " + str(cost))
    discountSuccess = discount(mst, cost)
    while discountSuccess == 0:
        print("You might have entered an invalid coupon")
        tryAgain = input("Do you want to try again[Y/N]? ")
        if tryAgain.lower() == 'y':
            discountSuccess = discount(mst, cost)
        else:
            break

    if discountSuccess == -1:
        loadDetails(mst[0].source, mst[length - 1].destination, cost, "-", 0, cost)


def inputID():  # Takes the Vehicle ID as Input
    id = int(input())
    while id < 1 or id > 5:
        print("Invalid ID\nSelect a Mode of Transportation: ")
        id = int(input())
    return id


def modeOfTransportBasedOnTraffic(length, route):
    global dirname, metro, noOfPlaces, noOfVehicles, timeString, dateString
    source_index: int
    destination_index: int
    cost: int
    mst, extraCostApplied = [], [0] * noOfVehicles
    start_time, end_time, extra_cost = [], [], []

    trafficChoice = ''
    if length > 2:
        while trafficChoice.lower() != 'y' and trafficChoice.lower() != 'n':
            trafficChoice = input("Do You Want to Select Mode of Transportation based on Traffic [Y/N]: ")
            if trafficChoice.lower() != 'y' and trafficChoice.lower() != 'n':
                print("Please Select a Valid Option")

    with open(dirname + "\\CitiesInfo\\availability-times.txt") as availableTimesPointer:
        for line in availableTimesPointer:
            lst = line.split()
            start_time.append(lst[0])
            end_time.append(lst[1])
            extra_cost.append(int(lst[2]))

    dateString = datetime.date.today().strftime("%d/%m/%Y")
    timeString = datetime.datetime.now().strftime("%H:%M:%S")

    # Display Cost Per Vehicle Table
    print("\nCost Per Kilometer of Vehicles Available:")
    print("Id\tVehicle \tPrice \t ExtraCost")
    print("1 \t %s \t\t %d \t\t -" % (vehicles[0], cost_per_km[0]))
    for i in range(1, noOfVehicles):
        print(str(i + 1) + " \t " + vehicles[i] + " \t\t " + str(cost_per_km[i]), end="")
        if timeString <= start_time[i - 1] or timeString >= end_time[i - 1]:
            print(" \t\t" + str(extra_cost[i]))
            extraCostApplied[i] = 1
        else:
            print(" \t\t -")

    if length > 2 and trafficChoice.lower() == 'y':
        for i in range(length - 1, 0, -1):
            traffic = random.random()
            if traffic == 0:
                print("\nThe route is Clear from " + route[i] + " to " + route[i - 1])
            elif 0 < traffic <= 0.5:
                print("\nThere is Moderate Traffic from " + route[i] + " to " + route[i - 1])
            elif 0.5 < traffic <= 1:
                print("\nThere is Heavy Traffic from " + route[i] + " to " + route[i - 1])
            source_index = places.index(route[i])
            destination_index = places.index(route[i - 1])

            print("Enter the ID of Mode of Transport you Prefer: ", end="")
            id = inputID()
            while id == 4:
                if metro[source_index] == 0 and metro[destination_index] == 0:
                    print("Metro not Available at " + route[i] + " and " + route[i - 1])
                elif metro[source_index] == 0:
                    print("Metro not Available at " + route[i])
                elif metro[destination_index] == 0:
                    print("Metro not Available at " + route[i - 1])
                else:
                    break
                print("Please Select another mode of transport: ", end="")
                id = inputID()
            if extraCostApplied[id - 1] == 0:
                cost = (singleSourceShortestPath(source_index, destination_index, 2)) * cost_per_km[id - 1]
            else:
                cost = (singleSourceShortestPath(source_index, destination_index, 2)) * (
                        cost_per_km[id - 1] + extra_cost[id - 1])
            mst.append(ModeOfTransport(route[i], route[i - 1], vehicles[id - 1], cost))
    else:
        source_index = places.index(route[length - 1])
        destination_index = places.index(route[0])
        print("Select a Mode of Transportation: ", end="")
        id = inputID()
        if extraCostApplied[id - 1] == 0:
            cost = (singleSourceShortestPath(source_index, destination_index, 2)) * cost_per_km[id - 1]
        else:
            cost = (singleSourceShortestPath(source_index, destination_index, 2)) * (
                    cost_per_km[id - 1] + extra_cost[id - 1])
        mst.append(ModeOfTransport(route[length - 1], route[0], vehicles[id - 1], cost))

    print("\nYour Bill:")
    generateBill(mst)


def printRoute(source_index, destination_index, shortestPath, path, case):
    global noOfPlaces, places
    route = []

    i = destination_index
    route.append(places[destination_index])
    while path[i] != source_index:
        route.append(places[path[i]])
        i = path[i]
    route.append(places[source_index])

    # Display the Path
    length = len(route)
    print("\n-------------------------------------------\nRoute: ", end="")
    for i in range(length - 1, -1, -1):
        print(route[i], end="")
        if i != 0:
            print(" -> ", end="")
    print("\n===========================================")
    print("Total Distance: " + str(shortestPath[destination_index]))
    print("-------------------------------------------")

    if case != 0:
        modeOfTransportBasedOnTraffic(length, route)


def singleSourceShortestPath(source_index, destination_index, case):
    global noOfPlaces
    shortestPath, visited, path = [0] * noOfPlaces, [0] * noOfPlaces, [source_index] * noOfPlaces
    min_dist: int
    min_dist_vertex = source_index

    for i in range(noOfPlaces):
        if city_adj_mat[source_index][i] != 0:
            shortestPath[i] = city_adj_mat[source_index][i]
        else:
            shortestPath[i] = sys.maxsize
        visited[i] = 0

    shortestPath[source_index] = 0
    for i in range(noOfPlaces):
        min_dist = sys.maxsize

        # select the vertex that is at minimum distance to source
        for j in range(noOfPlaces):
            if visited[j] == 0 and min_dist >= shortestPath[j]:
                min_dist = shortestPath[j]
                min_dist_vertex = j

        visited[min_dist_vertex] = 1  # set visited to 1

        # now go on relaxing the vertices that are adjacent to min_dist_vertex
        for j in range(noOfPlaces):
            relaxation_calc = shortestPath[min_dist_vertex] + city_adj_mat[min_dist_vertex][j]
            if (not visited[j]) and (city_adj_mat[min_dist_vertex][j] != 0) and (
                    shortestPath[min_dist_vertex] != sys.maxsize) and \
                    (shortestPath[j] > relaxation_calc):
                shortestPath[j] = relaxation_calc
                path[j] = min_dist_vertex

    if case == 1:
        printRoute(source_index, destination_index, shortestPath, path, case)
    elif case == 2:
        return shortestPath[destination_index]


def changeLocation(source, destination, case):
    changeLocationChoice = 'a'
    while changeLocationChoice.lower() != 'y' and changeLocationChoice.lower() != 'n':
        changeLocationChoice = input("Want to Change the Location(s) (Type 'N' to exit) [Y/N]: ")
        if changeLocationChoice.lower() != 'y' and changeLocationChoice.lower() != 'n':
            print("Please Select a Valid Option")

    if changeLocationChoice.lower() == 'y':
        if case == 1 or case == 4:
            source = input("Enter the Source Location Again: ")
            destination = input("Enter the Destination Again: ")
        elif case == 2:
            source = input("Enter the Source Location Again: ")
        elif case == 3:
            destination = input("Enter the Destination Again: ")

        # Check the location again after re-entering
        locationCheck(source, destination)  # This calls check_for_case
    else:
        print("Have A Great Day Ahead :)")
        exit(0)


"""
    Checks for the case based on source and destination:
    case 1: source and destination are wrong
    case 2: source is wrong
    case 3: destination is wrong
    case 4: source and destination same
    case 5: source and destination are correct
"""


def checkForCase(source, destination, source_index, destination_index, case):
    if case == 5:
        singleSourceShortestPath(source_index, destination_index, 1)

    elif case == 1:
        print(
            "Sorry! Our Services are not available at " + source + " and " + destination + "\nOr you have entered wrong locations")

    elif case == 2:
        print("Sorry! Our Services are not available at " + source)

    elif case == 3:
        print(
            "Sorry! We do not serve from " + source + " to " + destination + "\nOr You have entered a wrong Destination")

    elif case == 4:
        print("Source and Destination cannot be the same")

    if case != 5:
        changeLocation(source, destination, case)


def locationCheck(source, destination):
    source_index = -1
    destination_index = -1

    if source in places:
        source_index = places.index(source)
    if destination in places:
        destination_index = places.index(destination)

    if source_index == -1 and destination_index == -1:
        case = 1
    elif source_index == -1:
        case = 2
    elif destination_index == -1:
        case = 3
    elif source_index == destination_index:
        case = 4
    else:
        case = 5
    checkForCase(source, destination, source_index, destination_index, case)


def locationInput():
    source = input("Enter the Starting Point: ").lower()
    destination = input("Enter the Destination: ").lower()
    locationCheck(source, destination)


def displayMap():
    global noOfPlaces, places, city_adj_mat
    print("\n From\t\t\t To\t\tDistance")
    for i in range(noOfPlaces):
        for j in range(noOfPlaces):
            if city_adj_mat[i][j]:
                print("%-20s %-20s %-3d" % (places[i], places[j], city_adj_mat[i][j]))
        print()


def connectPlaces(source, destination, distance):
    global city_adj_mat
    city_adj_mat[int(source)][int(destination)] = city_adj_mat[int(destination)][int(source)] = int(distance)


def formCity():
    global noOfPlaces, dirname, city, city_adj_mat
    # Initializing city_adj_mat
    city_adj_mat = [[0] * noOfPlaces for _ in range(noOfPlaces)]
    connectionsPath = dirname + "\\CitiesInfo\\" + city + "-connections.txt"
    with open(connectionsPath) as connectionsFilePointer:
        for line in connectionsFilePointer:
            connectPlaces(*line.split())


# Option 1: Bookings
def bookings():
    global city, dirname, noOfPlaces, places, metro
    print("\n---------------------Welcome to EazyFinder!!!!---------------------")
    print("Select one of the City IDs:\n1) Hyderabad\n2) Bengaluru\n3) Chennai")
    while True:
        cityChoice = int(input())
        if cityChoice == 1:
            city = "hyderabad"
            break
        elif cityChoice == 2:
            city = "bengaluru"
            break
        elif cityChoice == 3:
            city = "chennai"
            break
        else:
            print("Please Select a valid Option\nSelect one of the City IDs: ")

    cityPath = dirname + "\\CitiesInfo\\" + city + ".txt"
    places, metro = [], []
    with open(cityPath) as cityFilePointer:
        for line in cityFilePointer:
            lst = line.split()
            places.append(lst[0])
            metro.append(int(lst[1]))
            noOfPlaces += 1

    formCity()

    print("\nMap:")
    displayMap()

    locationInput()


# Option 2: Transaction History
def transactionHistory():
    global th
    if os.path.getsize(th) == 0:
        print("You Have no Transactions Yet!!!")
    else:
        with open(th) as userFilePointer:
            print(userFilePointer.read())


def updateUsername():
    global db, th, username, password

    with open(db) as adminFile:
        credentials = adminFile.readlines()

    while True:
        newUsername = input("Enter new Username: ")
        if newUsername == username:
            print("Cannot switch with the same account")
        elif newUsername + " " + str(encryptPassword(password)) + "\n" in credentials:
            print("Username already taken. Try with another one")
        else:
            break

    accountDeletion('U')
    with open(db, "a") as adminFile:
        adminFile.write(newUsername + " " + str(encryptPassword(password)) + "\n")

    os.rename(th, dirname + "\\TransactionHistories\\" + newUsername + ".txt")
    username = newUsername
    return True


# Option 3: Password Change
def passwordChange():
    global username, password, db
    while True:
        newPassword = input("Enter New Password: ")
        while newPassword == password:
            print("Password Cannot be same as Old One")
            newPassword = input("Enter New Password: ")
        if isPasswordAccepted(newPassword):
            accountDeletion('P')
            with open(db, "a") as adminFile:
                adminFile.write(username + " " + str(encryptPassword(newPassword)) + "\n")
            password = newPassword
            return True


# Option 4: Account Deletion
def accountDeletion(ch):
    global username, password, db
    with open(db) as adminFile:
        credentials = adminFile.readlines()
        credentials.remove(username + " " + str(encryptPassword(password)) + "\n")

    with open(db, "w") as adminFile:
        adminFile.writelines(credentials)

    if ch != 'P' and ch != 'U':  # If function is not called by Password Change function
        os.remove(th)


def EazyFinder():
    # Display Menu
    optionChoice = 'y'
    while optionChoice.lower() == 'y':
        menuChoice = input("Select an Option:\n1) Bookings\n2) Transaction History\n3) Update Username\n"
                           "4) Password Change\n5) Account Deletion\n6) Switch Accounts\n7) Logout\n")
        if menuChoice == "1":
            bookings()

        elif menuChoice == "2":
            transactionHistory()

        elif menuChoice == "3":
            if updateUsername():
                print("\nUsername Changed Successfully\n")
            else:
                print("Some Error Occurred, Couldn't update the username")

        elif menuChoice == "4":
            if passwordChange():
                print("Password Changed Successfully")
            else:
                print("Password Not Changed")

        elif menuChoice == "5":
            accountDeletionChoice = input("Are You Sure [Y/N]? ")
            if accountDeletionChoice.isalpha():
                if accountDeletionChoice.lower() == 'y':
                    accountDeletion('A')
                    print("We Are Sorry to see you go :(")
                    exit(0)
                elif accountDeletionChoice.lower() == 'n':
                    print("Don't Worry! Your Account isn't Deleted")
                    break
            else:
                print("It's not a valid choice. Please type again")

        elif menuChoice == "6":
            pass

        elif menuChoice == "7":
            print("Logged Out Successfully")
            exit(0)

        else:
            print("Invalid Input")
        optionChoice = input("Want to Select between Options Again [Y/N]? ")


def encryptPassword(password_):
    code = 0
    a = 1
    length = len(password_)
    for i in range(length):
        code += ord(password_[i]) * a
        a *= 100
    return code


def isPasswordAccepted(password_):
    global maxPasswordLength
    length = len(password_)
    passwordAccepted = True
    if length < 8:
        print("Password is too Short. Must Contain Minimum of 8 Characters")
        passwordAccepted = False
    elif length > 16:
        print("Password is too Long. Maximum Acceptable Characters is", maxPasswordLength)
        passwordAccepted = False

    lowerCaseUsed, upperCaseUsed, splCharUsed, numUsed = False, False, False, False
    for ch in password_:
        if ch.isalpha():
            if ch.isupper():
                upperCaseUsed = True
            else:
                lowerCaseUsed = True
        elif ch.isnumeric():
            numUsed = True
        else:
            splCharUsed = True

    if not lowerCaseUsed:
        print("At-least One Lower Case Character must be Used")
    if not upperCaseUsed:
        print("At-least One Upper Case Character must be Used")
    if not numUsed:
        print("At-least One Number must be Used")
    if not splCharUsed:
        print("At-least One Special Character must be Used")

    if passwordAccepted and lowerCaseUsed and upperCaseUsed and numUsed and splCharUsed:
        passwordAccepted = True

    return passwordAccepted


def SignUp_LogIn(ch):
    global db, username, password
    if ch == 'S':
        username = input("Username: ")
        with open(db) as adminFile:
            for line in adminFile:
                scannedUsername, scannedPassword = line.split(' ')
                if scannedUsername == username:
                    print("Username already taken. Try with Another one")
                    return False
        while True:
            password = input("Set Password [Max of " + str(maxPasswordLength) + " characters]: ")
            if isPasswordAccepted(password):
                with open(db, "a") as adminFile:
                    adminFile.write(username + " " + str(encryptPassword(password)) + "\n")
                f = open(dirname + "\\TransactionHistories\\" + username + ".txt", "x")
                f.close()
                print("\nAccount Created Successfully\n")
                return True

    else:
        found = False
        while not found:
            username = input("Username: ")
            with open(db) as adminFile:
                for line in adminFile:
                    scannedUsername, scannedPassword = line.split()
                    if scannedUsername == username:
                        found = True
                        break
            if found:
                password = input("Password: ")
                if scannedPassword == str(encryptPassword(password)):
                    print("\nLogged in Successfully\n")
                    return True
                else:
                    print("Password Incorrect")
                    return False
            else:
                print("No User with given Username")


def callSignUpLogIn():
    SLChoice = input("SignUp or Login: ").lower()
    if SLChoice == "signup":
        return SignUp_LogIn('S')
    elif SLChoice == "login":
        return SignUp_LogIn('L')
    else:
        print("It's not a valid choice. Please type again")
        return callSignUpLogIn()


# Main Code
choice = 'y'
while choice.lower() == 'y':
    if callSignUpLogIn():
        th = dirname + "\\TransactionHistories\\" + username + ".txt"
        EazyFinder()
        choice = 'n'
    else:
        choice = input("Want to Try Again [Y/N]? ")
    if choice.lower() == 'n':
        print("Have a Great Day Ahead :)")
