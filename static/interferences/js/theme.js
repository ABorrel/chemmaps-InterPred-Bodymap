function ShowLoadingInterferences(e) {
    var div = document.createElement('div');
    var img = document.createElement('img');
    img.src = 'https://sandbox.ntp.niehs.nih.gov/static_chemmaps/interferences/img/loading.gif';
    //img.style.display = "";
    div.innerHTML = 'Loading....';
    div.appendChild(img);
    div.style.cssText =
        'position: fixed; top: 25%; left: 40%; z-index: 5000; width: 300px; background:#fff; height: 180px; text-align: center; color:#000;';

    document.body.appendChild(div);
    return true;
    // These 2 lines cancel form submission, so only use if needed.
    //window.event.cancelBubble = true;
    //e.stopPropagation();
}


function alertSubmit(form) {
    var txt;
    if (confirm("Please note by default a new chemical not included in the DSSTOX database will be add at our intern database for reproduction/speed purposes.\n")) {
        form.submit();
    } 
  }
