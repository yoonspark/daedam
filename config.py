import os

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', '')

# Authorization config
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', '')
AUTH0_ALGORITHMS = [os.environ.get('AUTH0_ALGORITHM', '')]
AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE', '')

# Tokens for testing
JWT_AUDIENCE = os.environ.get('JWT_AUDIENCE', '')
JWT_MODERATOR = os.environ.get('JWT_MODERATOR', '')
JWT_ADMIN = os.environ.get('JWT_ADMIN', '')

# Other config variables
ENTRIES_PER_PAGE = int(os.environ.get('ENTRIES_PER_PAGE', ''))
