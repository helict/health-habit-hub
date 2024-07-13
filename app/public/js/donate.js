function getCurrentPageLanguage() {
  return document.documentElement.lang;
}

function markSelection(context, editable) {
  const selection = window.getSelection();

  if (
    !editable.contains(selection.anchorNode) ||
    !editable.contains(selection.focusNode)
  ) {
    // Selection is not exclusively in the editable div
    return;
  }

  const range = selection.getRangeAt(0);
  const selectedText = range.toString();

  // Truncate overlapping highlights
  const startParent = range.startContainer.parentNode;
  if (startParent !== editable) {
    startParent.textContent = startParent.textContent.substring(
      0,
      range.startOffset,
    );
    // Cannot use setStartAfter because https://issues.chromium.org/issues/41239578
    range.setStart(startParent.nextSibling, 0);
  }

  const endParent = range.endContainer.parentNode;
  if (endParent !== editable) {
    endParent.textContent = endParent.textContent.substring(range.endOffset);
    // Cannot use setEndBefore because https://issues.chromium.org/issues/41239578
    range.setEnd(endParent.previousSibling, endParent.previousSibling.length);
  }

  const contextObj = contexts.find((c) => c.id === context);

  // Create new mark element
  const mark = document.createElement('mark');
  mark.className = `mark_${context}`;
  mark.textContent = selectedText;
  if (contextObj && contextObj.color) {
    mark.style.backgroundColor = contextObj.color; // Set the background color
  }
  range.deleteContents();
  range.insertNode(mark);
}

function removeAllHighlights(editable) {
  // This assumes `editable` is the contentEditable area where highlights are made
  const marks = editable.querySelectorAll('mark');
  marks.forEach((mark) => {
    // Replace each mark element with its text content
    const textNode = document.createTextNode(mark.textContent);
    mark.parentNode.replaceChild(textNode, mark);
  });
}

/**
 * Ensures that the editable contains only non-nested MARK elements as children
 * by removing all other markup.
 */
function cleanUpHabitInput(editable) {
  // remove all markup other than first-level mark elements
  editable.innerHTML = DOMPurify.sanitize(editable.innerHTML, {
    ALLOWED_TAGS: ['mark'],
    ALLOWED_ATTR: ['class'],
  });

  for (const child of editable.children) {
    child.innerHTML = child.textContent;
  }
}

/**
 * Validate habit data from <var>editable</var> and submit it to the server if valid.
 */
function submitHabit(editable, experimentGroup, language, grecaptcha) {
  cleanUpHabitInput(editable);

  const data = parseInput(editable, experimentGroup, language);
  const inputValidity = validate(data);
  const CaptchaSuccesful = checkCaptcha(grecaptcha);

  if (checkValidity(inputValidity) && CaptchaSuccesful) {
    sendData(data);
  } else {
    // Better error handling
    const errorMessageElement = document.getElementById('error-messages');
    const errorTextElement = document.getElementById('error-text');
    errorMessageElement.style.display = 'block';

    if (inputValidity.empty) {
      errorTextElement.textContent = 'Das Feld darf nicht leer sein.';
    } else if (inputValidity.noBehavior) {
      errorTextElement.textContent = 'Bitte markieren Sie das Verhalten.';
    } else if (!CaptchaSuccesful) {
      errorTextElement.textContent =
        'Bestätigen Sie, dass Sie kein Roboter sind.';
    }
  }
}

function sendData(data) {
  fetch('donate/data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (response.ok) {
        window.location.href = '/thanks';
        console.log('Data saved successfully.');
      } else {
        alert('Server Error while saving data.');
      }
    })
    .catch((error) => {
      console.error('Error while saving data:', error);
      alert('Error while saving data.');
    });
}

function parseInput(editable, experimentGroup, language) {
  const habitText = editable.innerText;
  const habitData = {
    text: habitText,
    experimentGroup: experimentGroup,
    language: language,
    contexts: getContexts(editable),
  };
  return habitData;
}

function getContexts(editable) {
  const contexts = [];
  for (const mark of editable.querySelectorAll('mark')) {
    const context = {
      name: mark.className.split('_')[1],
      value: mark.innerText,
    };
    contexts.push(context);
  }
  return contexts;
}

function validate(data) {
  return {
    empty: data.text === '',
    noBehavior:
      data.experimentGroup.closedTask &&
      !data.contexts.find((context) => context.name === 'Behavior'),
  };
}

function checkValidity(validity) {
  // return false if the value of at least one property of validity is true,
  // i.e. if there is at least one error.
  return !Object.values(validity).includes(true);
}

function checkCaptcha(grecaptcha) {
  var response = grecaptcha.getResponse();
  if (response.length === 0) {
    // reCAPTCHA nicht bestätigt
    return false;
  }
  return true;
}

function createContextButtons(contexts, language) {
  const buttonContainer = document.querySelector('.button-container');
  if (buttonContainer) {
    buttonContainer.innerHTML = '';
    const editable = document.getElementById('habit-input');

    contexts.forEach((context) => {
      const button = document.createElement('button');
      button.className = `custom-button btn`;
      button.id = context.id;
      button.textContent = context.labels[language];
      button.style.backgroundColor = context.color;
      button.addEventListener('click', () => {
        markSelection(context.id, editable);
      });
      buttonContainer.appendChild(button);
    });
  }
}

// Add event listeners
function addDonateEventListeners(
  editableId,
  submitButtonId,
  resetButtonId,
  experimentGroup,
  language,
  grecaptcha,
) {
  const editable = document.getElementById(editableId);
  const submitButton = document.getElementById(submitButtonId);
  const resetButton = document.getElementById(resetButtonId);

  submitButton.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent form submission for client-side validation
    submitHabit(editable, experimentGroup, language, grecaptcha);
  });

  resetButton?.addEventListener('click', () => {
    console.log('Clear button clicked');
    removeAllHighlights(editable);
  });
}
