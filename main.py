#!/usr/bin/env python3
import os, sys, argparse

from prettytable import PrettyTable
from colorama import Fore


def parser():
    parser = argparse.ArgumentParser(description='Count all lines, files and folders in a directory.')
    parser.add_argument("-p", '--path', metavar='N', type=str, help='the path to the folder.')
    parser.add_argument("-e", '--ext', type=str, help='set extensions to search.')

    parser.add_argument("-i", '--ign', type=str, help='set extensions to ignore.')

    parser.add_argument("-d", "--dirign", type=str, help="set directories to ignore.")

    parser.add_argument("-v", "--verbose", help="set verbose mode.", action="store_true")

    args = parser.parse_args()
    return args

def main():
    args = parser()

    table = PrettyTable()
    check = True
    if not args.path:
        while check:
            PATH = input(Fore.YELLOW + "Path: " + Fore.RESET)
            if os.path.exists(PATH) and os.path.isdir(PATH):
                check = False
            else:
                print(Fore.RED + "Please enter a valid path to a directory..." + Fore.RESET)

    else:
        PATH = args.path
        if not os.path.exists(PATH) and not os.path.isdir(PATH):
            print(Fore.RED + "Please enter a valid path to a directory..." + Fore.RESET)
            exit(1)
    if not args.ext and not args.ign:
        EXTENSIONS = input(Fore.YELLOW + "Extensions: " + Fore.RESET).split()
    else:
        if args.ext:
            EXTENSIONS = args.ext.split()
        else:
            EXTENSIONS = None


    if not EXTENSIONS:
        if not args.ign:
            IGNORE = input(Fore.YELLOW + "Extensions to Ignore: " + Fore.RESET).split()
        else:
            IGNORE = args.ign.split()
    else:
        IGNORE = None

    if not args.dirign:
        DIR_IGNORE = input(Fore.YELLOW + "Folders to Ignore: " + Fore.RESET).split()
    else:
        DIR_IGNORE = args.dirign.split()


    if not args.verbose:
        VERBOSE = input(Fore.YELLOW + "Verbose[Y|N]: " + Fore.RESET)
    else:
        VERBOSE = "y"

    print("Depending on the size of the selected path this might take a while.")

    if not PATH.endswith("/"):
        PATH + "/"

    num_lang = 0
    all_files = {}
    languages = {}
    folders = {}
    size = {}
    size_per_file = {}
    total_files, total_dirs, total_lines, total_size = 0, 0, 0, 0
    for base, dirs, files in os.walk(PATH):




        #ignore folders that were set to ignore
        if DIR_IGNORE:
            if any(ign in base for ign in DIR_IGNORE):
                continue


        for directorie in dirs:

            if not directorie in folders: folders[directorie] = 1
            else: folders[directorie] += 1

            total_dirs += 1

        for File in files:
            ext = os.path.splitext(File)[1][1:]
            if IGNORE and "." + ext in IGNORE:
                continue
            if EXTENSIONS and "." + ext not in EXTENSIONS:
                continue

            total_files += 1

            if not ext:
                ext = File


            if not ext in languages: languages[ext] = [1]
            else: languages[ext][0] += 1

            if not ext in size: size[ext] = os.path.getsize(base + "/" + File)
            else: size[ext] += os.path.getsize(base + "/" + File)

            total_size += os.path.getsize(base + "/" + File)
            cena = base + File if base.endswith("/") else base + "/" + File
            if cena not in size_per_file:
                size_per_file[cena] = os.path.getsize(cena)

            try:
                for lines in range(len(open(rf"{cena}", "r").readlines())):



                    #Getting lines per language
                    if len(languages[ext]) == 1:
                        languages[ext].append(1)

                    else:
                        languages[ext][1] += 1



                    #Getting lines per file
                    #cena = base + File if base.endswith("/") else base + "/" + File
                    if cena not in all_files:
                        all_files[cena] = 1
                    else:
                        all_files[cena] += 1

                    #all lines
                    total_lines += 1
                    #total_size += os.path.getsize(base + "/" + File)
            except UnicodeDecodeError:
                if VERBOSE.lower() in ["y", "yes"]:
                    print(f"Could not read {cena} because its a binary...")
                continue
            except PermissionError:
                if VERBOSE.lower() in ["y", "yes"]:
                    print(f"Could not read {cena}, run this program with root privelages...")
                continue
            except OSError: 
                if VERBOSE.lower() in ["y", "yes"]:
                    print(f"Could not read {cena}, Invalid Argument/File...")
                continue

    if EXTENSIONS:
        for extension in EXTENSIONS:
            if extension.replace(".", "") not in languages:
                print(Fore.RED + f"{extension + Fore.RESET} is not found...")
            else:
                break
        else:
            exit()



    print(f"There are {Fore.BLUE + str(total_dirs) + Fore.RESET} directories, {Fore.GREEN + str(total_files) + Fore.RESET} files and {Fore.YELLOW + str(total_lines) + Fore.RESET} lines in \033[1m{os.path.realpath(PATH)}\033[0m.")

    my_table = PrettyTable()

    my_table.field_names = [
        Fore.LIGHTMAGENTA_EX + "Language" + Fore.RESET,
        Fore.CYAN + "Files" + Fore.RESET,
        Fore.LIGHTCYAN_EX + "Files Percentages" + Fore.RESET,
        Fore.MAGENTA + "Lines" + Fore.RESET,
        Fore.LIGHTMAGENTA_EX + "Lines Percentages" + Fore.RESET,
        Fore.GREEN + "Size(kB)" + Fore.RESET,
        Fore.LIGHTGREEN_EX + "Size Percentages" + Fore.RESET,
    ]




    if total_dirs > 0:
        table.field_names = [Fore.BLUE + "Folder Name" + Fore.RESET, Fore.GREEN + "Folder ???" + Fore.RESET]
        for pasta, num in folders.items():
            table.add_row([pasta, num])

        table.add_row([Fore.LIGHTMAGENTA_EX + "Sum:" + Fore.RESET, total_dirs]) #sum of num of files
        print(table)

    
    for language in languages:
        try:
            my_table.add_row(
                [
                    language, #language name
                    languages[language][0], #num of language files
                    str(round((languages[language][0] / total_files) * 100, 2)) + "%",
                    languages[language][1], #num of lines
                    str(round((languages[language][1] / total_lines) * 100, 2)) + "%", #line percentage
                    size[language] / 1000 if len(str(size[language])) < 6 else str(round(size[language] * 1e-6, 2)) + "(MB)", #language size
                    str(round((size[language] / total_size) * 100, 2)) + "%" #size percentage of language
                ]
            )
        except IndexError:
            my_table.add_row(
                [
                    language, #language name
                    languages[language][0], #num of language files
                    str(round((languages[language][0] / total_files) * 100, 2)) + "%",
                    0, #num of lines
                    0, #line percentage
                    size[language] / 1000 if len(str(size[language])) < 6 else str(round(size[language] * 1e-6, 2)) + "(MB)", #language size
                    str(round((size[language] / total_size) * 100, 2)) + "%" #size percentage of language
                ]
            )


    my_table.add_row(
        [
            Fore.RED + f"SUM:({len(languages)})" + Fore.RESET, #sum of languages
            Fore.CYAN + str(total_files) + Fore.RESET, #total files
            Fore.LIGHTCYAN_EX + "100%" + Fore.RESET,
            Fore.MAGENTA + str(total_lines) + Fore.RESET, # total lines
            Fore.LIGHTMAGENTA_EX+ "100%" + Fore.RESET, #total line percentage
            Fore.GREEN + (str(total_size / 1000) + "(kB)" if len(str(total_size)) < 6 else str(round(total_size * 1e-6, 2)) + "(MB)") + Fore.RESET, #total size
            Fore.LIGHTGREEN_EX + "100%" + Fore.RESET #total size percentage
        ]
    )

    print(my_table)
    for count, (ficheiro, valores) in enumerate(all_files.items()):
        length = len(str(round(size_per_file[ficheiro])))
        length_str = str(round((size_per_file[ficheiro]) / total_size) * 100)
        if length < 6:
            length_str += "(MB)"



        print(f"{ficheiro}\t\t -> " + Fore.GREEN + str(valores) + "/" + str(round((valores / total_lines) * 100, 2)) + "%\t" + (str(size_per_file[ficheiro] / 1000) + "(kB)" if len(str(size_per_file[ficheiro])) < 6 else str(size_per_file[ficheiro] * 1e-6) + "(MB)") + "/" + str(round((size_per_file[ficheiro] / total_size) * 100, 2)) + "%" + Fore.RESET)
        if count == 25 and not VERBOSE.lower() in ["y", "yes"]:
            print("\033[1mThis project is too big to show all the files...\033[0m")
            break


    print(Fore.YELLOW + f"Lines/File{Fore.RESET} -> {round(total_lines / total_files, 3)}")
    print(Fore.YELLOW + "Size/File" + Fore.RESET + " -> " + (str(round(total_size / total_files, 2) / 1000) + "(kB)" if len(str(round(total_size/ total_files))) < 6 else str(round((total_size / total_files) * 1e-6, 2)) + "(MB)"))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\nBye..." + Fore.RESET)
else:
    print(Fore.RED + "DIE!!!!!!!!!!!!!" + Fore.RESET)
#this was made when I was hospitalized in Braga :)
