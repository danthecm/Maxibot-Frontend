strategyBtn = document.querySelector("#strategy")
grid_elements = document.querySelectorAll(".grid_st")
ac_elements = document.querySelectorAll(".ac")

remove_element = (array) => {
    array.forEach(element => {
        element.classList.remove("d-block")
        element.classList.add("d-none")
        element.firstElementChild.lastElementChild.value = 0
    })
}

add_element = (array) => {
    array.forEach(element => {
        element.classList.remove("d-none")
        element.classList.add("d-block")
        element.firstElementChild.lastElementChild.value = ""
    })
}

toggleStrategy = () => {
    console.log(strategyBtn.value)
    if (strategyBtn.value == "Grid") {
        add_element(grid_elements)
        remove_element(ac_elements)
    }
    else {
        add_element(ac_elements)
        remove_element(grid_elements)
    }
}

strategyBtn.addEventListener("change", toggleStrategy)