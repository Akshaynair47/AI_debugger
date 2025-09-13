import streamlit as st
import subprocess
import os
import google.generativeai as genai
from dotenv import load_dotenv
from difflib import unified_diff

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use latest Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Function to run Python code and capture errors/output
def run_code(file_path):
    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Ask Gemini to fix the code
def fix_code(code, error):
    prompt = f"""
    The following Python code has an error:
    --- CODE ---
    {code}
    --- ERROR ---
    {error}
    Please return only the corrected code (no explanations, no markdown).
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.set_page_config(page_title="AI Debugger", page_icon="⚡", layout="wide")

st.title("⚡ AI Debugger – Powered by Gemini")
st.markdown("Upload your Python file, and let the AI automatically debug it.")

uploaded_file = st.file_uploader("📂 Upload a Python file", type=["py"])

if uploaded_file:
    file_path = "uploaded_code.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(uploaded_file.read().decode("utf-8"))

    st.subheader("📜 Original Code")
    with open(file_path, "r") as f:
        st.code(f.read(), language="python")

    if st.button("🚀 Run & Debug"):
        with st.spinner("Running your code..."):
            result = run_code(file_path)

        if result["success"]:
            st.success("✅ Code ran successfully!")
            st.text_area("📤 Output", result["output"], height=150)
        else:
            st.error("⚠️ Error detected!")
            st.text_area("Error Message", result["error"], height=150)

            with st.spinner("🔧 Asking Gemini to fix..."):
                original_code = open(file_path, "r").read()
                fixed_code = fix_code(original_code, result["error"])

            # Save fixed attempt
            fixed_file = "fixed_code.py"
            with open(fixed_file, "w", encoding="utf-8") as f:
                f.write(fixed_code)

            # Show code diff
            diff = unified_diff(
                original_code.splitlines(),
                fixed_code.splitlines(),
                fromfile="Before Fix",
                tofile="After Fix",
                lineterm=""
            )
            st.subheader("📜 Code Diff")
            st.code("\n".join(diff), language="diff")

            # Test the fixed code
            with st.spinner("Running fixed code..."):
                fixed_result = run_code(fixed_file)

            if fixed_result["success"]:
                st.success("🎉 Fixed code ran successfully!")
                st.text_area("📤 Output", fixed_result["output"], height=150)
            else:
                st.error("❌ Fix attempt failed.")
                st.text_area("Error Message", fixed_result["error"], height=150)
