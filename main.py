from simple_term_menu import TerminalMenu
import main_functions
import logging
from pynput import keyboard

style = ("bg_red", "fg_yellow")
cursor_style = ("fg_red", "bold")
cursor = "> "
cycle_cursor = True
clear_screen = True

def on_release(key):
    if key == keyboard.Key.backspace:
        return False

def main():
    main_menu_title = " Main Menu\n"
    main_menu_items = ["Show total investment", "Show assets", "See specific account", "Show specific asset", "Quit"]

    main_menu = TerminalMenu(
        menu_entries = main_menu_items,
        title = main_menu_title,
        menu_cursor = cursor,
        menu_cursor_style = cursor_style,
        menu_highlight_style = style,
        cycle_cursor = cycle_cursor,
        clear_screen = clear_screen
    )

    assets_menu_title = " Assets\n"
    assets_menu_items = main_functions.get_specific_asset()
    assets_menu = TerminalMenu(
        menu_entries = assets_menu_items,
        title = assets_menu_title,
        menu_cursor = cursor,
        menu_cursor_style = cursor_style,
        menu_highlight_style = style,
        cycle_cursor = cycle_cursor,
        clear_screen = clear_screen
    )

    accounts_menu_title = " Accounts\n"
    accounts_menu_items = main_functions.get_specific_account()
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
    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            logging.info("Into total, investment")
            main_functions.show_total()
            with keyboard.Listener(on_release=on_release) as listener:
                listener.join()
        elif main_sel == 1:
            print("Into specific asset")
            while True:
                assets_menu_selection = assets_menu.show()
                # Back button
                if (len(assets_menu_items) - 1 == assets_menu_selection):
                    break
                selected_asset = assets_menu_items[assets_menu_selection]
                # main_functions.display_asset(selected_asset)
                with keyboard.Listener(on_release=on_release) as listener:
                    listener.join()
                

        elif main_sel == 2:
            logging.info("Into specific account")
            
            while True:
                accounts_menu_selection = accounts_menu.show()
                # Back button
                if (len(accounts_menu_items) - 1 == accounts_menu_selection):
                    break
                selected_account = accounts_menu_items[accounts_menu_selection]
                main_functions.display_all_wallets( main_functions.get_balance_from_account(selected_account) )
                with keyboard.Listener(on_release=on_release) as listener:
                    listener.join()
        else: 
            main_menu_exit = True
            logging.info("Quit Selected")

main()