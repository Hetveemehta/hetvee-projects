# URL Shortener Application

A full-stack web application designed to shorten long URLs into concise, manageable links. Built using Python (Flask) for the backend and HTML/CSS for the frontend, utilizing a persistent JSON-based storage system.

## Project Overview

This application provides a user-friendly interface for generating short links. It features a custom "Void Blue" and Beige aesthetic, ensures link persistence across server restarts using file-based storage, and includes a history log of recently generated links.

## Key Features

* **URL Redirection:** Instantly redirects short codes to the original destination URL.
* **Persistent Storage:** Uses a local JSON database (`urls.json`) to save data, ensuring links remain active even after the application is closed.
* **Input Validation:** Automatically detects and appends HTTP protocols if missing.
* **User History:** Displays a list of recently shortened links within the interface.
* **Clipboard Integration:** One-click functionality to copy generated links.
* **Responsive UI:** Professional interface designed with high-contrast styling for readability.

## Technical Stack

* **Language:** Python 3.x
* **Framework:** Flask
* **Frontend:** HTML5, CSS3
* **Storage:** JSON (File System)

## Installation and Setup

Follow these steps to set up the project locally on your machine.

### 1. Prerequisites
Ensure you have Python installed on your system. You can verify this by running `python --version` in your terminal.

### 2. Install Dependencies
Open your terminal or command prompt and install the required Flask libraries:

```bash
pip install flask flask-cors
```

### 3.Project Structure
URL_Shortener/
│
├── app.py              # Main application logic
├── urls.json           # Database file (auto-generated)
├── README.md           # Project documentation
└── templates/          # Frontend directory
    └── index.html      # User Interface file

### Usage
Navigate to the project directory in your terminal.

Run the application using the following command:

```bash
python app.py
```
The terminal will display a local server address (usually http://127.0.0.1:5000).

Open your web browser and navigate to that address.

Paste a long URL into the input field and click "Shorten URL".

### Troubleshooting
Module Not Found Error: If you see an error regarding missing modules, ensure you have run the pip install command listed in the Installation section.

Template Not Found: Ensure your index.html file is located inside a folder named exactly templates.

Permission Error: If the application fails to save links, ensure the folder has write permissions so the urls.json file can be created.


Author
Developed by- 
Hetvee Mehta