import os

# Database connection
DB_URI = os.environ.get('DB_URI', 'postgres://localhost:5432/daedam')

# Other config variables
ENTRIES_PER_PAGE = int(os.environ.get('ENTRIES_PER_PAGE', '10'))
