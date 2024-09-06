from flask import Flask, render_template, request, redirect, url_for
import os
import smtplib
import dns.resolver
from colorama import init, Fore

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
    with open('valid_Oui.txt', 'w') as valid_file:
        for email in valid_emails:
            valid_file.write(email + '\n')

    with open('invalid_Oui.txt', 'w') as invalid_file:
        for email in invalid_emails:
            invalid_file.write(email + '\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            with open(filepath, 'r') as f:
                email_list = [line.strip() for line in f.readlines()]

            valid_emails, invalid_emails = process_emails(email_list)

            return render_template('index.html', valid_emails=valid_emails, invalid_emails=invalid_emails)

    return render_template('index.html', valid_emails=[], invalid_emails=[])

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)