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
