let load = document.getElementById("load")
let loadform = document.getElementById("loadform")
let inputElement = document.getElementById('inp');




let lo = async () =>{
    
    let text = inputElement.value;
    document.cookie = "prompt=" + text;
    await fetch('/ai');
    console.log(text)
    loadform.innerHTML = " Please wait ..."
    

}

load.addEventListener('click', async () =>{
    await lo().catch(error => {
        console.log("error")
        loadform.innerHTML = " Please wait..."
    })
    
    console.log("??????")
    // loadform.innerHTML = "Please wait..."
    })
