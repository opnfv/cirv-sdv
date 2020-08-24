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

function getModel(){

  config = {}

  // Get current values from form
  for(category of document.getElementsByClassName('resmodData'))
      config = mergeDeep(config, objectifyDiv(category));

  requestModel(config);
}

function requestModel(config){

  form = document.getElementById('validate');
  form.elements['config'].value = JSON.stringify(config);
  form.submit();
}


