import os
import sendgrid
import jinja2
import json
from pathlib import Path
from datetime import datetime
from sendgrid.helpers import mail

class Emailer:
    def __init__(self, log_file, email, key):
        self.api = sendgrid.SendGridAPIClient(api_key = key)
        self.sender = mail.Email(email)

    def printlog(self, log_file, msg):
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
        print(template_path)
        template = env.get_template(template_name)
        print(template)

        recipient = mail.To(destination)
        content = mail.Content("text/html", template.render(context))
        email = mail.Mail(from_email=self.sender, to_emails=recipient, subject=subject, html_content=content)
        response = self.api.send(email)
        
        return response.status_code
