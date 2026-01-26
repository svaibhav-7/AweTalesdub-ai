import uvicorn
from dubsmart.api.app import app

def main():
    """Main entry point for the API server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
