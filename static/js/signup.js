const submitdata = document.querySelector(".submit-btn")
const name =  document.querySelector("#name")
const loader = document.querySelector('.loader')
const password =  document.querySelector("#password")
const tr_co = document.querySelector("#terms-and-cond")
form = document.querySelector("form")

let handleSubmit = async(e) => {
    e.preventDefault()
}    

submitdata.addEventListener('click',() => {
    if(password.value.length < 8){
        showAlert('password must be mor than 8')
        form.addEventListener('submit',handleSubmit)
    }else if(name.value.length <= 3){
        showAlert('name must be mor than 3')
        form.addEventListener('submit',handleSubmit)
    }else if(!tr_co.checked){
        showAlert('you must agree first')
        form.addEventListener('submit',handleSubmit)
    }else{
        loader.style.display = 'block'
    }
})

const showAlert = (msg) => {
    let alertBox  =document.querySelector(".alert-box")
    let alertMsg = document.querySelector(".alert-msg")
    alertMsg.innerHTML = msg
    alertBox.classList.add('show')
    setTimeout(()=>{
        alertBox.classList.remove('show')
        location.reload()
    },3000)
}


function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");

    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if not found
    return null;
}


function uuidv4(){
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,function(c){
        var r = Math.random()*16 |0 , v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16)
    })
}

let device = getCookie('device')
if (device == null || device == undefined){
    device = uuidv4()
}
document.cookie = 'device=' + device + ";domine=;path=/"