from . import *

if __name__ == "__main__":
    app = new_app()
    app.run(port="5050", debug=True)
