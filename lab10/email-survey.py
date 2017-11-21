# -*- coding: utf-8 -*-

# Note, this may take up to 12 hours to send the message!
# From: https://null-byte.wonderhowto.com/how-to/send-anonymous-emails-with-python-0163091/
# and http://npyscreen.readthedocs.io/introduction.html

# This lab is a thinly-veiled attempt at collecting your feedback to demonstrate how a Pi
# can automate browser interactions and generate a console-based GUI.

import mechanize
import npyscreen
import time

class FeedbackApp(npyscreen.NPSApp):
  def __init__(self):
    self.__questions = {}
    self.__questions[1] = "On a scale of 1 to 10, in general, how would you rate this class?"
    self.__questions[2] = "Why did you rank it this way?"
    self.__questions[3] = "How did you feel about the lecture component?"
    self.__questions[4] = "How did you feel about the practical (i.e., lab) component?"
    self.__questions[5] = "How did you feel about the term project?"
    self.__questions[6] = "What suggestions would you have for future iterations of this class?"
    self.__questions[7] = "Any other comments you feel I should know?" 

  def main(self):
    F  = npyscreen.Form(name = "CSCI5900 Course Feedback",)
    scale  = F.add(npyscreen.TitleSlider, out_of=10, name = self.__questions[1])
    q2     = F.add(npyscreen.TitleText, name = self.__questions[2])
    q3     = F.add(npyscreen.TitleText, name = self.__questions[3])
    q4     = F.add(npyscreen.TitleText, name = self.__questions[4])
    q5     = F.add(npyscreen.TitleText, name = self.__questions[5])
    q6     = F.add(npyscreen.TitleText, name = self.__questions[6])
    q7     = F.add(npyscreen.TitleText, name = self.__questions[7])
    name   = F.add(npyscreen.TitleText, name = "If you want to let me know who you are, change the name from Anonymous to your name", value = "Anonymous")

    # interact with the Form.
    F.edit()

    answers = {}
    answers[1] = scale.value
    answers[2] = q2.value
    answers[3] = q3.value
    answers[4] = q4.value
    answers[5] = q5.value
    answers[6] = q6.value
    answers[7] = q7.value

    # Create browser object
    br = mechanize.Browser()

    # Setup recipient
    to      = "fredericks@oakland.edu"
    subject = "CSCI5900 Lab 10 Feedback"
    
    # Get user feedback packaged into a message
    message = ""
    for i in xrange(1,8):
      message += self.__questions[i] + "\n" + str(answers[i]) + "\n----\n"

    url           = "http://anonymouse.org/anonemail.html"
    headers       = "Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)"
    
    # Setup browser 
    br.addheaders = [('User-agent', headers)]
    br.open(url)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_debug_http(False)
    br.set_debug_redirects(False)
    br.select_form(nr=0)
    br.form['to'] = to
    br.form['subject'] = subject
    br.form['text'] = message
    result = br.submit()
    resp = br.response().read()
    
    if "The e-mail has been sent anonymously!" in resp:
      npyscreen.notify("Email sent successfully!", title='Notice')
      time.sleep(5) # needed to have it show up for a visible amount of time
    else:
      npyscreen.notify("Email failure!", title='Notice')
      time.sleep(5) # needed to have it show up for a visible amount of time
      self.main()

    return 

if __name__ == "__main__":
  app = FeedbackApp()
  output = app.run()

  op = "\n\n##############################################################################################################################\n"
  op += "        ████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗    ██╗   ██╗ ██████╗ ██╗   ██╗    ███████╗ ██████╗ ██████╗                \n"
  op += "        ╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██╔════╝██╔═══██╗██╔══██╗               \n"
  op += "           ██║   ███████║███████║██╔██╗ ██║█████╔╝      ╚████╔╝ ██║   ██║██║   ██║    █████╗  ██║   ██║██████╔╝               \n"
  op += "           ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗       ╚██╔╝  ██║   ██║██║   ██║    ██╔══╝  ██║   ██║██╔══██╗               \n"
  op += "           ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝    ██║     ╚██████╔╝██║  ██║               \n"
  op += "           ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝               \n"
  op += "                                                                                                                              \n"
  op += "████████╗ █████╗ ██╗  ██╗██╗███╗   ██╗ ██████╗     ████████╗██╗  ██╗██╗███████╗     ██████╗██╗      █████╗ ███████╗███████╗██╗\n"
  op += "╚══██╔══╝██╔══██╗██║ ██╔╝██║████╗  ██║██╔════╝     ╚══██╔══╝██║  ██║██║██╔════╝    ██╔════╝██║     ██╔══██╗██╔════╝██╔════╝██║\n"
  op += "   ██║   ███████║█████╔╝ ██║██╔██╗ ██║██║  ███╗       ██║   ███████║██║███████╗    ██║     ██║     ███████║███████╗███████╗██║\n"
  op += "   ██║   ██╔══██║██╔═██╗ ██║██║╚██╗██║██║   ██║       ██║   ██╔══██║██║╚════██║    ██║     ██║     ██╔══██║╚════██║╚════██║╚═╝\n"
  op += "   ██║   ██║  ██║██║  ██╗██║██║ ╚████║╚██████╔╝       ██║   ██║  ██║██║███████║    ╚██████╗███████╗██║  ██║███████║███████║██╗\n"
  op += "   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝        ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝     ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝\n"
  op += "##############################################################################################################################\n\n"
  print op
