import random

NUM_SAMPLES = 1000
MAX_DEPTH = 4
OUTPUT_RAW_TXT = "complex_latex.txt"

VARS = ['x', 'y', 'z', 't', '\\alpha', '\\beta', '\\theta', 'n', 'k', 'a', 'b']
NUMS = ['1', '2', '0', '\\pi', '\\infty', 'e', '10']
FUNCS = ['\\sin', '\\cos', '\\log', '\\ln', '\\det']

def get_atom():
    return random.choice(VARS + NUMS)

def format_frac(num, den):
    """随机分式写法"""
    choices = [
        f"\\frac{{{num}}}{{{den}}}",
        f"{{{num} \\over {den}}}",
        f"\\frac {num} {den}" if len(num)<2 and len(den)<2 else f"\\frac{{{num}}}{{{den}}}"
    ]
    return random.choice(choices)

def format_group(content):
    """随机括号写法"""
    choices = [
        f"\\left( {content} \\right)",
        f"({content})",
        f"\\left[ {content} \\right]",
        f"\\left\\{{ {content} \\right\\}}"
    ]
    res = random.choice(choices)
    if random.random() < 0.3:
        res = res.replace("(", "( ").replace(")", " )")
    return res

def format_pow(base, exp):
    """随机上下标写法"""
    can_omit_brace = len(exp) == 1 and not exp.startswith('\\')
    
    if can_omit_brace and random.random() > 0.5:
        return f"{base}^{exp}"
    else:
        gap = " " if random.random() < 0.3 else ""
        return f"{base}^{gap}{{{exp}}}"

def format_sqrt(content):
    if random.random() < 0.3:
        return f"\\sqrt {content}" if len(content)==1 else f"\\sqrt{{{content}}}"
    return f"\\sqrt{{{content}}}"

def gen_expr(depth):
    """递归生成器"""
    if depth <= 0 or (depth < MAX_DEPTH and random.random() < 0.15):
        return get_atom()

    structure_type = random.choice([
        'op', 'frac', 'sqrt', 'power', 'sub', 
        'func', 'integral', 'matrix', 'cases'
    ])

    try:
        if structure_type == 'op':
            op = random.choice(['+', '-', '=', '\\approx', '\\times', '\\cdot'])
            return f"{gen_expr(depth-1)}{" "}{op}{" "}{gen_expr(depth-1)}"
        
        elif structure_type == 'frac':
            return format_frac(gen_expr(depth-1), gen_expr(depth-1))
        
        elif structure_type == 'sqrt':
            return format_sqrt(gen_expr(depth-1))
        
        elif structure_type == 'power':
            return format_pow(gen_expr(depth-1), gen_expr(depth-1))

        elif structure_type == 'sub':
            return f"{random.choice(VARS)}_{{{gen_expr(depth-1)}}}"

        elif structure_type == 'func':
            return f"{random.choice(FUNCS)}{format_group(gen_expr(depth-1))}"

        elif structure_type == 'integral':
            if random.random() < 0.5:
                return f"\\int_{{{gen_expr(depth-2)}}}^{{{gen_expr(depth-2)}}} {gen_expr(depth-1)} d{random.choice(['x','t'])}"
            else:
                return f"\\int {gen_expr(depth-1)} d{random.choice(['x','t'])}"

        elif structure_type == 'matrix':
            env = random.choice(['pmatrix', 'bmatrix', 'vmatrix', 'array'])
            rows = random.randint(2, 3)
            cols = random.randint(2, 3)
            content = ""
            for r in range(rows):
                row = [gen_expr(depth-2) for _ in range(cols)]
                content += " & ".join(row)
                if r < rows - 1:
                    content += " \\\\ "
            
            if env == 'array':
                align = "c" * cols
                return f"\\begin{{array}}{{{align}}} {content} \\end{{array}}"
            return f"\\begin{{{env}}} {content} \\end{{{env}}}"

        elif structure_type == 'cases':
            content = f"{gen_expr(depth-1)} & \\text{{if }} x > 0 \\\\ {gen_expr(depth-1)} & \\text{{otherwise}}"
            return f"\\begin{{cases}} {content} \\end{{cases}}"

    except RecursionError:
        return get_atom()
    return get_atom()

def main():
    print(f"Generating {NUM_SAMPLES} noisy LaTeX expressions...")
    with open(OUTPUT_RAW_TXT, 'w', encoding='utf-8') as f:
        unique_set = set()
        while len(unique_set) < NUM_SAMPLES:
            expr = gen_expr(MAX_DEPTH)
            if len(expr) < 20: continue
            
            final_expr = f"${expr}$"
            
            if final_expr not in unique_set:
                unique_set.add(final_expr)
                f.write(final_expr + "\n")
    
    print(f"Saved raw noisy LaTeX to: {OUTPUT_RAW_TXT}")

if __name__ == "__main__":
    main()