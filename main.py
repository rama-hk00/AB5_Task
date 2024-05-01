import Task2_RamaPassive
import Task3_RamaActive
import cloud



if __name__ == "__main__":

    flag = 1
    while flag == 1:
        if flag == 0:
            break
        while True:
            print("\n\n********************************************************************************************")
            print("Please enter your choice:")
            print("1. Passive scan.")
            print("2. Active scan.")
            print("3. Cloud bruteforcing.")
            print("4. to exit")
            print("********************************************************************************************")

            choice = input("Your choice: ")

            if choice in ['1', '2', '3', '4']:
                break
            else:
                print("\n\nInvalid choice. Please enter a number between 1, 2, or 3.\n\n")

        if choice == '1':
            Task2_RamaPassive.main()
        elif choice == '2':
            Task3_RamaActive.main()
        elif choice == '3':
            cloud.main()
        elif choice == '4':
            flag = 0

