#!/usr/bin/env python3
import os
import re
import shutil
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(prog="order", description="order files based on names")

parser.add_argument("-d", "--dir")
parser.add_argument("-s", "--string")
parser.add_argument("-r", "--regex")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()

class Order:
    def __init__(self, dir, string, regex):
        self.dir = dir
        self.string = string
        self.regex = regex
        self.matched = []
        pass

    def match(self):
        """
        Matches files in the specified directory based on the given string or regular expression.

        If a string is provided, it splits the string into words and searches for files that contain any of the words in their names.
        If a regular expression is provided, it searches for files that match the regular expression pattern.

        The matched files are stored in the `matched` list.

        Returns:
            None
        """
        if self.string:
            splits = self.string.lower().split()
            for root, _, files in os.walk(self.dir):
                for file in files:
                    for word in splits:
                        if word in file.lower():
                            full_path = os.path.join(root, file)
                            self.matched.append(full_path)
        elif self.regex:
            pattern = re.compile(self.regex)
            for root, _, files in os.walk(self.dir):
                for file in files:
                    if pattern.search(file):
                        full_path = os.path.join(root, file)
                        self.matched.append(full_path)

    def order(self):
        """
        Move files from the source directory to the destination directory.

        Args:
            self: The current instance of the class.

        Returns:
            None

        Raises:
            OSError: If there is an error moving the files.

        """

        cwd = os.getcwd()
        destination = os.path.join(cwd, self.string)
        source = self.dir

        try:
            os.makedirs(destination, exist_ok=True)
        except OSError as e:
            print(f"error creating destination directory: {e}")
            return
        
        for file in tqdm(self.matched, desc="moving files"):
            try:
                shutil.move(file, destination)
            except FileExistsError as e:
                continue
            except OSError as e:
                print(f"error moving {file} to {destination}: {e}")


if __name__ == "__main__":
    if(args.verbose):
        for arg in vars(args):
            print(arg, getattr(args, arg))

    obj = Order(args.dir, args.string, args.regex)
    obj.match()

    if len(obj.matched) > 0:
        obj.order()
    else:
        print("no files matching input!")

