AI Debugger – Powered by Gemini

An AI-powered debugging assistant that automatically runs, analyzes, and fixes Python code using Google Gemini.  

Upload any .py file, and the app will:  
1. Run your code safely in a sandbox  
2. Detect and display errors  
3. Ask Gemini to fix the code  
4. Show a before/after diff  
5. Test the fixed version automatically  



Live Demo
Try it on Streamlit Cloud: [AI Debugger App](https://34dzn5nul52zben25qq6vn.streamlit.app/)

---

Tech Stack
- Python 3.10+  
- [Streamlit](https://streamlit.io/) – interactive UI  
- [Google Gemini API](https://ai.google.dev/) – code debugging & fixes  
- subprocess – safe code execution  
- difflib – show code diffs  
- dotenv – manage API keys  

---

Project Structure
AI-debugger/
├── main.py # CLI debugger
├── app.py # Streamlit web app
├── requirements.txt
├── .gitignore
└── README.md




---

Features
- Debugs any Python file automatically  
- Detects and explains errors clearly  
- Asks Gemini to generate fixed code  
- Shows before/after diffs  
- Runs fixed code instantly  

---

Author
Akshay B Nair 
[LinkedIn](https://linkedin.com/in/akshay-b-nair) | [GitHub](https://github.com/Akshaynair47)
