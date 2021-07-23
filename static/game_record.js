const buttons = [...document.getElementsByClassName('positive ui button')]
const time = [...document.getElementsByClassName('time')]
const btnStopTimer = document.getElementById('stop-timer')
const btnStartTimer = document.getElementById('start-timer')
const btnResetTimer = document.getElementById('reset-timer')
const clock = document.getElementById('clock')
const btnOt = document.getElementById('ot-timer')
const btnEnd = document.getElementById('end')
const tab = document.getElementById('tab')
const tabAway = document.getElementById('away-tab')
const editBtns = [...document.getElementsByClassName('ui violet button')]
const editStat = document.getElementById('edit-text')
const valStat = document.getElementById('val-text')
const editForm = document.getElementById('edit')
const names = [...document.getElementsByClassName('left')]
const editPlayer = document.getElementById('edit-player')
const gameId = document.getElementById('game_id')
const editId = document.getElementById('edit-id')
const qtime = document.getElementById('qtime')
const qua = document.getElementById('qua')
const ot_time = document.getElementById('ot_time')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const inputStat = document.getElementById('edit-stat')
const valBox = document.getElementById('val_box')
const valText = document.getElementById('val-text')
const editTab = document.getElementById('edit-form')
const pickFive = document.getElementById('plrs')
const btnFive = document.getElementById('btn_home_5')
const btnFiveAway = document.getElementById('btn_away_5')
const textHomeFive = document.getElementById('text_home5')
const textAwayFive = document.getElementById('text_away5')
const pickFiveAway = document.getElementById('five_away')
const otNum = document.getElementById('ot')
const faul = document.getElementById('faul')
let qt = parseInt(qtime.textContent,10)
let clock_min = parseInt(qt / 60, 10 )
let clock_sec = qt % 60
let player_time_sec = 0
let player_time_min = 0
let ot = parseInt(ot_time.textContent, 10)
let last_cell = tab.rows[0].cells.length - 1
let rows = tab.rows.length - 1
let rowsAway = tabAway.rows.length - 1
let q = parseInt(qua.textContent)
let o = parseInt(otNum.textContent)
let game_id = gameId.textContent
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
for (i = 1; i<rows; i++){
    if (tab.rows[i].cells[last_cell].textContent == 'False'){
        tab.rows[i].classList.add('not-visible')
    }
}
for (i = 1; i<rowsAway; i++){
    if (tabAway.rows[i].cells[last_cell].textContent == 'False'){
        tabAway.rows[i].classList.add('not-visible')
    }
}
let _clock_min = clock_min
let _clock_sec = clock_sec
function timer(){
    sum_time = _clock_min * 60 + _clock_sec
    player_time = player_time_min * 60 + player_time_sec
    if (sum_time > 0){
        sum_time -= 1
        game_sec = sum_time % 60
        game_min = parseInt(sum_time / 60, 10)
        _clock_min = game_min
        _clock_sec = game_sec
        if (game_sec<10){
            game_sec = `0${game_sec}`
        }
        clock.textContent = `${game_min}:${game_sec}`
        for (i = 1; i<rows; i++){
            if (tab.rows[i].cells[last_cell].innerHTML == 'True'){
                player_sec = parseInt(tab.rows[i].cells[1].innerHTML) + 1
                tab.rows[i].cells[1].innerHTML = player_sec
            }
        }
        for (i = 1; i<rowsAway; i++){
            if (tabAway.rows[i].cells[last_cell].innerHTML == 'True'){
                player_sec = parseInt(tabAway.rows[i].cells[1].innerHTML) + 1
                tabAway.rows[i].cells[1].innerHTML = player_sec
            }
        }
    }
    if (sum_time == 0 && q< 4){
        btnResetTimer.classList.remove('not-visible')
        btnStopTimer.classList.add('not-visible')
    }
    if (sum_time == 0 && q>=4 && tab.rows[rows].cells[13].innerText==tabAway.rows[rowsAway].cells[13].innerText){
        btnOt.classList.remove('not-visible')
        btnStopTimer.classList.add('not-visible')
    }
    if (sum_time == 0 && q>=4 && tab.rows[rows].cells[13].innerText!=tabAway.rows[rowsAway].cells[13].innerText){
        btnEnd.classList.remove('not-visible')
        btnStopTimer.classList.add('not-visible')
    }
}
btnStartTimer.addEventListener('click', f=>{
    tiktok = setInterval(timer,1000)
    btnStopTimer.classList.remove('not-visible')
    btnStartTimer.classList.add('not-visible')
    faul.textContent = ''
})
btnStopTimer.addEventListener('click', g=>{
    clearInterval(tiktok)
    btnStopTimer.classList.add('not-visible')
    btnStartTimer.classList.remove('not-visible')
    const time_played = {}
        time.forEach(t=>{
            num = t.id
            min = t.textContent
            time_played[num] = min
        })
        console.log(time_played)
        $.ajax({
            type: 'POST',
            url: `/save-time/${game_id}`,
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'mins': JSON.stringify(time_played),
                'timer': clock.textContent
            },
            success: function (response){
                console.log(response.data)
            },
            error: function (error){
                console.log(error)
            }
        })
})
btnResetTimer.addEventListener('click', t=>{
    clearInterval(tiktok)
    q += 1
    btnResetTimer.classList.add('not-visible')
    btnStartTimer.classList.remove('not-visible')
    const time_played = {}
        time.forEach(t=>{
            num = t.id
            min = t.textContent
            time_played[num] = min
        })
    console.log(time_played)
    $.ajax({
        type: 'POST',
        url: `/save-qua/${game_id}`,
        data: {
                'csrfmiddlewaretoken': csrftoken,
                'mins': JSON.stringify(time_played),
                'qua': q
            },
        success: function (response){
            console.log(response.time_reset)
            const time_reset = response.time_reset
            clock_reset_min = parseInt(time_reset / 60, 10)
            clock_reset_sec= time_reset % 60
            _clock_min = clock_reset_min
            _clock_sec = clock_reset_sec
            if (clock_reset_sec < 10){
                clock.textContent = `${clock_reset_min}:0${clock_reset_sec}`
            }
            else{
                clock.textContent = `${clock_reset_min}:${clock_reset_sec}`
            }
            },
        error: function (error){
            console.log(error)
            }
    })
})
btnOt.addEventListener("click", e=>{
    clearInterval(tiktok)
    ot += 1
    q += 1
    btnOt.classList.add('not-visible')
    btnStartTimer.classList.remove('not-visible')
    const time_played = {}
        time.forEach(t=>{
            num = t.id
            min = t.textContent
            time_played[num] = min
        })
        $.ajax({
        type: 'POST',
        url: `/save-ot/${game_id}`,
        data: {
                'csrfmiddlewaretoken': csrftoken,
                'mins': JSON.stringify(time_played),
                'ot': o
            },
        success: function (response){
            console.log(response.time_reset)
            const time_reset = response.time_reset
            clock_reset_min = parseInt(time_reset / 60, 10)
            clock_reset_sec= time_reset % 60
            _clock_min = clock_reset_min
            _clock_sec = clock_reset_sec
            if (clock_reset_sec < 10){
                clock.textContent = `${clock_reset_min}:0${clock_reset_sec}`
            }
            else{
                clock.textContent = `${clock_reset_min}:${clock_reset_sec}`
            }
            },
        error: function (error){
            console.log(error)
            }
    })
})
btnEnd.addEventListener('click',e=>{
    const time_played = {}
        time.forEach(t=>{
            num = t.id
            min = t.textContent
            time_played[num] = min
        })
    $.ajax({
        type: 'POST',
        url: `/the-end/${game_id}`,
        data: {
                'csrfmiddlewaretoken': csrftoken,
                'mins': JSON.stringify(time_played),
            },
        success: function (response){
            console.log(response.time_reset)
            },
        error: function (error){
            console.log(error)
            }
    })
})
buttons.forEach(button=>{
    button.addEventListener('click', e=>{
        upd = parseInt(button.textContent) + 1
        button.textContent = upd
        const time_played = {}
        time.forEach(t=>{
            num = t.id
            min = t.textContent
            time_played[num] = min
        })
        console.log(time_played)
        $.ajax({
            type: 'POST',
            url: `/save-stats/${game_id}/`,
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'stat': button.id,
                'value': button.textContent,
                'mins': JSON.stringify(time_played),
                'timer': clock.textContent
            },
            success: function (response){
                console.log(response.data)
                console.log(response.team_stats)
                const stat = response.data
                stat.map(item=>{
                    if (item.done){
                        if (item.name){
                        const ele = document.getElementById(item.name)
                        upd = parseInt(ele.textContent) + 1
                        ele.textContent = upd
                        if ('pkt_id' in item) {
                            const point = document.getElementById(item.pkt_id)
                            point.textContent = item.pkt
                        }
                        }
                        if ('faul_limit' in item){
                            faul.textContent = `${item.faul_limit}`
                        }
                    }
                })
                const team_stats = response.team_stats
                team_stats.map(team=>{
                    document.getElementById(`PKT  ${team.id}`).textContent = team.PKT
                    document.getElementById(`AST  ${team.id}`).textContent = team.AST
                    document.getElementById(`OREB  ${team.id}`).textContent = team.OREB
                    document.getElementById(`DREB  ${team.id}`).textContent = team.DREB
                    document.getElementById(`TREB  ${team.id}`).textContent = team.TREB
                    document.getElementById(`TO  ${team.id}`).textContent = team.TO
                    document.getElementById(`STL  ${team.id}`).textContent = team.STL
                    document.getElementById(`BLK  ${team.id}`).textContent = team.BLK
                    document.getElementById(`PF  ${team.id}`).textContent = team.PF
                    document.getElementById(`FGM  ${team.id}`).textContent = `${team.FGM}/${team.FGA}`
                    document.getElementById(`FTM  ${team.id}`).textContent = `${team.FTM}/${team.FTA}`
                    document.getElementById(`FGM_three  ${team.id}`).textContent = `${team.FGM_three}/${team.FGA_three}`
                })
            },
            error: function (error){
                console.log(error)
            }
        })
    })
})
editBtns.forEach(editBtn=>{
    editBtn.addEventListener('click', e=>{
        editId.textContent = editBtn.id
        editTab.classList.remove('not-visible')
        names.forEach(name=>{
            if (name.id == editBtn.id){
                editPlayer.textContent = name.textContent
            }
        })
    })
})
inputStat.addEventListener('change',r => {
    const stat = r.target.value
    const edit_pk = editId.textContent
    const stat_val = `${stat} ${edit_pk}`
    const result = parseInt(document.getElementById(stat_val).textContent)
    valText.textContent = 'Value'
    valText.classList.add('default')
    valBox.innerText = ''
    for (step = 0; step < result; step++){
        const opt = document.createElement('div')
        opt.textContent = step
        opt.setAttribute('class', 'item')
        opt.setAttribute('data-value', step)
        valBox.appendChild(opt)
    }
})
editForm.addEventListener('submit', e=> {
    e.preventDefault()
    $.ajax({
        type: 'POST',
        url: `/edit/${game_id}/`,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'value': valStat.textContent,
            'stat': editStat.textContent,
            'player_id': editId.innerText
        },
        success: function (response){
            console.log(response.data)
            const ress = response.data
            ress.map(res=>{
                if ('pkt' in res){
                    const point = document.getElementById(res.pkt)
                    point.textContent = res.pkt_value
                    const fa = document.getElementById(res.name2)
                    fa.textContent = res.value2
                    const ts_pkt = document.getElementById(res.ts_pkt_id)
                    ts_pkt.textContent = res.ts_pkt_val
                    const ts_ss = document.getElementById(res.ts_id2)
                    ts_ss.textContent = res.ts_val2
                }
                if ('treb' in res){
                    const reb = document.getElementById(res.treb)
                    reb.textContent = res.treb_value
                    const ts_reb = document.getElementById(res.ts_treb_id)
                    ts_reb.textContent = res.ts_treb_val
                }
                if (!('pkt' in res)||!('treb' in res)){
                    const nm = document.getElementById(res.name1)
                    nm.textContent = res.valu
                    const ts_nm = document.getElementById(res.ts_id)
                    ts_nm.textContent = res.ts_val
                }
            })
        },
        error: function (error){
            console.log(error)
        }
    })
})

