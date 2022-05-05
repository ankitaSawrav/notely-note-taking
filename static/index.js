function ShowOnlyMyNotes() {
navTags = document.getElementsByTagName('nav')
console.log(navTags)
const e = document.getElementsByClassName("user")
console.log(e)
    // childrenOfNavTag = navtag.children[0];
    // console.log(childrenOfNavTag)
    // if (childrenOfNavTag.hasAttribute('class')) {
    //     console.log("found")
        loggedInUserId = document.getElementsByClassName("user")[0]
    //     console.log(loggedInUserId)

        if (e && loggedInUserId.getAttribute("u-id")) {
            userID = loggedInUserId.getAttribute("u-id")
            console.log(userID)
                checkboxvalue = document.getElementById("check")
                console.log(checkboxvalue)

                notes_elements = document.getElementsByClassName('notes')
                for (note_element of notes_elements) {
                    const elementUid = note_element.dataset['uid']
                    console.log(elementUid)
                    if(elementUid != userID){
                        console.log(':<')
                    }

                    if (checkboxvalue.checked == true && elementUid !== userID) {
                        
                        note_element.style.display = "none";
                    } else {
                        note_element.removeAttribute("style");
                    }
                }
        }
        // }

}