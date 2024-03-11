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

