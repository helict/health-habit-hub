    function changeLanguage(lang) {
    const data = {
        language: lang
        }
        sendLanguage(data)
    }
    
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