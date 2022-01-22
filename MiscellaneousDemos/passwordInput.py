from msvcrt import getch
maxPasswordLength = 16

def passwordInput():
     try:
          password = ""
          i = 0
          while True:
               ch = ord(getch())
               if ch == 13:
                    if(len(password) == 0):
                         print("\nPassword Cannot be Empty")
                    else:
                         break
               elif ch == 32 or ch == 9:
                    continue
               elif ch == 8:
                    if(i > 0):
                         i -= 1
                         print("\b \b")
               else:
                    if i < maxPasswordLength:
                         print("*", end="")
                         password += chr(ch)
                         i += 1
          return password
     except:
          print("Error")
print(passwordInput())
