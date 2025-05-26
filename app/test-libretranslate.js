import fetch from 'node-fetch';

fetch('http://libretranslate:5000/translate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    q: 'Hallo Welt',
    source: 'de',
    target: 'en',
    format: 'text'
  })
})
.then(res => res.json())
.then(console.log)
.catch(console.error);
