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
