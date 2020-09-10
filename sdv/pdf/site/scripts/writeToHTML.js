
/**
* Processes target HTML element and fill with values passed in
* javascript object
*
* @param {element} element to update with values
* @param {obj} Object from which values will be read
*/
  function writeToHTML(element, obj){

    var el = element.childNodes;
    for(var i in el)
    {

        if(el[i] instanceof HTMLInputElement && el[i].hasAttribute('name')){

            if(el[i].type == 'text')
              el[i].value = getValue(obj, el[i].name);

        }
        if(el[i] instanceof HTMLSelectElement && el[i].hasAttribute('name')){

          var option = getValue(obj, el[i].name);
          var defaultValue = el[i].value;
          el[i].value = option;
          if ( el[i].value != option){
              el[i].focus();
              alert(option + " is an invalid value! Setting to default");
              el[i].value = defaultValue;
          }

        }
        if(el[i] instanceof HTMLDivElement){

            if(el[i].hasAttribute('name'))
            {              
                if(el[i].classList.contains('arr')){

                    name = el[i].getAttribute('name');
                    values = getValue(obj, name);

                    // Sync number of Arr div with name inside element with number of values
                    syncArr(element, name, values.length);

                    // Update value inside all divs
                    var i = 0;
                    for(var div of element.getElementsByClassName('arr'))
                      if(div.getAttribute("name") == name)
                        writeToHTML(div , values[i++]);

                } //else-if single div
                else
                    writeToHTML(el[i], getValue(obj, el[i].getAttribute('name')));

            }//else-if blank div without attribute name, then simply pass values to next child
            else
                writeToHTML(el[i], obj);
        }

    }
  }

  // Reads value from obj with string 'key1.key2.key3' convention
  function getValue(obj, str) {
    str = str.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
    str = str.replace(/^\./, '');           // strip a leading dot
    var a = str.split('.');
    for (var i = 0; i < a.length; ++i) {
        var key = a[i];
        if (key in obj) {
            obj = obj[key];
        } else {
            alert('Invalid PDF file! Key '+key+ ' not Found');
            return "";
        }
    }
    return obj;
  }

function syncArr(el, name, length){

  // count number of arr-div with name present inside el
  var count = 0;
  var cp = null;
  for(var div of el.getElementsByClassName('arr')){
    if(div.getAttribute("name") == name){
      count++;
      cp = div;
    }
  }

  // balance loop
  while(count - length){
    if((count - length) < 0)
    { // add more div
      newdiv = cp.cloneNode(true);
      if (!newdiv.lastElementChild.classList.contains('del-button')){
        del ='<div class="del-button" onclick="remove(this)"></div>'
        newdiv.innerHTML += del;
      }
      cp.after(newdiv);
      count++;
    }
    else
    { // remove div
      for(var div of el.getElementsByClassName('arr'))
        if(div.getAttribute("name") == name)
          if (div.lastElementChild.classList.contains('del-button')){
            div.parentNode.removeChild(div);
            count--;
            if((count - length)==0)
              break;
          }
    }
  }

}
