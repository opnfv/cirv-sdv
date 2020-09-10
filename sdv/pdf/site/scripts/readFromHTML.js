
/**
* Reads HTML contents into javascript object
* 
*
* @param {element} element to read, can be input or div element
* @returns {object} New object with values read
*/
function objectifyDiv(element){
  var obj = {};
  var el = element.childNodes;
  for(var i in el){

    if(el[i] instanceof HTMLInputElement && el[i].hasAttribute('name')) {

      if(el[i].type == 'text')
        obj = mergeDeep(obj, objectify(el[i].name, el[i].value));
    
    }
    if(el[i] instanceof HTMLSelectElement && el[i].hasAttribute('name')){
        obj = mergeDeep(obj, objectify(el[i].name, el[i].value));          
    }
    if(el[i] instanceof HTMLDivElement){

      if(el[i].classList.contains('arr')){
        var key = el[i].getAttribute('name');
        var value = objectifyDiv(el[i]);
        if(obj[key] == undefined)
          obj[key] =[];
        obj[key].push(value[key]);
      }
      else
        obj = mergeDeep(obj, objectifyDiv(el[i]));
      
    }
  }
  
  if(element.hasAttribute('name')){
    var newobj = {};
    newobj[element.getAttribute('name')] = obj;
    return newobj;
  }
  return obj;
}



function objectify(key, value){
  var obj = {};
  var keys = key.split('.');
  for(var i = keys.length-1; i >= 0; i--){
    obj[keys[i]] = value;
    value = obj;
    obj = {};
  }
  return value;
}
