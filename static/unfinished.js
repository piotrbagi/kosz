const RoundInput = document.getElementById('recent-rounds')
const gameList = document.getElementById('fix-round-list')

RoundInput.addEventListener('change', e=>{
    const val = e.target.value
    gameList.innerHTML = ''
    $.ajax({
        type: 'GET',
        url: `/fix-round-games/${val}/`,
        success: function (response){
            console.log(response.data)
            const items = response.data
            items.map(item=>{
                val1 = document.createElement('div')
                val1.setAttribute('style', 'color: dodgerblue' )
                val1.setAttribute('class', 'header' )
                val1.textContent = `${item.home} n:n ${item.away}`
                val11 = document.createElement('div')
                val11.setAttribute('style', 'color: darkgrey')
                val11.textContent = `${item.data}`
                val1.appendChild(val11)
                val2 = document.createElement('div')
                val2.setAttribute('class', 'content')
                val3 = document.createElement('div')
                val3.setAttribute('class', 'right floated content')
                val4 = document.createElement('div')
                val4.setAttribute('class', 'ui blue button')
                val4.setAttribute('onclick', `location.href='http://127.0.0.1:8000/game/${item.id}/'` )
                val4.textContent = 'Game'
                if (item.regis == true){
                    val41 = document.createElement('div')
                    val41.setAttribute('class', 'ui yellow button')
                    val41.setAttribute('onclick', `location.href='${item.edit_game}'`)
                    val41.textContent = 'Edit Game'
                    val42 = document.createElement('div')
                    val42.setAttribute('class', 'ui red button')
                    val42.setAttribute('onclick', `location.href='${item.delete_game}'`)
                    val42.textContent = 'Delete Game'
                    val43 = document.createElement('div')
                    val43.setAttribute('class', 'ui green button')
                    val43.setAttribute('onclick', `location.href='${item.record_game}'`)
                    val43.textContent = 'Start Game'
                    val3.appendChild(val4)
                    val3.appendChild(val41)
                    val3.appendChild(val42)
                    val3.appendChild(val43)
                }
                else {
                    val3.appendChild(val4)
                }
                val5 = document.createElement('div')
                val5.setAttribute('class', 'item')
                val3.appendChild(val4)
                val5.appendChild(val3)
                val5.appendChild(val2)
                val5.appendChild(val1)
                gameList.appendChild(val5)
            })
        },
        error: function (error){
            console.log(error)
        }
    })
})


