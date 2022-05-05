
loggedInUserId = document.getElementsByClassName("user")[0]
userID = loggedInUserId.getAttribute("u-id")
function ShowOnlyMyNotes(){
    checkboxvalue = document.getElementById("check")

    notes_elements = document.getElementsByClassName('notes')
    for (note_element of notes_elements){
        const elementUid =note_element.dataset['uid']

        if (checkboxvalue.checked == true && elementUid !== userID ){
            note_element.style.display = "none";
        }else {
            note_element.removeAttribute("style");
        }
    }   
}