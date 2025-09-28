import math
import re


def insert_implicit_multiplication(expr: str) -> str:
    """
    Adds * where multiplication is implied in the math expression.
    """
    # Number followed by (
    expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
    # Number followed by π or e
    expr = re.sub(r'(\d)(π|e)', r'\1*\2', expr)
    # ) followed by number, (, π, or e
    expr = re.sub(r'(\))(\d|\(|π|e)', r'\1*\2', expr)
    # π or e followed by number, (, π, or e
    expr = re.sub(r'(π|e)(\d|\(|π|e)', r'\1*\2', expr)
    return expr


def evaluate(expression: str, angle_mode='deg') -> float | str:
    """
    Evaluates a mathematical expression safely.
    Replaces UI symbols (like √, ^) with proper math equivalents.
    Returns a float/int result or "Error" on failure.
    """
    if angle_mode == 'deg':
        # Safe math environment to evaluate expressions securely
        safe_env = {
            "__builtins__": None,  # Disable all Python built-ins for security
            "sin": lambda x: math.sin(math.radians(x)),  # Sine in degrees
            "cos": lambda x: math.cos(math.radians(x)),  # Cosine in degrees
            "tan": lambda x: math.tan(math.radians(x)),  # Tangent in degrees
            "sqrt": math.sqrt,  # Square root
            "ln": math.log,  # Natural logarithm
            "log": math.log10,  # Base-10 logarithm
            "π": math.pi,  # Pi constant
            "e": math.e,  # Euler's number
            "exp": math.exp,  # e^x
            "degrees": math.degrees,  # Toggle to degrees
            "radians": math.radians  # Toggle to radians
        }
    else:
        safe_env = {
            "__builtins__": None,  # Disable all Python built-ins for security
            "sin": lambda x: math.sin(x),  # Sine in degrees
            "cos": lambda x: math.cos(x),  # Cosine in degrees
            "tan": lambda x: math.tan(x),  # Tangent in degrees
            "sqrt": math.sqrt,  # Square root
            "ln": math.log,  # Natural logarithm
            "log": math.log10,  # Base-10 logarithm
            "π": math.pi,  # Pi constant
            "e": math.e,  # Euler's number
            "e^": math.exp,  # e^x
            "degrees": math.degrees,  # Toggle to degrees
            "radians": math.radians  # Toggle to radians
        }

    try:
        # Replace UI-specific symbols with Python equivalents
        expression = expression.replace('^', '**')    # e.g., 2^3 becomes 2**3
        expression = expression.replace('√', 'sqrt')  # e.g., √9 becomes sqrt(9)

        # Evaluate the expression using eval() with a restricted environment
        result = eval(expression, {"__builtins__": None}, safe_env)

        # If result is a number, return as int if whole, else round float
        if isinstance(result, (int, float)):
            if result.is_integer():
                return int(result)
            else:
                return round(result, 10)
        else:
            return "Error"

    except Exception:
        # Catch any error: syntax issues, divide by zero, etc.
        return "Error"


# Example usage (you can delete or comment this out in production)
if __name__ == '__main__':
    test_cases = [
        "2+2",               # 4
        "sqrt(25)+sin(0)",   # 5
        "ln(1)",            # 0
        "1/0",               # Error
        "5+(2*3",            # Error (unbalanced)
        "cos(180)",          # -1
        "sin(30)",           # 0.5
        "log(1000)"        # 3
    ]

    for expr in test_cases:
        print(f"{expr} = {evaluate(expr)}")
