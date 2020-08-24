/* Copyright 2020 University Of Delhi.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*   http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/


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