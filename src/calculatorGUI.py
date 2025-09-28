from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QHBoxLayout,
)
from PyQt5.QtGui  import QFont
from PyQt5.QtCore import Qt
import sys
import math
from engine import insert_implicit_multiplication, evaluate


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator")
        self.setFixedSize(400, 625)
        self.input_str = ""  # string shown in display, e.g., "(9)+sin(0)"
        self.paren_balance = 0  # how many parentheses are currently open
        self.init_ui()  # call to function to initialize the ui of the app
        self.angle_mode = 'deg'  # default angle mode: degrees

    def init_ui(self):
        # Layout for display and buttons and history
        outer_layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        self.setStyleSheet("background-color: #ffeef8;")  # soft pink background

        # History list
        self.history = []

        # Display Area
        self.display = QLineEdit()  # Single-line display for input/result
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)  # Prevent typing directly
        # Coloring and Dimensions of Display Area
        self.display.setStyleSheet("""
            background-color: #fff0f5;    /* light lavender background */
            border: 2px solid #ffb3c6;    /* pastel pink border */
            border-radius: 10px;
            padding: 10px;
            font-size: 24px;
            color: #4b3b47;
            font-family: 'Comic Sans MS';
        """)
        main_layout.addWidget(self.display)

        # Buttons (Grid Layout)
        button_layout = QGridLayout()

        # Define all buttons with explicit (row, col) so we control placement
        buttons = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('^', 0, 3),
            ('log', 1, 0), ('e^', 1, 1), ('ln', 1, 2), ('√', 1, 3),
            ('π', 2, 0), ('e', 2, 1), ('(', 2, 2), (')', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('*', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2), ('/', 6, 3),
            ('deg', 7, 0), ('rad', 7, 1),
            ('C', 7, 2), ('CE', 7, 3)
        ]

        # Button coloring based on type of button
        def button_color(text):
            if text in {'sin', 'cos', 'tan', 'ln', '√', '^', 'e^', 'deg', 'rad', 'log'}:
                return "#ffeaa7"  # pastel yellow (scientific functions)
            elif text in {'/', '*', '-', '+', '(', ')'}:
                return "#ffb3c6"  # pastel pink (operators)
            elif text == '=':
                return "#c2f0c2"  # pastel green (equals)
            elif text in {'C', 'CE'}:
                return "#ff8fab"  # red/pink (clear buttons)
            else:
                return "#c2dfff"  # pastel blue (digits and constants)

        # Create buttons
        # Loop through each of the 3 elements of the tuple in the list
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(60, 40)
            # Sets the color of the button depending on the type of button
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {button_color(text)};
                    border-radius: 10px;
                    font-size: 18px;
                    font-family: 'Comic Sans MS';
                    color: #4b3b47;
                }}
                QPushButton:hover {{
                    background-color: #fcdff1;
                }}
            """)
            # This hooks the signal from button click to function
            # The lambda swallows the unused checked bool and captures the specific button label for that instance
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))
            button_layout.addWidget(button, row, col)  # Adds the button to the button layout object

        # --- History Layout ---
        self.history_list = QListWidget()


        main_layout.addLayout(button_layout)  # Adds the grid of buttons to the main layout object
        outer_layout.addLayout(main_layout, 3)
        outer_layout.addWidget(self.history_list, 1)
        self.setLayout(outer_layout)  # Sets the layout to be the main layout object

    # Button click logic
    def on_button_click(self, text: str):
        if text == "CE":
            self.backspace()  # delete char
        elif text == "C":
            self.clear()  # clear entire display
        elif text == '=':
            expr = insert_implicit_multiplication(self.input_str)
            result = evaluate(expr, angle_mode=self.angle_mode)
            # Evaluate the current expression string using your math engine
            self.display.setText(str(result))
            # Update the display with the result (whether it’s a number or "Error")
            self.input_str = str(result) if result != "Error" else ""
            # Save to history
            self.history.append((expr, result))
            self.update_history_display()
            return
        elif text in {'+', '-', '*', '/', '^'}:  # appends the operator to the string object
            self.append_operator(text)
        elif text == '.':  # appends the decimal to the string object
            self.append_decimal()
        elif text == '(':  # appends the left parentheses to the string object
            self.append_left_paren()
        elif text == ')':  # appends the right parentheses to the string object
            self.append_right_paren()
        elif text in {'sin', 'cos', 'tan', 'ln', 'log', '√', 'e^'}:  # appends the function to the string object
            self.append_function(text)
        elif text == 'deg':
            self.angle_mode = 'deg'  # Changes the mode to degrees
        elif text == 'rad':
            self.angle_mode = 'rad'  # Changes the mode to radians
        elif text == 'π':
            self.append_symbol('π')  # appends pi to the string object
        elif text == 'e':
            self.append_symbol('e')  # appends Euler's number to the string object
        else:
            # appends digits 0..9
            self.append_digit(text)

        # update the current buffer to display
        self.display.setText(self.input_str)

    # Helper to update the history display
    def update_history_display(self):
        self.history_list.clear()
        font = QFont("Comic Sans MS", 10)
        self.history_list.setFont(font)
        for expr, res in self.history:
            self.history_list.addItem(f"{expr} = {res}")

    # Helper Functions to allow the button clicks to properly make the calculator function
    # Helper Function to clear the display/text
    def clear(self):
        self.input_str = ""  # Clears the string
        self.paren_balance = 0  # Sets the number of unbalanced parentheses to 0

    # Helper Function to delete a single character/function/digit/operation
    def backspace(self):
        if not self.input_str:
            return

        # Checks if the string ends with a function name + "("
        for func in ('sin', 'cos', 'tan', 'log', 'ln'):
            token = func + '('
            if self.input_str.endswith(token):
                # If the string does end with it, it deletes that function and parentheses from the string
                self.input_str = self.input_str[:-len(token)]
                # Adjusts the unbalanced parentheses amount to decrease it by 1, and cap it at 0 for the lowest
                self.paren_balance = max(0, self.paren_balance - 1)
                return

        # Checks if the string ends with a "√("
        if self.input_str.endswith("√("):
            self.input_str = self.input_str[:-2]  # Deletes √("
            # Adjusts the unbalanced parentheses amount to decrease it by 1, and cap it at 0 for the lowest
            self.paren_balance = max(0, self.paren_balance - 1)
            return

        # Otherwise remove one char; adjust paren balance if needed
        last = self.input_str[-1]
        self.input_str = self.input_str[:-1]
        if last == '(':
            self.paren_balance = max(0, self.paren_balance - 1)
        elif last == ')':
            self.paren_balance += 1  # we removed a right paren, so one more left paren is now unmatched

    # Helper function to append a single digit
    def append_digit(self, d: str):
        self.input_str += d

    # Helper function to append a decimal
    def append_decimal(self):
        # current_numeric_token() returns the most recent numeric value
        # Ex: 3.14 + 2 returns 2 || 3.14 + 2. it returns 2.

        token = self._current_numeric_token()
        # Only allow one decimal per current number token
        if '.' in token:
            return
        # If token is empty (like at start or after operator or (), prepend a 0 before decimal)
        if token == "":
            self.input_str += "0"
        self.input_str += "."

    # Helper function to append an operator
    def append_operator(self, op: str):
        if not self.input_str:
            # Allow unary minus/negative sign at start
            if op == '-':
                self.input_str += '-'
            return
        last = self.input_str[-1]
        if last in '+-*/^(':
            # Replace previous operator
            if not (last == '(' and op == '-'):  # allow "(-" for negative numbers
                self.input_str = self.input_str[:-1] + op
                return
        if last == '.':
            # Remove dangling decimal/dot before appending operator
            self.input_str = self.input_str[:-1]
        self.input_str += op

    # Helper functions to append parentheses
    # Left Parentheses Helper
    def append_left_paren(self):
        # Can also make it so after a number or ')', you *may* want to imply multiplication; Phase 5 can add that.
        self.input_str += '('
        self.paren_balance += 1  # Increments the number of unbalanced parentheses by 1

    # Right Parentheses Helper
    def append_right_paren(self):
        if self.paren_balance <= 0:
            return  # no matching '(' so it does not add right parentheses
        if not self.input_str:
            return  # if empty string, don't add right parentheses
        last = self.input_str[-1]
        # Makes it so "())" or operator right before ')' isn't allowed
        if last in '+-*/^(':
            return
        self.input_str += ')'
        self.paren_balance -= 1  # Since a right parentheses was added, the number of unbalanced parentheses decreases

    # Helper to append math/trig functions
    def append_function(self, name: str):
        """
        Append a function and an opening paren.
        sin  -> "sin("
        cos  -> "cos("
        tan  -> "tan("
        log  -> "log("
        √    -> "√("
        """
        if name == '√':
            self.input_str += '√('
        else:
            self.input_str += f'{name}('
        self.paren_balance += 1  # Increment the number of unbalanced parentheses by 1

    # Helper to append pi and e
    def append_symbol(self, name: str):
        if name == 'π':
            self.input_str += 'π'
        elif name == 'e':
            self.input_str += 'π'

    # Helper used to check most recent numeric value or token the user is entering
    def _current_numeric_token(self) -> str:

        # Return the number chunk the user is currently typing.

        if not self.input_str:  # If string is empty just return empty string
            return ""
        i = len(self.input_str) - 1  # Sets i to the index of the last character of the string
        # Stop when we hit an operator or a parenthesis
        # Loop decreases i by 1 until it hits an operator/parenthesis or until it reaches the first character
        while i >= 0 and self.input_str[i] not in '+-*/^()':
            # Also stop if we hit the end of a function name
            i -= 1
        return self.input_str[i + 1:]  # Returns the string starting 1 plus the index stored in i


# Main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
