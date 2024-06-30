var username = document.getElementById("username_edit");
console.log(username);
function makeEditable() {
    var usernameInput = document.getElementById("username_edit");
    usernameInput.removeAttribute("readonly");
}