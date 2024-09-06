from flask import Flask, render_template, request, jsonify, send_file
import os
import smtplib
import dns.resolver
from colorama import init

# Initialize colorama for terminal output
init(autoreset=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def check_email_existence(email):
    try:
        domain = email.split('@')[-1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)

        server = smtplib.SMTP(mx_record)
        server.set_debuglevel(0)

        server.helo()
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return True
        else:
            return False
    except Exception as e:
        return False

def process_emails(email_list):
    valid_emails = []
    invalid_emails = []

    for email in email_list:
        if check_email_existence(email):
            valid_emails.append(email)
        else:
            invalid_emails.append(email)

    write_to_files(valid_emails, invalid_emails)
    return valid_emails, invalid_emails

def write_to_files(valid_emails, invalid_emails):
    with open('valid.txt', 'w') as valid_file:
        for email in valid_emails:
            valid_file.write(email + '\n')

    with open('invalid.txt', 'w') as invalid_file:
        for email in invalid_emails:
            invalid_file.write(email + '\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    email_list = []

    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        with open(filepath, 'r') as f:
            email_list = [line.strip() for line in f.readlines()]

    elif 'email_text' in request.form and request.form['email_text'].strip() != '':
        email_list = [email.strip() for email in request.form['email_text'].splitlines()]

    if not email_list:
        return jsonify({'error': 'No emails to process'})

    valid_emails, invalid_emails = process_emails(email_list)

    return jsonify({'valid_emails': valid_emails, 'invalid_emails': invalid_emails})

@app.route('/download_valid')
def download_valid():
    return send_file('valid.txt', as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
