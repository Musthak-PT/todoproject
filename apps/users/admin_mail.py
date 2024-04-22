import threading
from todo.helpers.mail_fuction import SendEmails
from todo import settings

def admin_register_completion_mail(request, user_instances, current_password, email):
    try:
        subject = "This is From TODO"
        context = {
            'full_name'           : user_instances.full_name,
            'phone_number'        : user_instances.phone,
            'customer_email'      : email,
            'password'            : current_password,
            'email'               : email,
            # 'room_count'          : total_quantity,
            'domain'              : settings.EMAIL_DOMAIN,
            'protocol'            : 'https',
        }
        
        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/admin-register-mail/customer_registeration.html', email, settings.EMAIL_HOST_USER))
        x.start()
    except Exception as es:
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", es)
        pass