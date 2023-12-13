from application import app
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)

if __name__=="__main__":
    app.run(debug=True)