import time
from dataclasses import dataclass
from simple_term_menu import TerminalMenu

style = ("bg_red", "fg_yellow")
cursor_style = ("fg_red", "bold")
cursor = "> "
cycle_cursor = True
clear_screen = True

@dataclass
class Menu_settings:
    title: str
    items: list 

def main():
    main_menu = Menu_settings(
        title=" Main Menu\n", 
        items=["Show total investments", "Show assets", "See specific account", "Show specific asset", "Quit"]
    ) 

    main_menu = TerminalMenu(
        menu_entries = main_menu.items,
        title = main_menu.title,
        menu_cursor = cursor,
        menu_cursor_style = cursor_style,
        menu_highlight_style = style,
        cycle_cursor = cycle_cursor,
        clear_screen = clear_screen
    )

    accounts_menu = Menu_settings(title=" Accounts\n", items=["Kraken", "Rest"])
    edit_menu = TerminalMenu(
        menu_entries = accounts_menu.items,
        title = accounts_menu.title,
        menu_cursor = cursor,
        menu_cursor_style = cursor_style,
        menu_highlight_style = style,
        cycle_cursor = cycle_cursor,
        clear_screen = clear_screen
    )

    main_menu_exit = False
    edit_menu_back = False
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
            print("option 3 selected")
            time.sleep(5)
        elif main_sel == 3:
            main_menu_exit = True
            print("Quit Selected")

main()