
class MainClass():
    a = 0
    b = 0

    def run(self):
        s = int(input("enter: "))


        while True:
            if s == 1 and MainClass.b == 0:
                MainClass.b = 1
                MainClass.a = 1
                print(MainClass.a, MainClass.b, s)
            elif s == 0 and MainClass.b == 0:
                MainClass.b = 1
                MainClass.a = 0
                print(MainClass.a, MainClass.b, s)

t = MainClass()
t.run()
