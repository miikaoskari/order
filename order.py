#!/usr/bin/env python3
import os
import re
import shutil
import argparse

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
            splits = self.string.split()
            for _, _, files in os.walk(self.dir):
                for file in files:
                    for word in splits:
                        if word in file:
                            self.matched.append(file)
        elif self.regex:
            pattern = re.compile(self.regex)
            for _, _, files in os.walk(self.dir):
                for file in files:
                    if pattern.search(file):
                        self.matched.append(file)

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
        destination = self.string
        source = self.dir
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        for file in self.matched:
            source_path = os.path.join(source, file)
            destination_path = os.path.join(destination, file)
            try:
                shutil.move(source_path, destination_path)
            except OSError as e:
                print(f"error moving {source_path} to {destination_path}: {e}")

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

