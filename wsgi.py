import os
from app import app

if __name__ == "__main__":
    # Render automatically provides the PORT environment variable
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=False)  # Debug set to False for production
