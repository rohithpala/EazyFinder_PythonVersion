import msvcrt

def getPass():
    password = ''
    while True:
        x = msvcrt.getch()
        if x == '\r' or x == '\n':
            break
        print('*', end='', flush=True)
        password +=x
    return password

print("\nout=", getPass())
