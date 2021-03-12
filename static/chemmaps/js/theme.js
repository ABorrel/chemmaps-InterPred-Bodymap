function ShowLoading(e) {
    var div = document.createElement('div');
    var img = document.createElement('img');
    img.src = "https://sandbox.ntp.niehs.nih.gov/static_chemmaps/chemmaps/img/LOADING.gif";
    //img.style.display = "";
    div.innerHTML = 'Loading....';
    div.appendChild(img);
    div.style.cssText =
        'position: fixed; top: 25%; left: 40%; z-index: 5000; width: 300px; background:#000; height: 180px; text-align: center; color:#FFF;';

    document.body.appendChild(div);
    return true;
    // These 2 lines cancel form submission, so only use if needed.
    //window.event.cancelBubble = true;
    //e.stopPropagation();
}
