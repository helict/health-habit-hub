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
      range.startOffset
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

  // Create new mark element
  const mark = document.createElement('mark');
  mark.className = `mark_${context}`;
  mark.textContent = selectedText;
  range.deleteContents();
  range.insertNode(mark);
}

function removeAllHighlights(editable) {
  editable.innerHTML = editable.innerText;
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
    sendData(data, language);
  } else {
    // Better error handling
    const errorMessageElement = document.getElementById('error-messages');
    const errorTextElement = document.getElementById('error-text');
    errorMessageElement.style.display = 'block';

    if (inputValidity.empty) {
      errorTextElement.textContent = DONATE_ERRORS.emptyFieldError;
    } else if (inputValidity.noBehavior) {
      errorTextElement.textContent = DONATE_ERRORS.emptyBehaviorError;
    } else if (!CaptchaSuccesful) {
      errorTextElement.textContent = DONATE_ERRORS.noCaptchaError;
    }
  }
}

function sendData(data, language) {
  console.log('Sending data to database');
  console.debug(data);

  // Get reCAPTCHA response token
  const recaptchaResponse = grecaptcha.getResponse();

  // Add reCAPTCHA token to data
  const dataWithCaptcha = {
    ...data,
    'g-recaptcha-response': recaptchaResponse
  };

  fetch('donate/data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(dataWithCaptcha),
  })
    .then((response) => {
      if (response.ok) {
        window.location.href = response.url;
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
  console.debug(editable);
  const habitText = editable.innerText;
  const habitStrength = document.getElementById('habitStrength').value;
  const habitData = {
    inputValue: habitText,
    experimentGroup: experimentGroup,
    language: language,
    contexts: getContexts(editable),
    habitStrength: habitStrength
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
  console.debug(contexts);
  return contexts;
}

function validate(data) {
  console.debug(data);
  return {
    empty: data.inputValue === '',
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

// Add event listeners
function addDonateEventListeners(
  editableId,
  submitButtonId,
  resetButtonId,
  contextIds,
  experimentGroup,
  language,
  grecaptcha
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

  contextIds.forEach((contextId) => {
    document.getElementById(contextId)?.addEventListener('click', () => {
      markSelection(contextId, editable);
    });
  });
}
