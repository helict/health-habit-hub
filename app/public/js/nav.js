/**
 * Frontend: Changes the application's language by sending the selected language to the server.
 *
 * This function changes the language parameter in the current url with the selected value and links to the new url.
 *
 * @param {string} lang - The language code to set the application to (e.g., 'en', 'de', 'ja').
 */
function changeLanguage(lang) {
  console.log('Changing Language to:', lang);
  const targetUrl = window.location.pathname.replace(
    /\/\w{2}\//,
    '/' + lang + '/'
  );
  console.log('new URL:', targetUrl);
  window.location.href = targetUrl;
}
