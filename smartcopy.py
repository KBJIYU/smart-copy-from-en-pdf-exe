# -*- coding: UTF-8 -*-

######################
### SMART COPY      ##
### AUTHOR: KBJIYU  ##
### VERSION: v1.1.0 ##
######################

import sys
import time
import logging
import win32clipboard

from modifytext import modify_en_text

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_clipboard_text():
    """ Try to get clipboard's text

        Returns:
            text(str):
                string: data from clipboard

    """

    win32clipboard.OpenClipboard()
    try:
        text = win32clipboard.GetClipboardData(
            win32clipboard.CF_UNICODETEXT)
    except (TypeError, win32clipboard.error):
        text = None
    finally:
        win32clipboard.CloseClipboard()

    if text:
        return text
    else:
        raise TypeError(
            "Can't get clipboard's data, might not be text data.")


def set_clipboard_text(new_text):
    """ Try to get clipboard's text

        Args:
            new_text(str):
                data for updating clipboard.

    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    try:
        win32clipboard.SetClipboardData(
            win32clipboard.CF_UNICODETEXT, new_text)
    except:
        logging.warn(
            "Sorry we can't SET your clipboard.")
        raise TypeError("Sorry we can't RESET your clipboard.")
    finally:
        win32clipboard.CloseClipboard()


def smartcopy_runner(modifytext_func, **modifytext_kwargs):
    """ Loops in spying clipboard's action, then modify

        Args:
            modifytext_func (func):  The middleware function to modify your text.

    """
    try:
        last = get_clipboard_text()
    except TypeError:
        last = ""

    while True:
        try:
            current = get_clipboard_text()
        except TypeError:
            current = None

        if current and current != last:
            logging.info(
                "New clipboard data detected.")
            try:
                modified = modifytext_func(current, **modifytext_kwargs)
                logging.info(
                    "Successfully modified your clipboard's data.")
            except:
                modified = current
                logging.info("Failed to modify your clipboard's data.")

            if modified != current:
                try:
                    set_clipboard_text(modified)
                    _status = True
                except TypeError:
                    _status = False

                if _status:
                    last = modified
                else:
                    last = current

            else:
                last = current

        time.sleep(0.1)


def opening_msg():
    print("\n==============================================================\n")
    print(
        """    WELCOME TO SMARTCOPY v1.1.0 ^_^
    歡迎使用 SMARTCOPY !
    希望這項小工具能提升您的工作效率!
    -------------------------------
    > Author: github@kbjiyu
    > Github: https://goo.gl/Pnkazc
    ------------------------------- """)


def input_question():
    while True:
        print("\n==============================================================")
        # questions for params
        try:
            print("請選擇文章輸出模式 Please select the 'modify mode'(default is 1): \n  1 基本 basic\n  2 列表式 list-mark\n  輸入你的選擇(數字)後按下Enter Your Selection: ")
            modify_mode_num = int(input(">_ "))
        except ValueError:
            print("警告! 請輸入選項之對應數字! Warning! Please enter with the limited number.")
        else:
            break

    while True:
        print("\n==============================================================")
        try:
            print("請選擇是否清洗文章內emoji符號 Please select the 'keep_emoji' option(default is 1): \n  1 保存 keep it!\n  2 清洗 remove it\n  輸入你的選擇(數字)後按下Enter Your Selection: ")
            keep_emoji_num = int(input(">_ "))
        except ValueError:
            print("警告! 請輸入選項之對應數字! Warning! Please enter with the limited number.")
        else:
            break

    if modify_mode_num == 2:
        modify_mode = 'LIST-MARK'
    else:
        modify_mode = 'BASIC'

    if keep_emoji_num == 1:
        keep_emoji = True
    else:
        keep_emoji = False

    print("==============================================================")
    print("> modify_mode: {}\n> keep_emoji: {}".format(modify_mode, keep_emoji))
    print("==============================================================")

    return modify_mode, keep_emoji


def unexpected_exit_msg():
    logging.error(
        "Something not excepted happened, please try again, or report it!")
    logging.info(
        """ \n
            -------------------------------
            > Author: github@kbjiyu
            > Github: https://goo.gl/Pnkazc
            ------------------------------- \n
        """
    )
    logging.info(">> Press any key to exit.")


if __name__ == '__main__':

    opening_msg()
    modify_mode, keep_emoji = input_question()

    try:
        logging.info("Smartcopy is running!")
        smartcopy_runner(
            modify_en_text, modify_mode=modify_mode, keep_emoji=keep_emoji)
    except KeyboardInterrupt:
        logging.info("Smartcopy is Exiting. Wish you a nice day^^~")
        sys.exit(0)
    except:
        unexpected_exit_msg()
        input()
