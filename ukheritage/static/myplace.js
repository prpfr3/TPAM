const backBtn = document.getElementById('back-btn')
const url = window.location.href
const spinnerBox = document.getElementById('spinner-box')

backBtn.addEventListener('click', ()=>{
    history.back()
})

$.ajax({
    type: 'GET',
    url: url,
    success: function(response){
        console.log(response)
        const data = response.data

        if (data.logged_in !== data.author) {
            console.log('different')
        } else {
            console.log('the same')
        }

        spinnerBox.classList.add('not-visible')
    },
    error: function(error){
        console.log(error)
    }
})