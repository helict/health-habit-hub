  /**
   * Frontend: Changes the application's language by sending the selected language to the server.
   *
   * This function creates a JSON object (data) and  calls 'sendLanguage' to send this data to the backend.
   *
   * @param {string} lang - The language code to set the application to (e.g., 'en', 'de').
   */ 
  function changeLanguage(lang) {
  const data = {
      language: lang
      }
      sendLanguage(data)
  }

  /**
   * Frontend: Sends the language data (JSON) to the backend to update the application's language setting.
   *
   * This function sends a POST request to '/clang' with the language data in JSON format.
   * After that it handles the backend response by logging the success message or any errors.
   *
   * @param {object} data - An object containing the language data to be sent to the backend.
   */
  function sendLanguage(data) {
    fetch('/clang', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  }