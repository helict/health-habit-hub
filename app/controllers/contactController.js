import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';
import nodemailer from 'nodemailer';
import { config } from '../utils/config.js';
import fetch from 'node-fetch';

// POST Handler: Processes Contact Form Submission
export async function handleContactForm(req, res) {
  const { name, email, subject, message } = req.body;
  const recaptchaToken = req.body['g-recaptcha-response'];

  // Step 1: Validate form input
  if (!name || !email || !subject || !message) {
    return res.status(400).send('Alle Felder müssen ausgefüllt sein.');
  }

  // Step 2: Verify reCAPTCHA
  if (!recaptchaToken) {
    return res.status(400).send('Bitte bestätigen Sie das reCAPTCHA.');
  }

  try {
    const verifyUrl = `https://www.google.com/recaptcha/api/siteverify?secret=${config.recaptcha.secretKey}&response=${recaptchaToken}`;
    const recaptchaResponse = await fetch(verifyUrl, { method: 'POST' });
    const recaptchaData = await recaptchaResponse.json();

    if (!recaptchaData.success) {
      console.error('❌ reCAPTCHA verification failed:', recaptchaData);
      return res.status(400).send('reCAPTCHA-Verifizierung fehlgeschlagen. Bitte versuchen Sie es erneut.');
    }
    console.log('✅ reCAPTCHA verification passed for contact form');
  } catch (error) {
    console.error('❌ Error verifying reCAPTCHA:', error);
    return res.status(500).send('Fehler bei der reCAPTCHA-Verifizierung.');
  }

  // Step 3: Create the mail transporter using Mailjet SMTP
const transporter = nodemailer.createTransport({
  host: 'in-v3.mailjet.com',
  port: 587,
  secure: false, // use STARTTLS
  auth: {
    user: config.mail.user,
    pass: config.mail.pass,
  },
  logger: true, // enable logging for debugging
  debug: true, // include debug output in the console
});

  // Step 4: Define email content
const mailOptions = {
  from: `"HabitHub Contact" <${config.mail.from}>`,   // exact MAIL_FROM from .env
  to: config.mail.receiver,
  replyTo: email,  // the user's email
  subject: `[Kontaktformular] ${subject}`,
  text: `
Neue Nachricht vom Kontaktformular:

Name: ${name}
E-Mail: ${email}
Betreff: ${subject}

Nachricht:
${message}
  `.trim(),
};

  // Step 5: Attempt to send the email
  try {
    await transporter.sendMail(mailOptions);
    res.send('Looking good! Message sent successfully.');
  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).send('Oh oh. There was an error while sending your message. Please try again later.');
  }
}

// GET Handler: Renders Contact Page
export function renderContactPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/contact.ejs', import.meta.url)),
    getLanguageMessages(req.lang)
  );
}
