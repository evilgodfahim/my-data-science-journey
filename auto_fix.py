import py_compile

filename = "pdf.py"
max_attempts = 100
attempts = 0

print(f"Scanning {filename} for quote syntax errors...")

while attempts < max_attempts:
    attempts += 1
    try:
        # Try to compile the file. If it passes, we are done!
        py_compile.compile(filename, doraise=True)
        print("✅ File is perfectly clean! No syntax errors found.")
        break
    except py_compile.PyCompileError as e:
        # If it fails, grab the exact line number of the error
        line_num = e.exc_value.lineno
        print(f"⚠️ Syntax error on line {line_num}. Attempting to fix...")
        
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        bad_line = lines[line_num - 1]
        
        # Look for the outer wrapper, e.g., body(' ... ')
        if "('" in bad_line and "')" in bad_line:
            # Replace the first (' with ("""
            fixed_line = bad_line.replace("('", '("""', 1)
            
            # Replace the very last ') with """)
            parts = fixed_line.rsplit("')", 1)
            fixed_line = '""")'.join(parts)
            
            lines[line_num - 1] = fixed_line
            
            # Overwrite the file with the fix and loop again
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        else:
            print(f"❌ Cannot auto-fix line {line_num}. You will need to check this one manually:")
            print(bad_line)
            break