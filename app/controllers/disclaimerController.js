import { renderLocalizedView } from './defaultController.js';

export function renderDisclaimer(req, res) {
  const contextPath = process.env.APP_BASE_PATH || '/';
  const lang = req.lang;
  const nextUrl = `${contextPath}${lang}/donate`;

  renderLocalizedView(req, res, 'disclaimer', { nextUrl, contextPath });
}

export function acceptDisclaimer(req, res) {
  const redirectTo = req.body.nextUrl || `/${req.lang}/donate`;
  console.log('✅ AcceptDisclaimer: redirecting to', redirectTo);
  res.cookie('ageConfirmed', 'true', { maxAge: 3600000, httpOnly: true });
  res.redirect(302, redirectTo);
}