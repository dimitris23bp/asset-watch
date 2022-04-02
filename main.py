import time
from simple_term_menu import TerminalMenu
import main_functions
import logging
from pynput import keyboard

style = ("bg_red", "fg_yellow")
cursor_style = ("fg_red", "bold")
cursor = "> "
cycle_cursor = True
clear_screen = True
is_pressed = False

def on_press(key):
    global is_pressed
    is_pressed = True

def on_release(key):
    global is_pressed
    if (key == keyboard.Key.enter and is_pressed):
        is_pressed = False
        return False

def main():
    main_menu_title = " Main Menu\n"
    main_menu_items = ["Show total investments", "Show assets", "See specific account", "Show specific asset", "Quit"]

    main_menu = TerminalMenu(
        menu_entries = main_menu_items,
        title = main_menu_title,
        menu_cursor = cursor,
        menu_cursor_style = cursor_style,
        menu_highlight_style = style,
        cycle_cursor = cycle_cursor,
        clear_screen = clear_screen
    )

    accounts_menu_title = " Accounts\n"
    accounts_menu_items = main_functions.get_specific_accounts()
    accounts_menu = TerminalMenu(
        menu_entries = accounts_menu_items,
        title = accounts_menu_title,
        menu_cursor = cursor,
        menu_cursor_style = cursor_style,
        menu_highlight_style = style,
        cycle_cursor = cycle_cursor,
        clear_screen = clear_screen
    )

    main_menu_exit = False
    edit_menu_back = False
    accounts_menu_back = False
    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            while not edit_menu_back:
                edit_sel = edit_menu.show()
                if edit_sel == 0:
                    print("Edit Config Selected")
                    time.sleep(5)
                elif edit_sel == 1:
                    print("Save Selected")
                    time.sleep(5)
                elif edit_sel == 2:
                    edit_menu_back = True
                    print("Back Selected")
            edit_menu_back = False
        elif main_sel == 1:
            print("option 2 selected")
            time.sleep(5)

        elif main_sel == 2:
            logging.info("Into specific accounts")
            
            while True:
                accounts_menu_selection = accounts_menu.show()
                # Back button
                if (len(accounts_menu_items) - 1 == accounts_menu_selection):
                    break
                # print(main_functions.show_account(accounts_menu_items[accounts_menu_selection]))
                with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                    listener.join()
        else: 
            main_menu_exit = True
            logging.info("Quit Selected")

main()