"""
Activity 5 – File Handling Programs (OOP Implementation, Interactive P3)
Author : [Your Name]
Date   : April 2026

This script fulfils the requirements for Module 2, pages 17‑18:
  P1 – Extract even/odd numbers from numbers.txt
  P2 – Find student with highest GWA from students.txt
  P3 – **Interactive multi‑line input** that writes to mylife.txt
        (user types lines, confirms continuation, just like the sample)
  P4 – Compute squares (evens) and cubes (odds) from integers.txt

Design principles:
  * Pure Object‑Oriented structure with abstract base classes
  * Separation of concerns (UI, file I/O, data processing)
  * Robust error handling and input validation
  * Human‑readable comments, no emojis, no external libraries
  * P3 now uses live terminal interaction instead of hard‑coded story
"""

import os
import sys
import time
import random
import logging
import io
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

# Force UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ─── ANSI colour constants ────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
BLACK  = "\033[30m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
WHITE  = "\033[97m"

# ─── Logging configuration ────────────────────────────────────────────────────
logging.basicConfig(
    filename="activity5.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ─── Terminal UI class ───────────────────────────────────────────────────────

class Terminal:
    """Handles all terminal output formatting and interaction."""
    
    @staticmethod
    def clear():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def pause(seconds=0.03):
        """Sleep for a given number of seconds."""
        time.sleep(seconds)
    
    @staticmethod
    def banner():
        """Display the program banner with typewriter effect."""
        Terminal.clear()
        lines = [
            "  ███████╗██╗██╗     ███████╗    ████████╗ ██████╗  ██████╗ ██╗      ",
            "  ██╔════╝██║██║     ██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║      ",
            "  █████╗  ██║██║     █████╗         ██║   ██║   ██║██║   ██║██║      ",
            "  ██╔══╝  ██║██║     ██╔══╝         ██║   ██║   ██║██║   ██║██║      ",
            "  ██║     ██║███████╗███████╗        ██║   ╚██████╔╝╚██████╔╝███████╗ ",
            "  ╚═╝     ╚═╝╚══════╝╚══════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝ ",
        ]
        print()
        for line in lines:
            print(f"{CYAN}{BOLD}", end="")
            for ch in line:
                print(ch, end="", flush=True)
                Terminal.pause(0.001)
            print(RESET)
        
        print(f"\n  {DIM}{WHITE}Activity 5 - File Handling Programs  |  Module 2 Pages 17-18{RESET}")
        print(f"  {DIM}{'─' * 65}{RESET}\n")
    
    @staticmethod
    def header(title, color=CYAN):
        """Print a formatted header."""
        width = 60
        print(f"\n{color}{BOLD}  {'─' * width}")
        print(f"  {title.center(width)}")
        print(f"  {'─' * width}{RESET}\n")
    
    @staticmethod
    def success(msg):
        """Print a success message."""
        print(f"  {GREEN}{BOLD}[  OK  ]{RESET}  {msg}")
    
    @staticmethod
    def info(msg):
        """Print an info message."""
        print(f"  {CYAN}{BOLD}[ INFO ]{RESET}  {msg}")
    
    @staticmethod
    def warn(msg):
        """Print a warning message."""
        print(f"  {YELLOW}{BOLD}[ WARN ]{RESET}  {msg}")
    
    @staticmethod
    def error(msg):
        """Print an error message."""
        print(f"  {RED}{BOLD}[ FAIL ]{RESET}  {msg}")
    
    @staticmethod
    def row(label, value, label_color=WHITE, value_color=GREEN):
        """Print a labeled row."""
        print(f"  {label_color}{label:<28}{RESET}  {value_color}{BOLD}{value}{RESET}")
    
    @staticmethod
    def divider(color=DIM):
        """Print a horizontal divider."""
        print(f"  {color}{'─' * 60}{RESET}")
    
    @staticmethod
    def loading(label="Processing"):
        """Show a loading animation."""
        frames = ["[=        ]", "[==       ]", "[===      ]", "[====     ]",
                  "[=====    ]", "[======   ]", "[=======  ]", "[======== ]", "[=========]"]
        for frame in frames:
            print(f"\r  {CYAN}{label}  {frame}{RESET}", end="", flush=True)
            time.sleep(0.05)
        print(f"\r  {GREEN}Done!{RESET}                              ")
    
    @staticmethod
    def press_enter():
        """Prompt user to press Enter."""
        print(f"\n  {DIM}Press Enter to go back to the menu...{RESET}", end="")
        input()


# ─── Abstract base classes ────────────────────────────────────────────────────

class FileGenerator(ABC):
    """Abstract base class for file generators."""
    
    def __init__(self, filename: str):
        self.filename = filename
    
    @abstractmethod
    def generate(self):
        """Generate and write the file."""
        pass


class Program(ABC):
    """Abstract base class for programs."""
    
    @abstractmethod
    def run(self):
        """Run the program."""
        pass


# ─── Program 1: Even / Odd Sorter ────────────────────────────────────────────

class NumberFileGenerator(FileGenerator):
    """Generates numbers.txt with random integers."""
    
    def generate(self):
        numbers = random.sample(range(-50, 101), 20)
        with open(self.filename, 'w') as f:
            for n in numbers:
                f.write(f"{n}\n")
        Terminal.success(f"Generated {self.filename} with 20 random integers.")
        logger.info(f"Generated {self.filename}")
        return numbers


class NumberSorter(Program):
    """Reads numbers and sorts them into even/odd files."""
    
    def __init__(self, source="numbers.txt"):
        self.source = source
        self.numbers = []
        self.evens = []
        self.odds = []
    
    def read(self):
        """Read numbers from source file."""
        with open(self.source, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.numbers.append(int(line))
        logger.info(f"Read {len(self.numbers)} numbers from {self.source}")
    
    def sort(self):
        """Partition numbers into even and odd lists."""
        for n in self.numbers:
            (self.evens if n % 2 == 0 else self.odds).append(n)
    
    def write_output(self):
        """Write results to even.txt and odd.txt."""
        with open("even.txt", 'w') as f:
            f.write("Even Numbers\n")
            f.write("=" * 25 + "\n")
            for n in self.evens:
                f.write(f"{n}\n")
            f.write(f"\nCount: {len(self.evens)}\n")
        
        with open("odd.txt", 'w') as f:
            f.write("Odd Numbers\n")
            f.write("=" * 25 + "\n")
            for n in self.odds:
                f.write(f"{n}\n")
            f.write(f"\nCount: {len(self.odds)}\n")
        
        logger.info(f"Wrote {len(self.evens)} evens and {len(self.odds)} odds")
    
    def display(self):
        """Display the results in the terminal."""
        Terminal.header("P-1  |  Even and Odd Number Sorter", CYAN)
        
        Terminal.info(f"Read {len(self.numbers)} integers from {self.source}")
        Terminal.divider()
        print()
        
        cols = 10
        print(f"  {DIM}All numbers:{RESET}")
        for i, n in enumerate(self.numbers):
            color = GREEN if n % 2 == 0 else YELLOW
            print(f"  {color}{BOLD}{n:>6}{RESET}", end="")
            if (i + 1) % cols == 0:
                print()
        print("\n")
        Terminal.divider()
        
        print(f"\n  {GREEN}{BOLD}Even Numbers  -->  even.txt{RESET}")
        print(f"  {DIM}{'─' * 30}{RESET}")
        print(f"  {DIM}{'#':<6}{'Number':>8}{RESET}")
        for i, n in enumerate(self.evens, 1):
            print(f"  {WHITE}{i:<6}{GREEN}{BOLD}{n:>8}{RESET}")
        print(f"\n  {DIM}Total: {len(self.evens)} even numbers{RESET}")
        
        print(f"\n  {YELLOW}{BOLD}Odd Numbers   -->  odd.txt{RESET}")
        print(f"  {DIM}{'─' * 30}{RESET}")
        print(f"  {DIM}{'#':<6}{'Number':>8}{RESET}")
        for i, n in enumerate(self.odds, 1):
            print(f"  {WHITE}{i:<6}{YELLOW}{BOLD}{n:>8}{RESET}")
        print(f"\n  {DIM}Total: {len(self.odds)} odd numbers{RESET}")
        
        Terminal.divider()
        Terminal.success("even.txt and odd.txt written successfully.")
    
    def run(self):
        """Execute the program."""
        setup = NumberFileGenerator("numbers.txt")
        setup.generate()
        Terminal.loading("Sorting numbers")
        self.read()
        self.sort()
        self.write_output()
        self.display()


# ─── Program 2: Highest GWA Finder ───────────────────────────────────────────

class Student:
    """Represents a student record with name and GWA."""
    
    def __init__(self, name: str, gwa: float):
        self.name = name
        self.gwa = float(gwa)


class StudentFileGenerator(FileGenerator):
    """Generates students.txt with student records."""
    
    def generate(self):
        records = [
            ("Juan dela Cruz", 1.50), ("Maria Santos", 1.25),
            ("Carlo Reyes", 1.75),    ("Ana Gonzales", 1.00),
            ("Nico Bautista", 2.00),  ("Liza Mendoza", 1.50),
            ("Ryan Torres", 1.25),    ("Claire Villanueva", 1.75),
            ("Mark Ramos", 2.25),     ("Jenny Flores", 1.50),
            ("James Castillo", 1.00), ("Rachel Aquino", 2.50),
            ("Paolo Aguilar", 1.25),  ("Trish Morales", 1.75),
            ("Kevin Dela Pena", 1.50),("Sophia Navarro", 1.00),
            ("Andrei Lim", 2.00),     ("Camille Cruz", 1.75),
            ("Ethan Ong", 1.25),      ("Dana Pascual", 1.50),
        ]
        with open(self.filename, 'w') as f:
            for name, gwa in records:
                f.write(f"{name}, {gwa}\n")
        Terminal.success(f"Generated {self.filename} with 20 students.")
        logger.info(f"Generated {self.filename}")


class GWAChecker(Program):
    """Finds the student with the highest GWA."""
    
    def __init__(self, source="students.txt"):
        self.source = source
        self.students: List[Student] = []
    
    def load(self):
        """Load student records from file."""
        with open(self.source, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 2:
                    self.students.append(Student(parts[0].strip(), parts[1].strip()))
        logger.info(f"Loaded {len(self.students)} student records")
    
    def get_top(self) -> Student:
        """Return the student with the highest GWA (lowest numeric value)."""
        return min(self.students, key=lambda s: s.gwa)
    
    def display(self):
        """Display the results in the terminal."""
        Terminal.header("P-2  |  Highest GWA Finder", CYAN)
        Terminal.info(f"Loaded {len(self.students)} student records from {self.source}")
        print()
        
        sorted_students = sorted(self.students, key=lambda s: s.gwa)
        top = sorted_students[0]
        
        print(f"  {DIM}{'Rank':<6}{'Name':<26}{'GWA':>6}  {'Status'}{RESET}")
        Terminal.divider()
        
        for rank, student in enumerate(sorted_students, 1):
            if rank == 1:
                bar = f"{GREEN}{BOLD}  <<  TOP STUDENT{RESET}"
                name_color = GREEN
            elif rank <= 3:
                bar = f"{YELLOW}  --  Top 3{RESET}"
                name_color = YELLOW
            else:
                bar = ""
                name_color = WHITE
            
            gwa_color = GREEN if student.gwa <= 1.25 else (YELLOW if student.gwa <= 1.75 else RED)
            print(f"  {DIM}{rank:<6}{RESET}{name_color}{student.name:<26}{RESET}"
                  f"{gwa_color}{BOLD}{student.gwa:>6.2f}{RESET}{bar}")
        
        Terminal.divider()
        print(f"\n  {CYAN}{BOLD}Result:{RESET}")
        print(f"\n  {GREEN}{BOLD}  {top.name}{RESET}  {DIM}has the highest GWA of{RESET}  "
              f"{GREEN}{BOLD}{top.gwa:.2f}{RESET}\n")
    
    def run(self):
        """Execute the program."""
        setup = StudentFileGenerator("students.txt")
        setup.generate()
        Terminal.loading("Analyzing GWA records")
        self.load()
        self.display()


# ─── Program 3: My Life Writer (Interactive) ─────────────────────────────────

class MyLifeWriter(Program):
    """Interactive program that collects user input and writes to mylife.txt."""
    
    def __init__(self, filename="mylife.txt"):
        self.filename = filename
        self.sections = []
    
    def collect_input(self):
        """Collect multi-line input from the user interactively."""
        Terminal.clear()
        Terminal.header("P-3  |  My Life Writer  (Interactive)", CYAN)
        
        print(f"  {CYAN}{BOLD}Instructions:{RESET}")
        print(f"  {WHITE}Enter sections of your life story. For each section:")
        print(f"    1. Enter the section title")
        print(f"    2. Enter lines of text (empty line to finish)")
        print(f"    3. Confirm if you want to add another section{RESET}\n")
        
        Terminal.divider()
        
        while True:
            section_title = input(f"\n  {CYAN}Section title (or 'done' to finish): {RESET}").strip()
            if section_title.lower() == 'done':
                break
            
            if not section_title:
                Terminal.warn("Please enter a section title.")
                continue
            
            lines = []
            print(f"  {WHITE}Enter lines for '{section_title}' (empty line to finish):{RESET}")
            while True:
                line = input(f"  {DIM}> {RESET}").strip()
                if not line:
                    break
                lines.append(line)
            
            if lines:
                self.sections.append((section_title, lines))
                Terminal.success(f"Added section: {section_title}")
            else:
                Terminal.warn("No lines entered for this section.")
            
            cont = input(f"\n  {CYAN}Add another section? (yes/no): {RESET}").strip().lower()
            if cont not in ['yes', 'y']:
                break
    
    def write(self):
        """Write collected sections to mylife.txt."""
        with open(self.filename, 'w') as f:
            f.write("MY LIFE\n")
            f.write("=" * 50 + "\n\n")
            for section_title, lines in self.sections:
                f.write(f"[ {section_title} ]\n")
                f.write("-" * 30 + "\n")
                for line in lines:
                    f.write(f"  {line}\n")
                f.write("\n")
            f.write("=" * 50 + "\n")
            f.write("End of story. For now.\n")
        logger.info(f"Wrote {len(self.sections)} sections to {self.filename}")
    
    def display(self):
        """Display the story in the terminal."""
        Terminal.header("P-3  |  My Life  (mylife.txt)", CYAN)
        
        for section_title, lines in self.sections:
            print(f"  {CYAN}{BOLD}[ {section_title} ]{RESET}")
            print(f"  {DIM}{'─' * 35}{RESET}")
            for line in lines:
                print(f"  {WHITE}{line}{RESET}")
            print()
        
        Terminal.divider()
        Terminal.success(f"Written to {self.filename}")
    
    def run(self):
        """Execute the program."""
        self.collect_input()
        if not self.sections:
            Terminal.warn("No sections entered.")
            return
        
        Terminal.loading("Writing story to file")
        self.write()
        self.display()


# ─── Program 4: Square / Cube Generator ──────────────────────────────────────

class IntegerFileGenerator(FileGenerator):
    """Generates integers.txt with random integers."""
    
    def generate(self):
        numbers = random.sample(range(1, 51), 20)
        with open(self.filename, 'w') as f:
            for n in numbers:
                f.write(f"{n}\n")
        Terminal.success(f"Generated {self.filename} with 20 integers.")
        logger.info(f"Generated {self.filename}")


class IntegerProcessor(Program):
    """Reads integers and computes squares (evens) and cubes (odds)."""
    
    def __init__(self, source="integers.txt"):
        self.source = source
        self.integers = []
        self.even_results = []
        self.odd_results = []
    
    def read(self):
        """Read integers from source file."""
        with open(self.source, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.integers.append(int(line))
        logger.info(f"Read {len(self.integers)} integers from {self.source}")
    
    def process(self):
        """Process integers: square even numbers, cube odd numbers."""
        for n in self.integers:
            if n % 2 == 0:
                self.even_results.append((n, n ** 2))
            else:
                self.odd_results.append((n, n ** 3))
    
    def write_output(self):
        """Write results to double.txt and triple.txt."""
        with open("double.txt", 'w') as f:
            f.write("Square of Even Numbers\n")
            f.write("=" * 30 + "\n")
            f.write(f"{'Original':<15}{'Squared'}\n")
            f.write("-" * 30 + "\n")
            for original, result in self.even_results:
                f.write(f"{original:<15}{result}\n")
            f.write(f"\nTotal: {len(self.even_results)} entries\n")
        
        with open("triple.txt", 'w') as f:
            f.write("Cube of Odd Numbers\n")
            f.write("=" * 30 + "\n")
            f.write(f"{'Original':<15}{'Cubed'}\n")
            f.write("-" * 30 + "\n")
            for original, result in self.odd_results:
                f.write(f"{original:<15}{result}\n")
            f.write(f"\nTotal: {len(self.odd_results)} entries\n")
        
        logger.info(f"Wrote {len(self.even_results)} squares and {len(self.odd_results)} cubes")
    
    def display(self):
        """Display the results in the terminal."""
        Terminal.header("P-4  |  Square and Cube Generator", CYAN)
        Terminal.info(f"Read {len(self.integers)} integers from {self.source}")
        print()
        
        print(f"  {GREEN}{BOLD}{'Even  ->  double.txt':<32}{RESET}  "
              f"{YELLOW}{BOLD}Odd  ->  triple.txt{RESET}")
        print(f"  {DIM}{'─' * 30}  {'─' * 28}{RESET}")
        print(f"  {DIM}{'Num':<8}{'Squared':<22}  {'Num':<8}{'Cubed'}{RESET}")
        
        max_len = max(len(self.even_results), len(self.odd_results))
        even_pad = [(None, None)] * (max_len - len(self.even_results))
        odd_pad  = [(None, None)] * (max_len - len(self.odd_results))
        
        for (e_orig, e_sq), (o_orig, o_cu) in zip(
            self.even_results + even_pad,
            self.odd_results + odd_pad
        ):
            left  = f"{GREEN}{e_orig:<8}{BOLD}{e_sq:<22}{RESET}" if e_orig is not None else " " * 30
            right = f"{YELLOW}{o_orig:<8}{BOLD}{o_cu}{RESET}"   if o_orig is not None else ""
            print(f"  {left}  {right}")
        
        print()
        Terminal.divider()
        Terminal.success("double.txt and triple.txt written successfully.")
    
    def run(self):
        """Execute the program."""
        setup = IntegerFileGenerator("integers.txt")
        setup.generate()
        Terminal.loading("Computing squares and cubes")
        self.read()
        self.process()
        self.write_output()
        self.display()


# ─── Main Application ────────────────────────────────────────────────────────

class App:
    """Main application with interactive menu."""
    
    def __init__(self):
        self.programs = {
            "1": ("Even / Odd Sorter       [ even.txt   |  odd.txt ]",    NumberSorter),
            "2": ("Highest GWA Finder      [ students.txt ]",              GWAChecker),
            "3": ("My Life Writer (Interactive) [ mylife.txt ]",           MyLifeWriter),
            "4": ("Square and Cube         [ double.txt |  triple.txt ]",  IntegerProcessor),
            "5": ("Run All Programs",                                       None),
        }
    
    def menu(self):
        """Display the menu and get user choice."""
        Terminal.banner()
        print(f"  {CYAN}{BOLD}Select a program to run:{RESET}\n")
        for key, (label, _) in self.programs.items():
            bullet = f"{CYAN}{BOLD}[{key}]{RESET}"
            if key == "5":
                print(f"  {bullet}  {YELLOW}{BOLD}{label}{RESET}")
            else:
                print(f"  {bullet}  {WHITE}{label}{RESET}")
        print(f"\n  {BOLD}[0]{RESET}  {DIM}Exit{RESET}")
        print()
        Terminal.divider()
        choice = input(f"\n  {CYAN}>{RESET} ").strip()
        return choice
    
    def run_program(self, key):
        """Run a specific program."""
        Terminal.clear()
        if key == "5":
            for k in ["1", "2", "3", "4"]:
                _, program_class = self.programs[k]
                program_class().run()
                print()
            Terminal.success("All programs finished.")
        else:
            _, program_class = self.programs[key]
            program_class().run()
    
    def run(self):
        """Main application loop."""
        while True:
            choice = self.menu()
            if choice == "0":
                Terminal.clear()
                print(f"\n  {CYAN}Goodbye.{RESET}\n")
                sys.exit(0)
            elif choice in self.programs:
                self.run_program(choice)
                Terminal.press_enter()
            else:
                Terminal.warn("Invalid choice. Try again.")
                time.sleep(1)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        App().run()
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}Interrupted.{RESET}\n")
        sys.exit(0)
