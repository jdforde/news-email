from src.util import secret_constants as sc

SIGNUP_LINK = "https://cdn.forms-content.sg-form.com/d96cc00b-f7c0-11eb-be93-9a46fb82dd9f"
ITEMS = "items"
VIDEO_ARTICLE = "VIDEO"

STORY_URL = "url"
STORY_TITLE = "title"
STORY_CAPTION = "caption"
STORY_SOURCE = "source"
STORY_SCORE = "score"
STORY_TEXT = "text"
STORY_SUMMARY = "summary"
STORY_IMAGE = "image"
STORY_EMBED = "embed" #temporary, used for scoring
PARSER = "html.parser"

ANCHOR_TAG = "a"
HREF_TAG = "href"
PARAGRAPH_TAG = "p"
CAPTION_PROPERTY = "og:description"
IMAGE_PROPERTY = "og:image"
CONTENT_PROPERTY = "content"

PATH_TO_CHROMEDRIVER = "C:\\Users\\Jakob\\Downloads\\chromedriver.exe"

month = {
    1 : "January",
    2 : "February",
    3 : "March", 
    4 : "April",
    5 : "May",
    6 : "June",
    7 : "July",
    8 : "August",
    9 : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}

CACHED_STORIES = "cached_stories.txt"

STATIC_BEGINNING = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html data-editor-version="2" class="sg-campaigns" xmlns="http://www.w3.org/1999/xhtml">
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
      <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
      <!--[if !mso]><!-->
      <meta http-equiv="X-UA-Compatible" content="IE=Edge">
      <!--<![endif]-->
      <!--[if (gte mso 9)|(IE)]>
      <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
      </xml>
      <![endif]-->
      <!--[if (gte mso 9)|(IE)]>
  <style type="text/css">
    body {width: 600px;margin: 0 auto;}
    table {border-collapse: collapse;}
    table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
    img {-ms-interpolation-mode: bicubic;}
  </style>
<![endif]-->
      <style type="text/css">
    body, p, div {
      font-family: inherit;
      font-size: 14px;
    }
    body {
      color: #000000;
    }
    body a {
      color: #ba1f1f;
      text-decoration: none;
    }
    p { margin: 0; padding: 0; }
    table.wrapper {
      width:100% !important;
      table-layout: fixed;
      -webkit-font-smoothing: antialiased;
      -webkit-text-size-adjust: 100%;
      -moz-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }
    img.max-width {
      max-width: 100% !important;
    }
    .column.of-2 {
      width: 50%;
    }
    .column.of-3 {
      width: 33.333%;
    }
    .column.of-4 {
      width: 25%;
    }
    ul ul ul ul  {
      list-style-type: disc !important;
    }
    ol ol {
      list-style-type: lower-roman !important;
    }
    ol ol ol {
      list-style-type: lower-latin !important;
    }
    ol ol ol ol {
      list-style-type: decimal !important;
    }
    @media screen and (max-width:480px) {
      .preheader .rightColumnContent,
      .footer .rightColumnContent {
        text-align: left !important;
      }
      .preheader .rightColumnContent div,
      .preheader .rightColumnContent span,
      .footer .rightColumnContent div,
      .footer .rightColumnContent span {
        text-align: left !important;
      }
      .preheader .rightColumnContent,
      .preheader .leftColumnContent {
        font-size: 80% !important;
        padding: 5px 0;
      }
      table.wrapper-mobile {
        width: 100% !important;
        table-layout: fixed;
      }
      img.max-width {
        height: auto !important;
        max-width: 100% !important;
      }
      a.bulletproof-button {
        display: block !important;
        width: auto !important;
        font-size: 80%;
        padding-left: 0 !important;
        padding-right: 0 !important;
      }
      .columns {
        width: 100% !important;
      }
      .column {
        display: block !important;
        width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
      }
      .social-icon-column {
        display: inline-block !important;
      }
    }
  </style>
      <!--user entered Head Start--><link href="https://fonts.googleapis.com/css?family=Chivo&display=swap" rel="stylesheet"><style>
body {font-family: 'Chivo', sans-serif;}
</style><!--End Head user entered-->
    </head>
    <body>
      <center class="wrapper" data-link-color="#ba1f1f" data-body-style="font-size:14px; font-family:inherit; color:#000000; background-color:#f3f3f3;">
        <div class="webkit">
          <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#f3f3f3">
            <tr>
              <td valign="top" bgcolor="#f3f3f3" width="100%">
                <table width="100%" role="content-container" class="outer" align="center" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td width="100%">
                      <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td>
                            <!--[if mso]>
    <center>
    <table><tr><td width="600">
  <![endif]-->
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:600px;" align="center">
                                      <tr>
                                        <td role="modules-container" style="padding:0px 0px 0px 0px; color:#000000; text-align:left;" bgcolor="#FFFFFF" width="100%" align="left"><table class="module preheader preheader-hide" role="module" data-type="preheader" border="0" cellpadding="0" cellspacing="0" width="100%" style="display: none !important; mso-hide: all; visibility: hidden; opacity: 0; color: transparent; height: 0; width: 0;">
    <tr>
      <td role="module-content">
        <p></p>
      </td>
    </tr>
  </table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="bb66f67d-14da-4c7c-8edc-afdc4a44eab0" data-mc-module-version="2019-10-22">
    <tbody>
      <tr>
        <td style="padding:13px 20px 18px 20px; line-height:22px; text-align:inherit; background-color:#ffffff;" height="100%" valign="top" bgcolor="#ffffff" role="module-content"><div><div style="font-family: inherit; text-align: center"></div>
