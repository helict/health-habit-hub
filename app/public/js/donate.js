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
  // eslint-disable-next-line no-undef
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
function submitHabit(editable, experimentGroup, language) {
  cleanUpHabitInput(editable);

  const data = parseInput(editable, experimentGroup, language);
  const inputValidity = validate(data);

  if (checkValidity(inputValidity)) {
    sendData(data);
  } else {
    // TODO: better error handling
    if (inputValidity.empty) {
      // Definition of handleEmptyFieldError in script.js
      handleEmptyFieldError();
    } else if (inputValidity.noBehavior) {
      // Definition of handleEmptyBehaviorError in script.js
      handleEmptyBehaviorError();
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
        window.location.href = 'bedankung.html';
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
    noBehavior: !data.contexts.find((context) => context.name === 'Behavior'),
  };
}

function checkValidity(validity) {
  // return false if the value of at least one property of validity is true,
  // i.e. if there is at least one error.
  return !Object.values(validity).includes(true);
}

// Add event listeners
// eslint-disable-next-line no-unused-vars
function addDonateEventListeners(
  editableId,
  submitButtonId,
  resetButtonId,
  contextButtons,
  experimentGroup,
  language,
) {
  const editable = document.getElementById(editableId);
  const submitButton = document.getElementById(submitButtonId);
  const resetButton = document.getElementById(resetButtonId);

  submitButton.addEventListener('click', () => {
    submitHabit(editable, experimentGroup, language);
  });

  resetButton.addEventListener('click', () => {
    removeAllHighlights(editable);
  });

  Object.keys(contextButtons).forEach(function (key) {
    document.getElementById(key).addEventListener('click', function () {
      markSelection(contextButtons[key], editable);
    });
  });
}

// TODO: Rework
function handleEmptyFieldError() {
  fetch('language/language-data.json')
    .then((response) => response.json())
    .then((data) => {
      const fehlerText = data[currentLanguage].emptyFieldError;
      alert(fehlerText);
    })
    .catch((error) =>
      console.error('Error loading language data file:', error),
    );
}

function handleEmptyBehaviorError() {
  fetch('language/language-data.json')
    .then((response) => response.json())
    .then((data) => {
      const fehlerText = data[currentLanguage].emptyBehaviorError;
      alert(fehlerText);
    })
    .catch((error) =>
      console.error('Error loading language data file:', error),
    );
}
