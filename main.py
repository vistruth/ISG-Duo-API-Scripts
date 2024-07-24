import os
import sys
import time






def secret_check():
    if os.path.isfile("IgnoreFolder/keys.py"):
        main_menu()
    elif not os.path.isdir("IgnoreFolder"):
        print("no direct")
        os.mkdir("IgnoreFolder")
        secret_check()
    else:
        print("\n\nSeems like you have some missing information.\n\n\nPlease enter the values for the following...\n\n")
        f = open("IgnoreFolder/keys.py", "a")
        f.write("integration = \"" + input("Enter Intergration key here: ") + "\"\n")
        f.write("secret = \"" + input("Enter secret here: ") + "\"\n")
        f.write("host = \"" + input("Enter Host here: ") + "\"\n")

        f.close()
        f = open("IgnoreFolder/keys.py", "r")
        print(f.read())
        secret_check()


    main_menu()





def main_menu():
    print("This is ISGs DUO API scripts\n\n")
    option = 0
    while option == 0:
        print("Please select which option you want and enter the number associated with it.")
        print("1 - Get user info")
        print("2 - Get Bypass code")
        print("3 - Delete bypass codeGet user info")
        print("4 - Update alias")
        print("5 - User creation")
        print("6 - User deletion")
        option = int(input("(Use numbers only) Enter number here: "))
        if option == 1:
            import getUserInfo
        elif option == 2:
            import getBypassCode
        elif option == 3:
            import deleteBypassCode
        elif option == 4:
            import updateAlias
        elif option == 5:
            import userCreation
        elif option == 6:
            import userDeletion
        else:
            print("This option isn't available, redirecting back to the main menu.\n\n")
            main_menu()
def exit():
    option = 0
    while option == 0:
        print("To quit the program Select 1\nTo go back to the main menu choose 2")
        option = int(input("(Use numbers 1 or 2 only!!!) Enter number here: "))
        if option == 1:
            print("Application will exit in 5 seconds, Thanks")
            time.sleep(5)
            sys.exit()
        elif option == 2:
            print("Returning back to the Main menu in 5 seconds, Thanks\n\n\n\n")
            time.sleep(5)
            main_menu()





if __name__ == "__main__":
    secret_check()