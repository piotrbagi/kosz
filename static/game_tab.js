const btnHome = document.getElementById('home')
const btnAway = document.getElementById('away')
const tabHome = document.getElementById('home-tab')
const tabAway = document.getElementById('away-tab')

btnAway.addEventListener('click',e=>{
    btnAway.classList.add('not-visible')
    btnHome.classList.remove('not-visible')
    tabHome.classList.add('not-visible')
    tabAway.classList.remove('not-visible')
})

btnHome.addEventListener('click',e=>{
    btnHome.classList.add('not-visible')
    btnAway.classList.remove('not-visible')
    tabAway.classList.add('not-visible')
    tabHome.classList.remove('not-visible')
})