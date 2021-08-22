# news-email
Python script to scrape news sites and send email of important news articles. Using the dependencies in requirements.txt, it has the following flow:
1. Concurrently scrape news sites for important US and international politics/business stories
2. Scores every story's relevancy based on simple criteria
3. Picks the top 10 most important stories, adds to the "mockup"
4. Generates at most 3 bullet points for each story in the mockup
5. Dynamically places title, caption, and bullet points of stories into HTML skeleton
6. Grabs contacts from SendGrid API and sends out email

Here is the link to signup: 
https://cdn.forms-content.sg-form.com/d96cc00b-f7c0-11eb-be93-9a46fb82dd9f

Project is deployed to AWS and currently **sends out emails Sunday-Thursday**