<div style="font-family: inherit; text-align: center"><span style="font-size: 48px; color: #a70c0c; font-family: verdana, geneva, sans-serif"><strong>Today in News</strong></span></div><div></div></div></td>
      </tr>
    </tbody>
  </table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="3adb1318-b99a-47a9-b500-3eac6c194949">
    <tbody>
      <tr>
        <td style="padding:0px 0px 15px 0px;" role="module-content" bgcolor="#374785">
        </td>
      </tr>
    </tbody>
  </table>
  """

STATIC_END = """
 <table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="0fab0d29-049a-442d-8faf-5efd102c5669.1">
    <tbody>
      <tr>
        <td style="padding:0px 0px 13px 0px;" role="module-content" bgcolor="374785">
        </td>
      </tr>
    </tbody>
  </table>
  
  
  
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="11a43fa3-79eb-4e9a-9c70-1a95769fb630" data-mc-module-version="2019-10-22">
    <tbody>
      <tr>
        <td style="padding:15px 30px 15px 30px; line-height:20px; text-align:inherit; background-color:#ffffff;" height="100%" valign="top" bgcolor="#ffffff" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="color: #a70c0c; font-size: 14px; font-family: &quot;lucida sans unicode&quot;, &quot;lucida grande&quot;, sans-serif">This email was generated by a bot. Click </span><a href="https://github.com/jdforde/news-email"><span style="color: #a70c0c; font-size: 14px; font-family: &quot;lucida sans unicode&quot;, &quot;lucida grande&quot;, sans-serif"><u>here</u></span></a><span style="color: #a70c0c; font-size: 14px; font-family: &quot;lucida sans unicode&quot;, &quot;lucida grande&quot;, sans-serif"> to view the source code.</span></div>
<div style="font-family: inherit; text-align: center"></div>
<div style="font-family: inherit; text-align: center"><span style="color: #a70c0c; font-size: 14px; font-family: &quot;lucida sans unicode&quot;, &quot;lucida grande&quot;, sans-serif">If you would like to unsubscribe, please click </span><a href="https://urldefense.com/v3/__https:/u22828547.ct.sendgrid.net/wf/unsubscribe?upn=RiqxEcWfNTGhGzN-2BKcYYGKRiPWxiUdNg0JoQ8y3BQpgBzBg8le1a1Fowh59lmbFgVWh6UbTAwE-2BCng0LtxydkcLVQIVHJeqSq-2BrzTLHaOkykDBbn3lxIy0roNi1Y8kmsYYZ0NIP81gVYKNTX2DERvanpSpSMGKlBdwzKJqiEBPMhDemxW0iq2p8oY4QkTD2UEDfqy-2BaYVIuZQX5HUMYhG9cLycywZaRlkWggqE8VBZAxE6v01qODzuns7IZpHM6HtxfaaHaa9XBemQCpDDF9WRvpzV-2BsxBwKeFerJE7cTG4EV6nuegh-2BExfIW-2FUYR5DH47FRYZodd78bB6bchVLfhnAuHxbEXZjGUKDqD-2BaKva9mT4btCFgApBLfkUM-2FMSEXSvCG6OTSHpsaee6FLyLnSJnNLB6PphKo7jdVbgp-2BGctf7f-2BMWpQOtPFM1kw5pmL5Qb5Iwm-2F9l1AsKR6Vu0LEOxGStetLFB2dZ5OqNQqF-2BQtT9KwD4Jrhfq8mFEswrEOHy5H9vmSjZFxksBsTztbBJ4IzrBa5sb97oq8d7Y1dJop-2Bw-2B4uUDrNN-2FoFaeI-2Bgg82__;!!IKRxdwAv5BmarQ!KtcEx4Y7g_n2tX-coHRJlN78fAinfIj92Ih9mtg0lP7Rihiak6oXQa96eVIQy_0$"><span style="color: #a70c0c; font-size: 14px; font-family: &quot;lucida sans unicode&quot;, &quot;lucida grande&quot;, sans-serif"><u>here</u></span></a><span style="color: #a70c0c; font-size: 14px; font-family: &quot;lucida sans unicode&quot;, &quot;lucida grande&quot;, sans-serif">.</span></div><div></div></div></td>
      </tr>
    </tbody>
  </table></td></td>
                                      </tr>
                                    </table>
                                    <!--[if mso]>
                                  </td>
                                </tr>
                              </table>
                            </center>
                            <![endif]-->
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </div>
      </center>
    </body>
  </html>
"""