Setup Instructions
 
1. Clone the repository:
   git clone https://github.com/bhaktijain09/datachat.git
   cd datachat

2. Create a virtual environment (Python 3.10 recommended).

   Option A - Using venv:
   python -m venv venv

   Activate:
   • Windows: venv\Scripts\activate
   • macOS/Linux: source venv/bin/activate

   Option B - Using Conda:
   conda create -n datachat python=3.10 -y
   conda activate datachat

3. Install the required dependencies:
   pip install -r requirements.txt

4. Set up the MySQL database:
   • Ensure MySQL is installed and running.
   • Login:
     mysql -u root -p
   • Create the database:
     CREATE DATABASE datachat;
     USE datachat;
   • Import the SQL files:
     mysql -u root -p datachat < company_db.sql
     mysql -u root -p datachat < university_system.sql

5. Configure environment variables:
   • Create a `.env` file in the project root directory.
   • Add the following:
     DB_USER=your_mysql_username
     DB_PASS=your_mysql_password
     DB_HOST=localhost
     DB_PORT=3306
     DB_NAME=datachat
     GOOGLE_API_KEY=your_api_key

6. Run the application:
   streamlit run app.py

   If the `streamlit` command is not recognized:
   python -m streamlit run app.py
