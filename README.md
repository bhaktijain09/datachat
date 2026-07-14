# Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/bhaktijain09/datachat.git
cd datachat
```

2. **Create a virtual environment (Python 3.10 recommended)**

**Option A: Using venv**

```bash
python -m venv venv
```

Activate the environment:

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

**Option B: Using Conda**

```bash
conda create -n datachat python=3.10 -y
conda activate datachat
```

3. **Install the required dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up the MySQL database**

Ensure MySQL is installed and running.

Login:

```bash
mysql -u root -p
```

Create the database:

```sql
CREATE DATABASE datachat;
USE datachat;
```

Import the SQL files:

```bash
mysql -u root -p datachat < company_db.sql
mysql -u root -p datachat < university_system.sql
```

5. **Configure environment variables**

Create a `.env` file in the project root directory and add:

```env
DB_USER=your_mysql_username
DB_PASS=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=datachat
GOOGLE_API_KEY=your_api_key
```

6. **Run the application**

```bash
streamlit run app.py
```

If the `streamlit` command is not recognized:

```bash
python -m streamlit run app.py
```
