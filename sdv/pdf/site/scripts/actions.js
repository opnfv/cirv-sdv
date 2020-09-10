
// expand-arrow button
function toggleClass(element, classname){
  element.classList.toggle(classname)
}

// Add button
function duplicate(button){
  if (button.previousElementSibling.hasAttribute('name') && 
      button.previousElementSibling.getAttribute('name') != null)
  {
      newdiv = button.previousElementSibling.cloneNode(true);
      if (!newdiv.lastElementChild.classList.contains('del-button')){
        del ='<div class="del-button" onclick="remove(this)"></div>'
        newdiv.innerHTML += del;
      }
      button.parentNode.insertBefore(newdiv, button)
  }
}

// Delete Button
function remove(button){
  button.parentNode.parentNode.removeChild(button.parentNode);
}