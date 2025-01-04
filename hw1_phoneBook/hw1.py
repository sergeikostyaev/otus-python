import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
FILE_NAME = "dict.txt"


def map_lines_to_dictionary(lines):
    dictionary = {}
    if not lines:
        logging.info("Dictionary is empty as file is empty")
        return dictionary

    for line in lines:
        try:
            key, value, comment = line.strip().split(":", 2)
            dictionary[key] = (value, comment)
        except ValueError:
            logging.error("Invalid line format")

    return dictionary


def format_entry(name, number, comment):
    return f"{name}: {number}, {comment}"


def write_dictionary_to_file(lines_dict):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        data = "\n".join(f"{key}:{value[0]}:{value[1]}" for key, value in lines_dict.items())
        f.write(data + "\n")
    logging.info("Dictionary written to file")


def process_file():
    with open(FILE_NAME, "r+", encoding="utf-8") as file:
        lines_dict = map_lines_to_dictionary(file.readlines())
        while True:
            line = input().strip()
            if not line:
                logging.info("Empty line, breaking loop")
                break

            if line == "add":
                name = input("Enter name: ").strip()
                number = input("Enter number: ").strip()
                comment = input("Enter comment: ").strip()
                if name and number and comment and name not in lines_dict:
                    lines_dict[name] = (number, comment)
                    file.seek(0, os.SEEK_END)
                    file.write(f"{name}:{number}:{comment}\n")
                    file.flush()
                    logging.info(f"Added {format_entry(name, number, comment)}")
                else:
                    logging.info("No empty lines or duplicate names allowed")

            elif line == "edit":
                name = input("Enter name: ").strip()
                if name in lines_dict:
                    number = input("Enter new number: ").strip()
                    comment = input("Enter new comment: ").strip()
                    lines_dict[name] = (number, comment)
                    write_dictionary_to_file(lines_dict)
                    logging.info(f"Edited entry: {format_entry(name, number, comment)}")
                else:
                    logging.info("Name not found in dictionary")

            elif line == "del":
                name = input("Enter name: ").strip()
                if name in lines_dict:
                    number, comment = lines_dict.pop(name)
                    write_dictionary_to_file(lines_dict)
                    logging.info(f"Deleted entry: {format_entry(name, number, comment)}")
                else:
                    logging.info("Name not found in dictionary")

            elif line == "find":
                name = input("Enter name: ").strip()
                if name in lines_dict:
                    number, comment = lines_dict[name]
                    print(format_entry(name, number, comment))
                else:
                    logging.error("Name not found in dictionary")

            elif line == "all":
                for name, (number, comment) in lines_dict.items():
                    print(format_entry(name, number, comment))

            elif line == "exit":
                break
            else:
                print("Unknown command")


if __name__ == "__main__":
    process_file()
