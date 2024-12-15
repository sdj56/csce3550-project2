# JWKS Server with SQLite-backed Storage

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-repo-link>.git
   cd <repo-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python setup_db.py
   ```
   This script initializes the SQLite database `totally_not_my_privateKeys.db` with the required schema.

---

## Running the Server
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Access the server at `http://127.0.0.1:5000`.

---

## Testing with Gradebot
1. Ensure the server is running.
2. Run the Gradebot client with the following command:
   ```bash
   gradebot-client project2
   ```
3. The Gradebot client will validate your implementation and provide a rubric with the points awarded.
4. Include a screenshot of the Gradebot output in your repository for submission.

---

For any questions or issues, please contact `<Your Name>` at `<Your Email>`. 
