from flask import Flask, render_template, request, send_file
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from ToneModifier import Tonechanger
from TweetinTOV import createTweet
from CustominTOV import createCustom
from flask import request, redirect
from flask import session

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model = request.form['model']
        apikey = request.form['api_key']
        inputAuthorText = request.form['inputAuthorText']
        inputText = request.form['inputText']
        selectOutputFormat = request.form['selectOutputFormat']
        customInstruction = request.form['customInstruction']

        # Redirect to the selected application
        if selectOutputFormat == 'Long Text':
            token_counter, output_docx = Tonechanger(model, apikey, inputAuthorText, inputText, selectOutputFormat, customInstruction)
            filename = secure_filename(output_docx)
            return render_template('output-download.html', token_counter=token_counter, filename=filename)
        if selectOutputFormat == 'Tweet':
            token_counter, output_docx = createTweet(model, apikey, inputAuthorText, inputText, selectOutputFormat, customInstruction)
            filename = secure_filename(output_docx)
            return render_template('output-download.html', token_counter=token_counter, filename=filename)
        if selectOutputFormat == 'Custom':
            token_counter, output_docx = createCustom(model, apikey, inputAuthorText, inputText, selectOutputFormat, customInstruction)
            filename = secure_filename(output_docx)
            return render_template('output-download.html', token_counter=token_counter, filename=filename)
    return render_template('ToneChange.html')
    # Add more if-else conditions as needed for other options
    

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(filename)

if __name__ == '__main__':
    app.run(debug=True)
