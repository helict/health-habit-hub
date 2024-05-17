function markSelection(context, editableId) {
  const editable = document.getElementById(editableId);
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
  const mark = document.createElement("mark");
  mark.className = `mark_${context}`;
  mark.textContent = selectedText;
  range.deleteContents();
  range.insertNode(mark);
}

function removeAllHighlights(editableId) {
  let editable = document.getElementById(editableId);
  editable.innerHTML = editable.innerText;
}

// Ensure that only first-level mark elements are present in the editable div
function cleanUpEditable(editableID) {
  const editable = document.getElementById(editableID);
  // remove all markup other than first-level mark elements
  editable.innerHTML = DOMPurify.sanitize(editable.innerHTML, {
    ALLOWED_TAGS: ["mark"],
    ALLOWED_ATTR: ["class"],
  });

  for (const child of editable.children) {
    child.innerHTML = child.textContent;
  }
}

function submitData(editableId) {
  cleanUpEditable(editableId);
  const editable = document.getElementById(editableId);
  const data = parseInput(editable);
  console.log(data);
  const inputValidity = validate(data);
  console.log(inputValidity);
  if (checkValidity(inputValidity)) {
    sendData(data);
  } else {
    if (inputValidity.empty) {
      handleEmptyFieldError(); // TODO: better error handling
    } else if (inputValidity.noBehavior) {
      handleEmptyBehaviorError(); // TODO: better error handling
    }
  }
}

function sendData(data) {
  console.log(data); // TODO: send data to server
}

function parseInput(editable) {
  const habitText = editable.innerText;
  const habitData = {
    text: habitText,
    language: "en", // TODO: get language from session
    experimentGroup: {
      // TODO: get actual experiment group
      closedTask: true,
      closedDescription: true,
    },
    contexts: getContexts(editable),
  };
  return habitData;
}

function getContexts(editable) {
  const contexts = [];
  for (const mark of editable.querySelectorAll("mark")) {
    const context = {
      name: mark.className.split("_")[1],
      value: mark.innerText,
    };
    contexts.push(context);
  }
  return contexts;
}

function validate(data) {
  return {
    empty: data.text === "",
    noBehavior: !data.contexts.find((context) => context.name === "Behavior"),
  };
}

function checkValidity(validity) {
  // return false if the value of at least one property of validity is true,
  // i.e. if there is at least one error.
  return !Object.values(validity).includes(true);
}
