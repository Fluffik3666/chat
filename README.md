# Seurt

## What is Seurt
- Seurt is a open source web based chat app. 

## Setup & Development
- All commands from project root

1. Create virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create firebase app:
   - Create a firebase app and add Cloud Firestore in location "London"
   - Generate a python service account json file
   - Either:
      - Convert the json file to enviroment varibles and continue to step 5
      - Place the json file in firebase/ and then update DB varible in api.py with:
         ```python
         db = DB(credentials_path="./firebase/<file_name_here>")
         ```

5. Run the application:
   ```bash
   python3 main.py
   ```

## Structure

- `main.py` - Application entry point
- `firebase/` - Firebase configuration
- `src/` - Source code
  - `controllers/` - Business logic
  - `routes/` - Route definitions
  - `static/` - Statically served files
  - `templates/` - HTML files
