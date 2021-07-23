const tabPkt = document.getElementById('PKT')
const tabReb = document.getElementById('REB')
const tabAst = document.getElementById('AST')
const tabBlk = document.getElementById('BLK')
const tabStl = document.getElementById('STL')
const selectStat = document.getElementById('select-stat')
selectStat.addEventListener('change', e=>{
    const stat = e.target.value
    if (stat == "PKT"){
        tabPkt.classList.remove('not-visible')
        tabAst.classList.add('not-visible')
        tabBlk.classList.add('not-visible')
        tabStl.classList.add('not-visible')
        tabReb.classList.add('not-visible')
    }
    if (stat == 'AST'){
        tabPkt.classList.add('not-visible')
        tabAst.classList.remove('not-visible')
        tabBlk.classList.add('not-visible')
        tabStl.classList.add('not-visible')
        tabReb.classList.add('not-visible')
    }
    if (stat == 'BLK'){
        tabPkt.classList.add('not-visible')
        tabAst.classList.add('not-visible')
        tabBlk.classList.remove('not-visible')
        tabStl.classList.add('not-visible')
        tabReb.classList.add('not-visible')
    }
    if (stat == 'STL'){
        tabPkt.classList.add('not-visible')
        tabAst.classList.ad('not-visible')
        tabBlk.classList.add('not-visible')
        tabStl.classList.remove('not-visible')
        tabReb.classList.add('not-visible')
    }
    if (stat == 'REB'){
        tabPkt.classList.add('not-visible')
        tabAst.classList.add('not-visible')
        tabBlk.classList.add('not-visible')
        tabStl.classList.add('not-visible')
        tabReb.classList.remove('not-visible')
    }
    if (stat == 'ALL'){
        tabPkt.classList.remove('not-visible')
        tabAst.classList.remove('not-visible')
        tabBlk.classList.remove('not-visible')
        tabStl.classList.remove('not-visible')
        tabReb.classList.remove('not-visible')
    }
})