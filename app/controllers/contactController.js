import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';
import nodemailer from 'nodemailer';
import { config } from '../utils/config.js';

// POST Handler: Processes Contact Form Submission
export async function handleContactForm(req, res) {
  const { name, email, subject, message } = req.body;

  // Step 1: Validate form input
  if (!name || !email || !subject || !message) {
    return res.status(400).send('Alle Felder müssen ausgefüllt sein.');
  }

  // Step 2: Create the mail transporter using Mailjet SMTP
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

  // Step 3: Define email content
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

  // Step 4: Attempt to send the email
  try {
    await transporter.sendMail(mailOptions);
    res.send('Vielen Dank! Ihre Nachricht wurde erfolgreich versendet.');
  } catch (error) {
    console.error('Fehler beim E-Mail-Versand:', error);
    res.status(500).send('Beim Versenden der Nachricht ist ein Fehler aufgetreten.');
  }
}

// GET Handler: Renders Contact Page
export function renderContactPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/contact.ejs', import.meta.url)),
    getLanguageMessages(req.lang)
  );
}