pickFive.addEventListener('change', e=>{
    ids =e.target.value
    arr_ids = ids.split(',')
    if (arr_ids.length != 5){
        btnFive.classList.add('not-visible')
        textHomeFive.textContent = ids
    }
    else{
        btnFive.classList.remove('not-visible')
        textHomeFive.textContent = ids
    }
})
btnFive.addEventListener('click', e=>{
    $.ajax({
        type: 'GET',
        url: `/start-five/${textHomeFive.textContent}/`,
        success: function (response){
            console.log(response)
            out = response.data
            btnFive.classList.add('not-visible')
            out.map(item=>{
                if(item.on_court == true){
                    for (j = 1; j < rows; j++) {
                    if (tab.rows[j].id == item.id) {
                        tab.rows[j].classList.remove('not-visible')
                        tab.rows[j].cells[last_cell].innerHTML = 'True'
                    }
                }
                }
                if(item.on_court == false){
                    for (j = 1; j < rows; j++) {
                    if (tab.rows[j].id == item.id) {
                        tab.rows[j].classList.add('not-visible')
                        tab.rows[j].cells[last_cell].innerHTML = 'False'
                    }
                }
                }
            })
        },
        error: function (error){
            console.log(error)
        }
    })
})
pickFiveAway.addEventListener('change', e=>{
    ids =e.target.value
    arr_ids = ids.split(',')
    if (arr_ids.length != 5){
        btnFiveAway.classList.add('not-visible')
        textAwayFive.textContent = ids
    }
    else{
        btnFiveAway.classList.remove('not-visible')
        textAwayFive.textContent = ids
    }
})
btnFiveAway.addEventListener('click', e=>{
    $.ajax({
        type: 'GET',
        url: `/start-five/${textAwayFive.textContent}/`,
        success: function (response){
            console.log(response)
            out = response.data
            btnFiveAway.classList.add('not-visible')
            out.map(item=>{
                if(item.on_court == true){
                    for (i = 1; i < rowsAway; i++) {
                    if (tabAway.rows[i].id == item.id) {
                        tabAway.rows[i].classList.remove('not-visible')
                        tabAway.rows[i].cells[last_cell].innerHTML = 'True'
                    }
                }
                }
                if(item.on_court == false){
                    for (i = 1; i < rowsAway; i++) {
                    if (tabAway.rows[i].id == item.id) {
                        tabAway.rows[i].classList.add('not-visible')
                        tabAway.rows[i].cells[last_cell].innerHTML = 'False'
                    }
                }
                }
            })
        },
        error: function (error){
            console.log(error)
        }
    })
})