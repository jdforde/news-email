from datetime import date
import time
import random
import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.mockup_generator import mockup_generator
import src.util.secret_constants as sc
import src.util.constants as c
from util.functions import read_cache


'''
Open Issues:
- Get database functionality running
- Fix issue of caption being the same as a sentence (I think this is fixed)
- Make summaries far shorter
- Make mockup generation quicker, not really sure why it's taking so long
- Add a "source" in html which tells user where story is from
- Clean up html a bit: there's a big space between beginning and Today In News
'''

total_time = time.time()
logger = logging.getLogger()
logger.propagate = False
logger.setLevel(logging.INFO) 
log = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s : %(filename)s : %(funcName)s :: %(message)s', "%Y-%m-%d %H:%M:%S")
log.setFormatter(formatter)
logger.addHandler(log)

def add_bullets(story):
  html = ""
  for sentence in story[c.STORY_SUMMARY]:
    html += '''
      <li color="rgb(255, 255, 255)" style="text-align: inherit; font-family: &quot;times new roman&quot;, times, serif; color: rgb(255, 255, 255)">
      <span style="overflow-wrap: break-word; text-indent: -0.25in; line-height: normal; font-size: 14pt; color: #ffffff; font-family: &quot;times new roman&quot;, times, serif">
      ''' + sentence + '''<br></span><span style="color: #ffffff; font-family: &quot;times new roman&quot;, times, serif">&nbsp;</span></li>
    '''
  return html

def create_story(story, image):
  html = '''
    <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" style="padding:0px 0px 0px 0px;" bgcolor="#A8D0E6" data-distribution="1">
    <tbody>
      <tr role="module-content">
        <td height="100%" valign="top">
        <table width="580" style="width:580px; border-spacing:0; border-collapse:collapse; margin:0px 10px 0px 10px;" cellpadding="0" cellspacing="0" align="left" 
        border="0" bgcolor="" class="column column-0">
      <tbody>
        <tr>
          <td style="padding:0px;margin:0px;border-spacing:0;">
          <table class="wrapper" role="module" data-type="image" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" 
          data-muid="36b63578-131e-48e8-b88e-ae463267a7c8">
            <tbody> 
    '''
  if image and c.STORY_IMAGE in story.keys():
    html +=  '''
    <tr>
      <td style="font-size:6px; line-height:10px; padding:15px 0px 0px 0px;" valign="top" align="center">
        <img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px;" 
        href=width="275" alt="" data-proportionally-constrained="true" data-responsive="false" src=''' + story[c.STORY_IMAGE]  + ''' height="183">
      </td>
    </tr>
    '''
  
  html += '''
          </tbody>
        </table>
    <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" 
    data-muid="b7ba1a11-3f0c-4d1e-a9bc-857b817dbf61" data-mc-module-version="2019-10-22">
    <tbody>
      <tr>
        <td style="padding:18px 0px 18px 0px; line-height:22px; text-align:inherit;" height="100%" valign="top" bgcolor="" role="module-content"><div>
        <div style="font-family: inherit; text-align: center"><span style="overflow-wrap: break-word; margin-bottom: 0in; line-height: normal; font-size: 30px; 
        color: #a70c0c; font-family: verdana, geneva, sans-serif"><strong><a href=''' + story[c.STORY_URL] +">" +  story[c.STORY_TITLE] + '''</a></strong></span>
        <span style="font-size: 30px; color: #a70c0c; font-family: verdana, geneva, sans-serif">&nbsp;</span></div>
        <div style="font-family: inherit; text-align: center"><span style="overflow-wrap: break-word; margin-bottom: 0in; line-height: normal; font-size: 18px; 
        color: #a70c0c; font-family: verdana, geneva, sans-serif">''' + story[c.STORY_CAPTION] + '''</span><span style="font-size: 18px; color: #a70c0c; 
        font-family: verdana, geneva, sans-serif">&nbsp;</span></div>
        <div style="font-family: inherit; text-align: center"><br></div>
        <ul padding-left: 200px >
    '''
  html+= add_bullets(story)
  html+= '''
  </ul><div></div></div></td>
      </tr>
    </tbody>
  </table>
  </td>
        </tr>
      </tbody>
    </table></td>
      </tr>
    </tbody>
  </table>
    <table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="0fab0d29-049a-442d-8faf-5efd102c5669">
    <tbody>
      <tr>
        <td style="padding:0px 0px 8px 0px;" role="module-content" bgcolor="374785">
        </td>
      </tr>
    </tbody>
  </table>
  '''

  return html

def email_sender():
  logging.info("Starting mockup generation")
  mockup = mockup_generator()

  logging.info("Composing email")
  choices = random.choices([True, False], weights=(30, 70), k=len(mockup)-1)
  choices.insert(0, True)
  html = c.STATIC_BEGINNING
  for story, picture in zip(mockup, choices):
      html+= create_story(story, picture)

  html += c.STATIC_END

  activity_time = time.time()

  message = Mail(
      from_email=sc.SENDER_EMAIL,
      to_emails=sc.RECIPIENTS,
      subject=c.month[date.today().month] + " " + str(date.today().day) + ", " + str(date.today().year),
      html_content=html
  )

  try:
      sg = SendGridAPIClient(sc.SENDGRID_API_KEY)
      response = sg.send(message)
      logging.info("Successfully able to send email in {:.2f} seconds".format(time.time()-activity_time))
      logging.info(response.headers)
  except Exception as e:
      logging.critical("Unable to send email: ", e)

  logging.info("Entire program finished in {:.2f} seconds".format(time.time()-total_time))

if __name__ == '__main__':
  email_sender()