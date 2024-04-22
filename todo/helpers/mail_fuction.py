from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.mail import  get_connection
from apps.users.models import Users
from todo import settings
from todo.helpers.signer import URLEncryptionDecryption
"""------------------------------ EMAIL SENDING ---------------------------------------------"""

class SendEmails:
    
    def __init__(self, *args, **kwargs):
        pass
    
    
    def sendTemplateEmail(self, subject, request, context, template, email_host, user_email):
        sending_status = False
        sender_name = settings.EMAIL_SENDER_NAME

        try:
            connection        = get_connection()
            connection.open()
            context           = context
            image             = request.build_absolute_uri("/")
            # Social-Logo
            context['logo']                 = str(image)+'media/logo/todo_logo.png'
            context['x_logo']               = str(image)+'media/mail-logos/social-icons/x.png'
            context['instagram_logo']       = str(image)+'media/mail-logos/social-icons/instagram.png'
            context['facebook_logo']        = str(image)+'media/mail-logos/social-icons/facebook.png'
            context['linkedin_logo']        = str(image)+'media/mail-logos/social-icons/linkedin.png'
            context['youtube_logo']         = str(image)+'media/mail-logos/social-icons/youtube.png'
            # Social Url
            context['x_logo_url']           = 'https://www.twitter.com/lukerbrand'
            context['instagram_logo_url']   = 'https://www.instagram.com/harmanmotors'
            context['facebook_logo_url']    = 'https://www.facebook.com/harmanmotors'
            context['linkedin_logo_url']    = 'https://www.linkedin.com/company/lukerbrand/'
            context['youtube_logo_url']     = 'https://www.youtube.com/@harmanmotors2200'
            
            html_content      = render_to_string(str(template), {'context':context})
            text_content      = strip_tags(html_content)
            send_e            = EmailMultiAlternatives(subject, text_content, f'{sender_name} <{context["email"]}>', [context["email"]], connection=connection)
            send_e.attach_alternative(html_content, "text/html")
            
            send_e.send()
            connection.close()
            sending_status    = True
        except Exception as es:
            pass
        return sending_status
    
    
"""------------------------------ BULK EMAIL SENDING FOR SUBSCRIPTION---------------------------------------------"""


class SendBulkEmailsSend:
    def __init__(self, *args, **kwargs):
        pass
    
    def sendBulkEmailSend(self, subject, request, context, template, email_host, user_emails,encrypted_emails):
        sending_status = False
        sender_name = settings.EMAIL_SENDER_NAME

        try:
            for key,value in encrypted_emails.items():
                connection  = get_connection()
                connection.open()
                context = context  
                context['encrypt_email'] = value
                context['full_name']     = key[1]
                image = request.build_absolute_uri("/")
                # Social-Logo
                context['logo']                 = str(image)+'media/mail-logos/harman-motors.png'
                context['x_logo']               = str(image)+'media/mail-logos/social-icons/x.png'
                context['instagram_logo']       = str(image)+'media/mail-logos/social-icons/instagram.png'
                context['facebook_logo']        = str(image)+'media/mail-logos/social-icons/facebook.png'
                context['linkedin_logo']        = str(image)+'media/mail-logos/social-icons/linkedin.png'
                context['youtube_logo']         = str(image)+'media/mail-logos/social-icons/youtube.png'
                # Social Url
                context['x_logo_url']           = 'https://www.twitter.com/lukerbrand'
                context['instagram_logo_url']   = 'https://www.instagram.com/lukerbrand/'
                context['facebook_logo_url']    = 'https://www.facebook.com/lukerbrand'
                context['linkedin_logo_url']    = 'https://www.linkedin.com/company/lukerbrand/'
                context['youtube_logo_url']     = 'https://www.youtube.com/channel/UCqtd_B8oSXFpaRBe3s1Nb3w'
                
                html_content = render_to_string(str(template), {'context':context})
                text_content = strip_tags(html_content)
                send_e = EmailMultiAlternatives(str(subject), text_content, f'{sender_name} <email_host>', bcc=[key[0]], connection=connection)
                send_e.attach_alternative(html_content, "text/html")
                send_e.send()
                connection.close()
                sending_status = True
        except Exception as es:
            pass
        
        return sending_status
        
    def sendBulkReviewEmailSend(self, subject, context, template, email_host, user_emails,encrypted_emails):
        sending_status = False
        sender_name = settings.EMAIL_SENDER_NAME

        try:
            for key,value in encrypted_emails.items():
                connection  = get_connection()
                connection.open()
                context = context  
                context['encrypt_email'] = value[0]
                context['booked_room_detailed_obj'] = value[1]
                context['encryption_id'] = URLEncryptionDecryption.enc(value[1].id)
                # Social-Logo
                context['logo']                 = ''
                context['x_logo']               = ''
                context['instagram_logo']       = ''
                context['facebook_logo']        = ''
                context['linkedin_logo']        = ''
                context['youtube_logo']         = ''
                # Social Url
                context['x_logo_url']           = 'https://www.twitter.com/lukerbrand'
                context['instagram_logo_url']   = 'https://www.instagram.com/lukerbrand/'
                context['facebook_logo_url']    = 'https://www.facebook.com/lukerbrand'
                context['linkedin_logo_url']    = 'https://www.linkedin.com/company/lukerbrand/'
                context['youtube_logo_url']     = 'https://www.youtube.com/channel/UCqtd_B8oSXFpaRBe3s1Nb3w'
                
                html_content = render_to_string(str(template), {'context':context})
                text_content = strip_tags(html_content)
                send_e = EmailMultiAlternatives(str(subject), text_content, f'{sender_name} <email_host>', bcc=[key], connection=connection)
                send_e.attach_alternative(html_content, "text/html")
                send_e.send()
                connection.close()
                sending_status = True
        except Exception as es:
            pass
        
        return sending_status