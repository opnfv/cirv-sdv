/**
 * This function creates a Json file to support client-side file download
 */

function createjson() {
    element=document.getElementById('pdfform')
    data = objectifyDiv(element);
    jsonstr = JSON.stringify(data);
    var data = new Blob([jsonstr], {type: 'application/json'});
    var url = window.URL.createObjectURL(data);
    document.getElementById('download_link').href = url;
    console.log(jsonstr);
}
