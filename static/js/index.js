let container = document.getElementById("container");

toggle = () => {
  container.classList.toggle("sign-in");
  container.classList.toggle("sign-up");
};

setTimeout(() => {
  container.classList.add("sign-in");
}, 200);



    // Get references to the radio buttons and the input text box
const automaticRunRadioButton = document.getElementById("automaticRun");
const timeInput = document.getElementById("timeInput");
const downloadButton = document.querySelector("#download_all");

timeInput.addEventListener("input", function (event) {
  const enteredValue = parseFloat(this.value);
  const minValue = parseFloat(this.min);
  const maxValue = parseFloat(this.max);

  if (enteredValue < minValue) {
    this.value = this.min;
  }

  if (enteredValue > maxValue) {
    this.value = this.max;
  }
});


const radios = document.querySelectorAll("input[name=run_type]")

for (const radio of radios){
  radio.addEventListener("change",function(event){
    if(this.value=="auto" && this.checked){
      timeInput.style.display = "none"
    }
    if(this.value == "seq" && this.checked){
      timeInput.style.display = "block"
    }
  })
}


document.querySelector("#download_all").addEventListener("click", function () {
  const downloadLinks = document.querySelectorAll(".downloadButton");
  downloadLinks.forEach(link => link.click());
});