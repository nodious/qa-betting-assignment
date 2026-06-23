# Automation Framework Setup

## Prerequisites
- Python 3.12+
- Latest desktop Chrome

## Installation
1. Clone the repository
   git clone https://github.com/nodious/qa-betting-assignment.git
   cd qa-betting-assignment

2. Create and activate a virtual environment
   python3.12 -m venv venv
   source venv/bin/activate        # macOS/Linux

3. Install dependencies
   pip install -r requirements.txt

## Configuration
This project authenticates to the test application using a `user-id`, supplied
as an environment variable. Credentials are kept out of version control, 
so the suite can be run by anyone using their
own `user-id`.

### Setup

1. Copy the example environment file:
   cp .env.example .env          # macOS/Linux

2. Open `.env` and set your `user-id`:
   USER_ID=<your-user-id>

The application provides your `user-id` via the authentication method described
in the assignment (appended as a query parameter in the app URL). Use that same
value here.

`.env` should be gitignored and shouldn't be committed.

### Running the tests