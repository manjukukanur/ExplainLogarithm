import numpy as np
import streamlit as st

def log_base(x, base):
    """
    Calculate the logarithm of x with a given base.
    
    Args:
        x: The value to find the logarithm of
        base: The base of the logarithm
        
    Returns:
        The logarithm value
    """
    if x <= 0:
        return None
    
    if base <= 0 or base == 1:
        return None
        
    # Use change of base formula
    if base == np.e:
        return np.log(x)
    elif base == 10:
        return np.log10(x)
    elif base == 2:
        return np.log2(x)
    else:
        return np.log(x) / np.log(base)

def explain_log_calculation(x, base):
    """
    Provide a step-by-step explanation of a logarithm calculation.
    
    Args:
        x: The value to find the logarithm of
        base: The base of the logarithm
        
    Returns:
        A string with the step-by-step explanation
    """
    if x <= 0:
        return f"Error: Cannot compute logarithm of {x} because logarithms are only defined for positive numbers."
    
    if base <= 0:
        return f"Error: Cannot use {base} as logarithm base because the base must be positive."
    
    if base == 1:
        return f"Error: Cannot use 1 as logarithm base because it would lead to division by zero in the logarithm formula."
    
    result = log_base(x, base)
    
    # Format based on common bases
    if base == 10:
        base_name = "common logarithm (base 10)"
        notation = f"log({x})"
    elif base == np.e:
        base_name = "natural logarithm (base e)"
        notation = f"ln({x})"
    elif base == 2:
        base_name = "binary logarithm (base 2)"
        notation = f"log₂({x})"
    else:
        base_name = f"logarithm base {base}"
        notation = f"log_{base}({x})"
    
    explanation = f"""
    **Step-by-step calculation of {notation}:**
    
    1. The {base_name} asks: "To what power must {base} be raised to get {x}?"
    
    2. In other words, we're solving for y in the equation:
       {base}^y = {x}
    
    3. Using logarithm rules, the answer is y = {result:.6f}
    
    4. This means {base}^{result:.6f} = {x}
    
    5. We can verify this: {base}^{result:.6f} = {base ** result:.6f} ≈ {x}
    """
    
    return explanation

