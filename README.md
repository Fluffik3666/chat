# Flask Application

## Setup

1. Activate virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Structure

- `main.py` - Application entry point
- `src/` - Source code
  - `controllers/` - Business logic
  - `routes/` - Route definitions
  - `models/` - Data models
  - `helpers/` - Utility functions
