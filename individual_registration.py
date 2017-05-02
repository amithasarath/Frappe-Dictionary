@frappe.whitelist(allow_guest=True)
def send_notification(doc):	
	''' Notification to Administrator on Individual Delegate submit the Form '''

  #Send Desk Notification
  if doc:
      args = {
        "assign_to":"Administrator" ,
        "doctype": doc.doctype ,
        "name": doc.name ,
        "description":"Student Applicant: "+ doc.first_name + " is Applied"
      }
      print args

      assign_to.notify_assignment(frappe.session.user, frappe.session.user, doc.doctype, doc.name, action='CLOSE',description=None, notify=0)
      assign_to.add(args)	
      #frappe.desk.form.assign_to.remove_from_todo_if_already_assigned (doc.doctype, doc.name)

      #Send Mail			
      sub = "Student Application"
      content = doc.first_name + " has been applied for a course"
      mail_to = frappe.db.get_value("User",{"name":"Administrator"},"email")
      msgprint(_("Thank You for Registering. Please note that your application id is : "+doc.name))	

      from frappe.utils import get_url

      try:
        if doc.student_email_id:
          sMsg = """Dear {fname} {mname} {lname}. 
          Greetings from thinksmart for registering for the program - {pgm} . 
          Please note that your application id is {app_id}. 
          You can check your application status in this page {status_page}.
          Thanks""".format(fname=doc.first_name,mname=doc.middle_name,lname=doc.last_name,pgm=doc.program,app_id=doc.name,status_page=get_url()+"/app_status?app_id="+doc.name)
          send(recipients = doc.student_email_id, sender = doc.student_email_id,
            subject = "Thank You for Registering", message = sMsg,
            reference_doctype = doc.doctype, reference_name = doc.name,
            send_priority = 0)
        send(recipients = mail_to, sender = mail_to,
          subject = sub, message = content,
          reference_doctype = doc.doctype, reference_name = doc.name,
          send_priority = 0)
        #frappe.local.response["type"] = "redirect"
        #frappe.local.response["location"] = "/home_page"
        #frappe.utils.response.redirect ()
        #redirect_to = get_url("/home_page")

      except frappe.OutgoingEmailError:
        print frappe.get_traceback()
        #msgprint (_("EMAIL NOT SEND "))
        pass # email server not set, don't send email