def solve_logarithmic_equation(equation_type, parameters):
    """
    Solve various types of logarithmic equations.
    
    Args:
        equation_type: The type of equation to solve
        parameters: Dictionary of parameters for the equation
        
    Returns:
        Solution and explanation
    """
    if equation_type == "log_x_equals_k":
        # Solving log_b(x) = k for x
        base = parameters.get("base", 10)
        k = parameters.get("k", 1)
        
        if base <= 0 or base == 1:
            return None, "Error: Base must be positive and not equal to 1."
        
        solution = base ** k
        
        if base == 10:
            equation = f"log(x) = {k}"
        elif base == np.e:
            equation = f"ln(x) = {k}"
        elif base == 2:
            equation = f"log₂(x) = {k}"
        else:
            equation = f"log_{base}(x) = {k}"
        
        explanation = f"""
        **Solving {equation}:**
        
        1. We need to find x such that log_{base}(x) = {k}
        
        2. Using the definition of logarithms, if log_{base}(x) = {k}, then {base}^{k} = x
        
        3. Therefore, x = {base}^{k} = {solution}
        """
        
        return solution, explanation
    
    elif equation_type == "log_k_equals_x":
        # Solving log_b(k) = x for b
        k = parameters.get("k", 10)
        x = parameters.get("x", 1)
        
        if k <= 0:
            return None, "Error: The value inside the logarithm must be positive."
        
        if x == 0:
            return k, f"If log_b({k}) = 0, then b^0 = {k}, which is only true if {k} = 1."
        
        solution = k ** (1/x)
        
        equation = f"log_b({k}) = {x}"
        
        explanation = f"""
        **Solving {equation} for b:**
        
        1. We need to find the base b such that log_b({k}) = {x}
        
        2. Using the definition of logarithms, if log_b({k}) = {x}, then b^{x} = {k}
        
        3. To solve for b, we raise both sides to the power of 1/{x}
           b = {k}^(1/{x}) = {solution}
        """
        
        return solution, explanation
    
    elif equation_type == "compound_interest":
        # Solving for time in compound interest formula
        principal = parameters.get("principal", 1000)
        rate = parameters.get("rate", 0.05)
        target = parameters.get("target", 2000)
        
        if principal <= 0 or target <= 0:
            return None, "Error: Principal and target amounts must be positive."
        
        if rate <= -1:
            return None, "Error: Rate cannot be less than or equal to -100%."
            
        if rate == 0:
            if principal == target:
                return 0, "With 0% interest rate, the amount remains constant."
            else:
                return None, "With 0% interest rate, the principal will never reach the target."
        
        # Using the formula A = P(1+r)^t, solve for t
        ratio = target / principal
        solution = np.log(ratio) / np.log(1 + rate)
        
        explanation = f"""
        **Solving for time to grow from ${principal} to ${target} at {rate*100}% interest:**
        
        1. We use the compound interest formula: A = P(1+r)^t
           Where:
           - A = ${target} (final amount)
           - P = ${principal} (principal)
           - r = {rate} (interest rate)
           - t = time (what we're solving for)
        
        2. Divide both sides by P:
           A/P = (1+r)^t
           {target}/{principal} = (1+{rate})^t
           {ratio} = {1+rate}^t
        
        3. Take the logarithm of both sides:
           log({ratio}) = t * log({1+rate})
        
        4. Solve for t:
           t = log({ratio}) / log({1+rate})
           t = {np.log(ratio)} / {np.log(1+rate)}
           t = {solution} years
        """
        
        return solution, explanation
    
    return None, "Equation type not supported."

