var updateCourier = document.getElementsByClassName('update-courier')

for (i=0; i < updateCourier.length; i++){
    updateCourier[i].addEventListener('click', function(){
        var courier = this.dataset.product
        console.log('courier:', courier)

        console.log('Courier:', courier)
//        if (user == 'AnonymousUser'){
//            console.log('User is not authenticated')
//        }else{
//            updateUserOrder(productId, action)
//        }

    })
}


function updateUserOrder(productId, action){
    console.log('User is logged in, sending data..')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
    })
}
