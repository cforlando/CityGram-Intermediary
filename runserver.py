"""
This script runs the Citygram application using a development server
"""

from cgorl import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
