import os
import sendgrid
import jinja2
import json
from pathlib import Path
from datetime import datetime
from sendgrid.helpers import mail
import smtplib
from email.mime.text import MIMEText

class Emailer:
    def __init__(self, log_file, email, key):
        self.api = sendgrid.SendGridAPIClient(api_key = key)
        self.sender = mail.Email(email)
        self.log_file = log_file

    def printlog(self, log_file, msg):
        if log_file is None:
            return
        
        fmt_msg = datetime.now().strftime("[%X]") + " " + "[{}]".format(Path(__file__).name) + " " + msg
        print(fmt_msg)
        log_file.write(fmt_msg + "\n")

    # destination: email address to be sent to
    # subject: just string with the emails subject
    # template_path: folder holding location of templates (needed due to no implicit cwd)
    # template_name: the html file to be loaded
    # context: context for said template
    def sendEmail(self, destination, subject, template_name, context):
        template_path = os.path.dirname(os.path.realpath(__file__)) + "\\templates\\email\\"
        env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path))
        template = env.get_template(template_name)

        recipient = mail.To(destination)
        content = mail.Content("text/html", template.render(context))
        email = mail.Mail(from_email=self.sender, to_emails=recipient, subject=subject, html_content=content)
        response = self.api.send(email)
        
        return response.status_code
    
    def sendEmailDemo(self, destination, subject, template_name, context):
        host = "smtp.mail.yahoo.com"
        port = 465
        username = "lanmanking@yahoo.com"
        password = "GeorgiaTech#1"
        sender = "lanmanking@yahoo.com"
        destination = "lanmanking@yahoo.com"

        template_path = os.path.dirname(os.path.realpath(__file__)) + "\\templates\\email\\"
        env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path))
        template = env.get_template(template_name)

        msg = MIMEText(template.render(context))
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = destination

        server = smtplib.SMTP_SSL(host, port)
        server.login(username, password)
        server.sendmail(sender, destination, msg.as_string())
        server.quit()

def test():

    emailer = Emailer(None, "lking@diversitech.com", "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")
    result = emailer.sendEmail("lanmanking@yahoo.com", "Test!", "reminder.html", {"fullname": "Landry M. King"})
    print(result)

if __name__ == "__main__":
    test()