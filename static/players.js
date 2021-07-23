const searchPlayer = document.getElementById('search-player')
const playersList = document.getElementById('players-list')
const teamBox = document.getElementById('select-team-box')
const teamText = document.getElementById('select-team-text')
const selectTeam = document.getElementById('select-team')

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
selectTeam.addEventListener('change' ,e=>{
    const inpt = e.target.value
    playersList.innerHTML = ''
    $.ajax({
        type: 'GET',
        url: `/search-player-team/${inpt}`,
        success: function (response){
            console.log(response.data)
            results = response.data
            results.map(item=>{
                val1 = document.createElement('div')
            val1.setAttribute('style', 'color: dodgerblue' )
            val1.setAttribute('class', 'header' )
            val1.textContent = `${item.last_name} ${item.first_name}`
            val11 = document.createElement('div')
            val11.setAttribute('style', 'color: darkgrey')
            val11.textContent = `${item.t}| ${item.pkt}/${item.reb}/${item.ast}`
            val1.appendChild(val11)
            val2 = document.createElement('div')
            val2.setAttribute('class', 'content')
            val3 = document.createElement('div')
            val3.setAttribute('class', 'right floated content')
            val4 = document.createElement('div')
            val4.setAttribute('class', 'ui blue button')
            val4.setAttribute('onclick', `location.href='${item.player_url}'`)
            val4.textContent = 'Profile'
            if (item.regis == true){
                val41 = document.createElement('div')
                val41.setAttribute('class', 'ui yellow button')
                val41.setAttribute('onclick', `location.href='${item.edit_player}'`)
                val41.textContent = 'Edit Player'
                val42 = document.createElement('div')
                val42.setAttribute('class', 'ui red button')
                val42.setAttribute('onclick', `location.href='${item.delete_player}'`)
                val42.textContent = 'Delete Player'
                val3.appendChild(val4)
                val3.appendChild(val41)
                val3.appendChild(val42)
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
            playersList.appendChild(val5)
            })
        },
        error: function (error){
            console.log(error)
        }
    })
})
searchPlayer.addEventListener('keyup',e=>{
    const letters = e.target.value
    playersList.innerHTML = ''
    console.log(letters)
    $.ajax({
        type: 'POST',
        url: '/search-player/',
        data:{
            'csrfmiddlewaretoken': csrftoken,
            'word':letters
        },
        success: function (response){
            console.log(response.data)
            results = response.data
            results.map(item=>{
                val1 = document.createElement('div')
            val1.setAttribute('style', 'color: dodgerblue' )
            val1.setAttribute('class', 'header' )
            val1.textContent = `${item.last_name} ${item.first_name}`
            val11 = document.createElement('div')
            val11.setAttribute('style', 'color: darkgrey')
            val11.textContent = `${item.team}| ${item.pkt}/${item.reb}/${item.ast}`
            val1.appendChild(val11)
            val2 = document.createElement('div')
            val2.setAttribute('class', 'content')
            val3 = document.createElement('div')
            val3.setAttribute('class', 'right floated content')
            val4 = document.createElement('div')
            val4.setAttribute('class', 'ui blue button')
            val4.setAttribute('onclick', `location.href='${item.player_url}'` )
            val4.textContent = 'Profile'
                if (item.regis == true){
                val41 = document.createElement('div')
                val41.setAttribute('class', 'ui yellow button')
                val41.setAttribute('onclick', `location.href='${item.edit_player}'`)
                val41.textContent = 'Edit Player'
                val42 = document.createElement('div')
                val42.setAttribute('class', 'ui red button')
                val42.setAttribute('onclick', `location.href='${item.delete_player}'`)
                val42.textContent = 'Delete Player'
                val3.appendChild(val4)
                val3.appendChild(val41)
                val3.appendChild(val42)
            }
            else {
                val3.appendChild(val4)
            }
            val5 = document.createElement('div')
            val5.setAttribute('class', 'item')
            val5.appendChild(val3)
            val5.appendChild(val2)
            val5.appendChild(val1)
            playersList.appendChild(val5)
            })
        },
        error: function (error){
            console.log(error)
        }
    })
})

