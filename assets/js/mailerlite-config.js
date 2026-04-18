/*
  MailerLite form configuration.
  Johan updates this file after creating his MailerLite account + embedded form.

  To configure:
  1. In MailerLite dashboard → Forms → Embedded forms → create a form for "AI Guide Subscribers"
  2. Open the form HTML → find the <form action="..."> URL — that's formAction
  3. The field names are standard: fields[email], fields[name], fields[requested_guide]
     (the custom field "Requested Guide" must be added to the form in MailerLite)

  Until configured: submissions fall back to direct download (user still gets the PDF,
  but no email capture happens).
*/

export const MAILERLITE = {
  // Replace XXXXXX/YYYYYY with the real account/form IDs from MailerLite
  formAction: 'https://assets.mailerlite.com/jsonp/XXXXXX/forms/YYYYYY/subscribe',
  configured: false, // set to true once real formAction is in place
  fields: {
    email: 'fields[email]',
    name:  'fields[name]',
    guide: 'fields[requested_guide]',
  },
};
