from flask import Flask, request
from PIL import Image
from escpos import printer

# p = printer.Dummy()
p = printer.Usb(0x0416, 0x5011, 0, 0x81, 0x03)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['DEBUG'] = True
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/upload", methods=['GET', 'POST'])
def image_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "No file selected"

        file = request.files['file']

        if file and allowed_file(file.filename):
            img = Image.open(file)
            #img.save('output.png')
            print("\nImage size: ", img.size)
            #img.show()
            p.image(img)
            #print(p.output)
            print("image printed to dummy printer\n")
            return "image uploaded"
        
        return "file not allowed"
    
    if request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload an image</title>
        <h1>Upload an image to print</h1>
        <form method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
             </form>
          </p>
        </form>
        '''

    return f'Invalid request method {request.method}, use POST'

def main():
    p.text("Start Machine\n")
    # print(p.output)

    app.run(host='localhost', port=8080)

if __name__ == "__main__":
    main()