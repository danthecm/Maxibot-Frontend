sumbit = document.querySelector("#submit")

const checkLength = (field) => {
    data = field.value
    if(data.length < 10){
        return `${data} is to short`
    }
    else{
        return true
    }

}

// sumbit.addEventListener("click", (e) => {
//     e.preventDefault()
//     full_name = document.querySelector("#name")
//     full_name = full_name.value
//     if(full_name.length < 5){
//     console.log("YOur full name is to short")
//     }
    
// })