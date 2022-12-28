function toggleHighlightSearchbox(box) {
    if(box.parentElement.classList.contains("highlighted")) {
        box.parentElement.classList.remove("highlighted");

        if(typeof  hideAutocomplete !== "undefined")
            setTimeout(() => hideAutocomplete(), 100);
    }
    else {
        box.parentElement.classList.add("highlighted");
        let searchField = document.getElementById("search");

        if(searchField.value.length > 0) {
            let autocomplete = document.getElementById("autocomplete");
            if(autocomplete)
                autocomplete.style.display = "block";
        }
    }
}

function scrollUpToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

window.onscroll = scrollFunction;
function scrollFunction() {
    let goTop = document.getElementById("gotop");

    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20)
        goTop.style.display = "block";
    else
        goTop.style.display = "none";
}
