window.onresize = onresizewindows;

function onresizewindows() {
    let menu = document.getElementById("menu");
    if(window.getComputedStyle(menu).display == "none") {
        let overlay = document.getElementById("overlay");
        let sidemenu = document.getElementById("sidemenu");
        overlay.style.display = null;
        sidemenu.style.display = null;

        document.body.style.overflow = "auto";
    }
}

function showMenu() {
    let overlay = document.getElementById("overlay");
    let sidemenu = document.getElementById("sidemenu");
    overlay.style.display = "block";
    sidemenu.style.display = "block";

    document.body.style.overflow = "hidden";
}

function hideMenu() {
    let menu = document.getElementById("menu");
    if(window.getComputedStyle(menu).display == "block") {
        let overlay = document.getElementById("overlay");
        let sidemenu = document.getElementById("sidemenu");
        overlay.style.display = "none";
        sidemenu.style.display = "none";
    
        document.body.style.overflow = "auto";
    }
}

let searchIndex = null;

function search(searchField) {
    if(searchIndex == null)
        searchIndex = JSON.parse(document.getElementById("searchIndex").innerHTML);

    let autocomplete = document.getElementById("autocomplete");
    autocomplete.innerHTML = "";

    if(searchField.value.length == 0)
    {
        autocomplete.style.display = null;
        return;
    }

    for (const index of searchIndex) {
        for (const str of index.index) {
            if(str.toLowerCase().includes(searchField.value.toLowerCase())) {
                let beg = str.toLowerCase().indexOf(searchField.value.toLowerCase())

                let part1 = str.substring(0, beg);
                let part2 = str.substring(beg, beg + searchField.value.length);
                let part3 = str.substring(beg + searchField.value.length);

                let str1 = part1 + "<span class='highlight'>" + part2 + "</span>" + part3;

                autocomplete.innerHTML += "<p><a href='#" + index.href + "' onclick='hideAutocomplete()'>" + str1 + "</a></p>";
                break;
            }
        }
    }

    autocomplete.style.display = "block";
}

function hideAutocomplete() {
    let autocomplete = document.getElementById("autocomplete");
    autocomplete.style.display = null;
}