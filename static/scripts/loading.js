function loading() {
    const prompt = document.getElementById('prompt'); 

    if (prompt.value == ""){
        console.log("Prompt is empty");
        prompt.style.borderColor = 'red';
        return false;
    } else {
        console.log("Loading...");
        const loadButton = document.getElementById('loadingBtn'); 
        const loading = document.getElementById('loading'); 
    
        // Disable button and prevent further clicks 
        loadButton.disabled = true; 
        loading.style.display = 'inline-block';
        return true;
    }
}