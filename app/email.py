'''
Created on 2017415

@author: zhou
'''

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mymail
import sendgrid
from sendgrid.helpers.mail import *
import os


def send_async_email(app, msg):
    with app.app_context():
        mymail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    sg = sendgrid.SendGridAPIClient(apikey='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')
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    from_email = Email(app.config['FLASKY_MAIL_SENDER'])
    subject = subject
    to_email = Email(to)
    content = Content("text/plain", render_template(template + '.txt', **kwargs))
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())
