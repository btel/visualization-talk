var svgDocument;

function on_load(evt){
   O=evt.target;
   svgDocument=O.ownerDocument;
}

function uncheck(evt) {
    check_box = evt.currentTarget;
    check_mark = check_box.getElementsByTagName("path")[0];

    visibility = check_mark.style.display;

    if (visibility=='none')
    {
        check_mark.style.display='inline';
    }
    else {
        check_mark.style.display='none';
    }
}
