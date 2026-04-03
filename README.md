Setup Instructions:

1. Clone the Repository
git clone https://github.com/bhaktijain09/datachat.git
cd datachat

2. Create a Virtual Environment (Python 3.10 Recommended)

Option A - Using venv:
python -m venv venv

Activate:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate


Option B — Using Conda:
conda create -n datachat python=3.10 -y
conda activate datachat

3. Install Dependencies
pip install -r requirements.txt

4. Set Up MySQL Database
Ensure MySQL is installed and running.

Login: mysql -u root -p

Create database:
CREATE DATABASE datachat;
USE datachat;

Import schema files:
mysql -u root -p datachat < company_db.sql
mysql -u root -p datachat < university_system.sql

5. Configure Environment Variables
Create a file named .env in the project root directory.

Add:
DB_USER=your_mysql_username
DB_PASS=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=datachat
GOOGLE_API_KEY=your_api_key

The .env file is intentionally excluded from version control for security reasons.

6. Run the Application
streamlit run app.py


If Streamlit is not recognized: python -m streamlit run app.py
