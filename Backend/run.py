import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from app import app

if __name__ == "__main__":
    app.run(debug=True) 