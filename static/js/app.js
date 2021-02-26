// select modal-btn,modal-overlay,close-btn
// listen for click events on modal-btn and close-btn
// when user clicks modal-btn add .open-modal to modal-overlay
// when user clicks close-btn remove .open-modal from modal-overlay
const modalBtn = document.querySelector(".modal-btn");
const closeBtn = document.querySelector(".close-btn");
const modal = document.querySelector(".modal-overlay");
const my_Form = document.getElementById("form")
const modalToggle = () => modal.classList.toggle("open-modal");
const btn = document.querySelector("#run");
const run = document.querySelector("#running")

console.log("starting")

btn.addEventListener("click", (e) => {
    e.preventDefault();
    attrib = run.getAttribute("hidden")
    console.log(attrib)
    run.removeAttribute("hidden");
    console.log(my_Form);
    my_Form.submit();
    console.log("done");
    modal.classList.remove("open-modal")
    let inputs = document.querySelectorAll("input")
    console.log("done")
    inputs.forEach(element => {
        element.value = ""
    });
    
})

modalBtn.addEventListener("click", modalToggle)

closeBtn.addEventListener("click", modalToggle)

