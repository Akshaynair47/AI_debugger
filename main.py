import subprocess
import difflib
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load .env file
load_dotenv()

# ✅ Configure Gemini with GOOGLE_API_KEY
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found! Please add it to your .env file.")
genai.configure(api_key=api_key)

# ✅ Select Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# --------------------------------------------------
# Function to run a Python file and capture errors
# --------------------------------------------------
def run_code(filename):
    try:
        result = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return {"success": True, "output": result.stdout.strip()}
        else:
            return {"success": False, "error": result.stderr.strip()}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "⏳ Timeout: Code took too long to run."}

# --------------------------------------------------
# Function to ask Gemini to fix code
# --------------------------------------------------
def fix_code(code, error):
    prompt = f"""
You are a Python code debugging assistant.
The following code has an error:

--- CODE ---
{code}
--- ERROR ---
{error}

Please return ONLY the corrected Python code (no markdown, no ```).
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# --------------------------------------------------
# Debugging workflow
# --------------------------------------------------
def debug_code(file_path, max_attempts=3):
    with open(file_path, "r") as f:
        code = f.read()

    for attempt in range(1, max_attempts + 1):
        print(f"\n▶️ Attempt {attempt}: Running {file_path}...")
        result = run_code(file_path)

        if result["success"]:
            print("✅ Code ran successfully!")
            print("📤 Output:\n", result["output"])

            final_file = "fixed_final.py"
            with open(final_file, "w") as f:
                f.write(code)
            print(f"\n🎉 Final working code saved as {final_file}")
            return

        else:
            print("⚠️ Error detected:\n", result["error"])
            print("\n🛠 Asking Gemini to fix the code...")

            fixed_code = fix_code(code, result["error"])

            # Show code diff
            diff = difflib.unified_diff(
                code.splitlines(),
                fixed_code.splitlines(),
                fromfile="Before Fix",
                tofile="After Fix",
                lineterm=""
            )
            print("\n📜 Code Diff:")
            for line in diff:
                print(line)

            # Save fixed attempt
            new_file = f"fixed_attempt_{attempt}.py"
            with open(new_file, "w") as f:
                f.write(fixed_code)
            print(f"💾 Fixed code saved as {new_file}")

            file_path = new_file
            code = fixed_code

    print("❌ Max attempts reached, still failing.")

# --------------------------------------------------
# Main Entry
# --------------------------------------------------
def main():
    print("\n🚀 Starting Debugging Agent...")
    debug_code("buggy.py")

if __name__ == "__main__":
    main()
