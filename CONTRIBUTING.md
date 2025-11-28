# Contributing to Zuiti

Thank you for your interest in contributing to **Zuiti — The Workplace Rant Companion**!  
We welcome all kinds of contributions, including:

- New features  
- Bug fixes  
- Documentation improvements  
- UI/UX enhancements  
- New rant personalities / styles  
- Ideas and discussions  

This document explains how to contribute.

---

## 🔧 Setting Up the Project Locally

### Backend (Flask)

```bash
git clone https://github.com/guanjun89061-beep/gongwei-zuite.git
cd gongwei-zuite

python -m venv .venv
.venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Set your key
set OPENAI_API_KEY=your_key_here

python app.py
