# <Customer Sentiment Analysis>

## Overview

This project performs sentiment analysis using a trained model. Follow the steps below to set up and run the project.

## Prerequisites

- Python 3.6 or higher

## Setup

1. **Create a Python Environment:**

    ```bash
    python -m venv venv
    ```

2. **Activate the Environment:**

    - On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```

3. **Install Required Libraries:**

    ```bash
    pip install -r requirements.txt
    ```

## Training the Model

4. **Run the Trainer:**

    ```bash
    python trainer.py
    ```

    This will train the model.

## Starting the Server

5. **Run the Server:**

    ```bash
    python server.py
    ```

    The server will start running on `http://127.0.0.1:5000/` unless specified otherwise.

6. **Access the Application:**

    Open your preferred web browser (e.g., Chrome) and navigate to `http://127.0.0.1:5000/`.

    Enjoy!

## Notes

- Make sure to update the `requirements.txt` file whenever you add or remove dependencies.
- Customize the project settings in the respective Python files as needed.
- For additional options and configurations, refer to the project documentation.

Happy analyzing!
