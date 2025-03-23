# Flask Application

A simple Flask web application with a responsive design.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to: `http://127.0.0.1:5000/`

## Project Structure

- `app.py`: Main Flask application file
- `templates/`: HTML templates
  - `base.html`: Base template with common elements
  - `index.html`: Home page template
  - `about.html`: About page template
- `static/`: Static files
  - `css/`: CSS stylesheets
  - `js/`: JavaScript files 