def generate_quiz_question(difficulty="medium"):
    """
    Generate a quiz question about logarithms.
    
    Args:
        difficulty: The difficulty level of the question
        
    Returns:
        Dictionary with question, options, correct answer, and explanation
    """
    np.random.seed(None)  # Ensure randomness
    
    if difficulty == "easy":
        # Simple logarithm evaluation or property identification
        question_types = [
            "evaluate_basic_log",
            "identify_property",
            "basic_equation"
        ]
    elif difficulty == "medium":
        # Application, moderate equations, or applying properties
        question_types = [
            "apply_property",
            "moderate_equation",
            "application"
        ]
    else:  # hard
        # Complex problems, real-world applications, multi-step
        question_types = [
            "complex_equation",
            "real_world",
            "multi_step"
        ]
    
    question_type = np.random.choice(question_types)
    
    if question_type == "evaluate_basic_log":
        # Generate a question to evaluate a basic logarithm
        base = np.random.choice([2, 10, np.e])
        exponent = np.random.randint(1, 6)
        value = base ** exponent
        
        if base == 10:
            base_notation = "log"
            base_name = "base 10"
        elif base == np.e:
            base_notation = "ln"
            base_name = "base e"
        else:
            base_notation = f"log_{base}"
            base_name = f"base {base}"
        
        question = f"What is the value of {base_notation}({value})?"
        correct_answer = exponent
        
        # Generate wrong options
        options = [exponent]
        while len(options) < 4:
            wrong = exponent + np.random.choice([-2, -1, 1, 2])
            if wrong not in options and wrong > 0:
                options.append(wrong)
        
        np.random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        explanation = f"""
        To find {base_notation}({value}), we need to determine what power of {base} equals {value}.
        
        Since {base}^{exponent} = {value}, we have {base_notation}({value}) = {exponent}.
        """
        
        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation
        }
    
    elif question_type == "identify_property":
        # Generate a question about logarithm properties
        properties = [
            {
                "name": "Product Rule",
                "formula": "log(x × y) = log(x) + log(y)",
                "example": f"log(8 × 4) = log(8) + log(4) = 3 + 2 = 5"
            },
            {
                "name": "Quotient Rule",
                "formula": "log(x ÷ y) = log(x) - log(y)",
                "example": f"log(32 ÷ 8) = log(32) - log(8) = 5 - 3 = 2"
            },
            {
                "name": "Power Rule",
                "formula": "log(x^n) = n × log(x)",
                "example": f"log(4^3) = 3 × log(4) = 3 × 2 = 6"
            },
            {
                "name": "Zero Property",
                "formula": "log(1) = 0",
                "example": f"log(1) = 0 because 10^0 = 1"
            }
        ]
        
        selected_property = np.random.choice(properties)
        
        question = f"Which logarithm property is represented by the formula: {selected_property['formula']}?"
        correct_answer = selected_property['name']
        
        # Generate options (all property names)
        options = [prop["name"] for prop in properties]
        np.random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        explanation = f"""
        The formula {selected_property['formula']} represents the {selected_property['name']}.
        
        Example: {selected_property['example']}
        """
        
        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation
        }
    
    elif question_type == "basic_equation":
        # Generate a simple logarithmic equation
        base = np.random.choice([2, 10])
        exponent = np.random.randint(1, 4)
        
        if base == 10:
            base_notation = "log"
        else:
            base_notation = f"log_{base}"
        
        question = f"Solve for x: {base_notation}(x) = {exponent}"
        correct_answer = base ** exponent
        
        # Generate wrong options
        options = [correct_answer]
        while len(options) < 4:
            wrong = correct_answer * np.random.choice([0.5, 0.9, 1.1, 2])
            wrong = round(wrong)
            if wrong not in options and wrong > 0:
                options.append(wrong)
        
        np.random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        explanation = f"""
        To solve {base_notation}(x) = {exponent}, we need to find what value of x gives us {exponent} when we take the logarithm base {base}.
        
        Using the definition of logarithms, if {base_notation}(x) = {exponent}, then x = {base}^{exponent}.
        
        Therefore, x = {base}^{exponent} = {correct_answer}.
        """
        
        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation
        }
    
    elif question_type == "apply_property":
        # Generate a problem applying logarithm properties
        x = np.random.randint(2, 10)
        y = np.random.randint(2, 10)
        
        operations = [
            f"log({x} × {y})",
            f"log({x*y} ÷ {y})",
            f"log({x}^{y})",
            f"log(√{x*x})"
        ]
        
        answers = [
            f"log({x}) + log({y})",
            f"log({x*y}) - log({y})",
            f"{y} × log({x})",
            f"log({x*x}) ÷ 2"
        ]
        
        results = [
            np.log10(x) + np.log10(y),
            np.log10(x),
            y * np.log10(x),
            np.log10(x)
        ]
        
        idx = np.random.randint(0, len(operations))
        
        question = f"Simplify the expression: {operations[idx]}"
        correct_answer = answers[idx]
        
        # Generate options (one correct, others wrong)
        wrong_answers = []
        for i in range(len(answers)):
            if i != idx:
                wrong_answers.append(answers[i])
        
        options = [correct_answer] + np.random.choice(wrong_answers, 3, replace=False).tolist()
        np.random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        explanation = f"""
        To simplify {operations[idx]}, we can apply the appropriate logarithm property.
        
        The correct simplification is {correct_answer}.
        
        Calculating the result: {results[idx]:.4f}
        """
        
        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation
        }
    
    elif question_type == "moderate_equation":
        # Generate a moderate logarithmic equation
        a = np.random.randint(2, 5)
        b = np.random.randint(1, 4)
        
        equation_types = [
            f"log(x) + log(x-{b}) = {a}",
            f"log(x) - log(x-{b}) = {a}",
            f"log(x^2) = {a}",
            f"log(x) = log({a*b}) - log({b})"
        ]
        
        solutions = [
            (b + np.sqrt(b*b + 4*10**a))/2,  # Using the quadratic formula for log(x) + log(x-b) = a
            (b*10**a)/(10**a - 1),  # For log(x) - log(x-b) = a
            10**(a/2),  # For log(x^2) = a
            a  # For log(x) = log(a*b) - log(b)
        ]
        
        idx = np.random.randint(0, len(equation_types))
        
        question = f"Solve for x: {equation_types[idx]}"
        correct_answer = round(solutions[idx], 2)
        
        # Generate wrong options
        options = [correct_answer]
        while len(options) < 4:
            wrong = correct_answer * np.random.choice([0.5, 0.8, 1.2, 1.5])
            wrong = round(wrong, 2)
            if abs(wrong - correct_answer) > 0.1 and wrong not in options and wrong > 0:
                options.append(wrong)
        
        np.random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        explanation = f"""
        To solve {equation_types[idx]}, we need to apply logarithm properties and algebraic techniques.
        
        The solution is x = {correct_answer}.
        """
        
        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation
        }
    
    elif question_type == "application":
        # Generate an application problem
        applications = [
            {
                "scenario": "Compound Interest",
                "question": f"How many years will it take for an investment of ${1000} to double at an annual interest rate of {6}%?",
                "formula": "t = log(2) / log(1 + r)",
                "solution": np.log(2) / np.log(1 + 0.06),
                "approach": "Using the compound interest formula A = P(1+r)^t, we set A = 2P and solve for t."
            },
            {
                "scenario": "Earthquake Magnitude",
                "question": f"An earthquake with amplitude A is {100} times stronger than an earthquake with amplitude B. How many points higher is the first earthquake on the Richter scale?",
                "formula": "Difference = log(A/B)",
                "solution": np.log10(100),
                "approach": "Using the Richter scale formula M = log(A), the difference in magnitude is log(A) - log(B) = log(A/B)."
            },
            {
                "scenario": "pH Calculation",
                "question": f"A solution has a hydrogen ion concentration of {10**(-3)} mol/L. What is its pH?",
                "formula": "pH = -log([H+])",
                "solution": 3,
                "approach": "Using the pH formula pH = -log([H+]), we substitute the hydrogen ion concentration."
            },
            {
                "scenario": "Sound Intensity",
                "question": f"If the sound intensity increases by a factor of {1000}, by how many decibels does the sound level increase?",
                "formula": "Difference = 10 × log(I₂/I₁)",
                "solution": 10 * np.log10(1000),
                "approach": "Using the decibel formula dB = 10 × log(I/I₀), the difference is 10 × log(I₂/I₁)."
            }
        ]
        
        selected_app = np.random.choice(applications)
        
        question = selected_app["question"]
        correct_answer = round(selected_app["solution"], 2)
        
        # Generate wrong options
        options = [correct_answer]
        while len(options) < 4:
            wrong = correct_answer * np.random.choice([0.5, 0.8, 1.2, 1.5])
            wrong = round(wrong, 2)
            if abs(wrong - correct_answer) > 0.1 and wrong not in options and wrong > 0:
                options.append(wrong)
        
        np.random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        explanation = f"""
        This problem involves {selected_app["scenario"]}.
        
        {selected_app["approach"]}
        
        Using the formula: {selected_app["formula"]}
        
        The answer is {correct_answer}.
        """
        
        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation
        }
    
    # Default fallback question (simple logarithm evaluation)
    base = 10
    exponent = 2
    value = base ** exponent
    
    question = f"What is the value of log({value})?"
    correct_answer = exponent
    options = [1, 2, 10, 20]
    correct_index = 1
    
    explanation = f"""
    To find log({value}), we need to determine what power of 10 equals {value}.
    
    Since 10^{exponent} = {value}, we have log({value}) = {exponent}.
    """
    
    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation
    }
