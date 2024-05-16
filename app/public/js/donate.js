function markSelection(context, editableId) {
  let editable = document.getElementById(editableId);
  let selection = window.getSelection();
  if (
    !editable.contains(selection.anchorNode) ||
    !editable.contains(selection.focusNode)
  ) {
    // Selection is not exclusively in the editable div
    return;
  }
  // Wrap selected text in a span
  let mark = document.createElement("mark");
  mark.className = `mark_${context}`;
  range = selection.getRangeAt(0);

  if (range.startContainer.parentNode.nodeName === "MARK") {
    // Cannot use setStartAfter because https://issues.chromium.org/issues/41239578
    range.setStart(range.startContainer.parentNode.nextSibling, 0);
  }
  if (range.endContainer.parentNode.nodeName === "MARK") {
    // Cannot use setEndBefore because https://issues.chromium.org/issues/41239578
    range.setEnd(
      range.endContainer.parentNode.previousSibling,
      range.endContainer.parentNode.previousSibling.length
    );
  }
  if (
    range.startContainer === range.endContainer &&
    range.startContainer.parentNode === editable
  ) {
    range.surroundContents(mark);
    cleanUp(editable);
  }
  console.log(editable.innerHTML);
}

function cleanUp(editable) {
  // merge all child nodes of editable which are identical if they immediately follow each other
  // remove empty text nodes
  removeEmptyTextNodes(editable);
  let children = editable.childNodes;
  let i = 0;
  while (i < children.length) {
    let current = children[i];
    let next = children[i + 1];
    console.log(current, next);
    if (
      next &&
      current.nodeName === next.nodeName &&
      current.className === next.className
    ) {
      current.append(next.innerHTML);
      next.remove();
    } else {
      i++;
    }
  }
}

function removeEmptyTextNodes(editable) {
  let children = editable.childNodes;
  for (let i = 0; i < children.length; i++) {
    let current = children[i];
    if (
      current.nodeType === Node.TEXT_NODE &&
      current.textContent.trim() === ""
    ) {
      current.remove();
    }
  }
}

function removeAllHighlights(editableId) {
  let editable = document.getElementById(editableId);
  editable.innerHTML = editable.innerText;
}
