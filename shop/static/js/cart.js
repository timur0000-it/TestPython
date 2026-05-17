function getCookie(name){
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')
    return m ? decodeURIComponent(m.pop()) : ''

}

csrftoken = getCookie('csrftoken')
all_buttons = document.querySelectorAll('.btn')
function plus_minus(btn){
    const url = btn.dataset.url;
        
        btn.disabled = true;
        fetch(url, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken}
        })
        .then(resp => {
            if (!resp) return 0
            else return resp.json()
        })
            .then(json => {
                if (!json.status){
                    return 0
                }
                else if(json.status === 'not'){
                     const product_id = json.product_id
                     const qua = json.qua
                     console.log(qua);
                     if(qua < 1 || !qua){
                        const deleteBtn = document.getElementById(`minus ${product_id}`)
                        deleteBtn.remove()
                        const qunt = document.getElementById(`qunt ${product_id}`)
                        qunt.remove()

                     }
                     else{
                     const qunt = document.getElementById(`qunt ${product_id}`)
                     qunt.textContent = String(qua)
                     }
                }
                    
            })
        .finally(()=> {btn.disabled = false})

}
all_buttons = document.querySelectorAll('.btn')
all_buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        const url = btn.dataset.url;
        
        btn.disabled = true;
        fetch(url, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken}
        })
        .then(resp => {
            if (!resp) return 0
            else return resp.json()
        })
            .then(json => {
                if (!json.status){
                    return 0
                }
                else if(json.status === 'ok'){
                     const product_id = json.product_id
                     const qua = json.qua
                     console.log(qua);
                     if(qua == 1){
                        const deleteBtn = document.createElement('button')
                        deleteBtn.textContent = "➖"
                        deleteBtn.setAttribute('data-url', `/shop/minus_cart/${product_id}`)
                        deleteBtn.setAttribute('id',`minus ${product_id}`)
                        deleteBtn.setAttribute('class',`btn`)
                        deleteBtn.addEventListener("click", () => {
                        plus_minus(deleteBtn)
                    })
                        const qunt = document.createElement('p')
                        qunt.setAttribute('id',`qunt ${product_id}`)
                        qunt.textContent = String(qua)
                        const list = document.getElementById(`ono ${product_id}`)
                        list.appendChild(qunt)
                        list.appendChild(deleteBtn)
                        

                     }
                     else{
                     const qunt = document.getElementById(`qunt ${product_id}`)
                     qunt.textContent = String(qua)
                     }
                }
                else if(json.status === 'not'){
                     const product_id = json.product_id
                     const qua = json.qua
                     console.log(qua);
                     if(qua < 1 || !qua){
                        const deleteBtn = document.getElementById(`minus ${product_id}`)
                        deleteBtn.remove()
                        const qunt = document.getElementById(`qunt ${product_id}`)
                        qunt.textContent=' '

                     }
                     else{
                     const qunt = document.getElementById(`qunt ${product_id}`)
                     qunt.textContent = String(qua)
                     }
                }
                    
            })
        .finally(()=> {btn.disabled = false})
    })
});
