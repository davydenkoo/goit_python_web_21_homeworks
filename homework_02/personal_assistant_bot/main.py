try:
    from classes.menu import MainMenu
except ModuleNotFoundError:
    from personal_assistant_bot.classes.menu import MainMenu

def main():

    MainMenu().show_menu()
    
if __name__ == '__main__':
    main()
