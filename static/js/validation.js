const emailEl = document.querySelector("input[name=email]")
const passwordEl = document.querySelector("input[name=password]")
const fileEl = document.querySelector("input[name=excel_file]")
const submit_buttonEl = document.querySelector("button[type=submit]")
const formEl = document.querySelector("#form")
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
const mobileRegex = /^([0-9]{10})$/;
let isValidEmail = false
let isValidContact = false
let isValidPassword = false
let isValidFile = false



emailEl.addEventListener("input", function () {
    let value = this.value
    if (value != "") {
       if (!emailRegex.test(value)) {
          this.classList.add("error")
          isValidEmail = false
          checkValidation()
       }
       else {
          this.classList.remove("error")
          checkValidation()
          isValidEmail = true
       }
    }
    else {
       if (this.classList.contains("error")) {
            this.classList.remove("error")
            checkValidation()
            isValidEmail = false
       }
    }
 })


emailEl.addEventListener("input", function () {
    let value = this.value
    if (value != "") {
       if (!mobileRegex.test(value)) {
          this.classList.add("error")
          isValidContact = false
          checkValidation()
       }
       else {
          this.classList.remove("error")
          isValidContact = true
          checkValidation()
       }
    }
    else {
       if (this.classList.contains("error")) {
          this.classList.remove("error")
          checkValidation()
          isValidContact = false
       }
    }
 })

passwordEl.addEventListener("input", function () {
    let value = this.value
    if (value != "") {
       if (!passwordRegex.test(value)) {
          isValidPassword = false
          checkValidation()
          this.classList.add("error")
       }
       else {
          this.classList.remove("error")
          isValidPassword = true
          checkValidation()
       }
    }
    else {
       if (this.classList.contains("error")) {
          this.classList.remove("error")
          isValidPassword = false
          checkValidation()
       }
    }
})

fileEl.addEventListener("input",function(event){
    let value = this.value
    if(!value.endsWith(".xlsx")){
        alert("Please upload excel file mf")
        isValidFile = false
        this.value = ""
        checkValidation()
        this.classList.add("error")
    }
    else{
        isValidFile = true
        checkValidation()
        this.classList.remove("error")
    }
})

function checkValidation() {
    if ((isValidEmail || isValidContact) && isValidPassword && isValidFile  ) {
      submit_buttonEl.classList.remove("disabled")
    } else {
        submit_buttonEl.classList.add("disabled")
    }
}

formEl.addEventListener("submit",function(){
    alert("Processing...")
    submit_buttonEl.textContent = "Processing..."
})