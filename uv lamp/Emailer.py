import os
import sendgrid
import jinja2
import json
from sendgrid.helpers import mail

class Emailer:
    def __init__(self, email, key):
        self.api = sendgrid.SendGridAPIClient(api_key = key)
        self.sender = mail.Email(email)

    # destination: email address to be sent to
    # subject: just string with the emails subject
    # template_path: folder holding location of templates (needed due to no implicit cwd)
    # template_name: the html file to be loaded
    # context: context for said template
    def sendEmail(self, destination, subject, template_path, template_name, context):
        env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path))
        template = env.get_template(template_name)
        
        recipient = mail.To(destination)
        content = mail.Content("text/html", template.render(context))
        email = mail.Mail(self.sender, recipient, subject, content)
        
        response = self.api.send(email)
        print(response.status_code)
        print(response.body)
        print(response.headers)
