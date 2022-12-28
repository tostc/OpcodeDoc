function search(searchbox) {
    var cards = document.getElementById("cards");

    var children = cards.children;
    for (var i = 0; i < children.length; i++) {
        var el = children[i];
        if(el.getElementsByClassName("search-card-header")[0].innerHTML.toLowerCase().includes(searchbox.value.toLowerCase()) ||
           el.getElementsByClassName("search-card-content")[0].innerHTML.toLowerCase().includes(searchbox.value.toLowerCase()) )
            el.style.display = "block";
        else
            el.style.display = "none";
    }
}