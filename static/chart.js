const gameId = document.getElementById('game_num')

$.ajax({
  type: 'GET',
  url: `/game-chart/${gameId.textContent}`,
  success: function (response){
    console.log(response.data)
    const items = response.data
      zingchart.render({
    id: 'myChart',
    data: {
      type: 'area',
      plot: {
        aspect: 'stepped',
        stacked: false
      },
      series: [
        { values: items }
      ]
    }
  });
  },
  error: function (error){
    console.log(error)
  }
})



  zingchart.render({
    id: 'myChart',
    data: {
      type: 'area',
      plot: {
        aspect: 'stepped',
        stacked: false
      },
      series: [
        { values: [[0,54],[3,23],[9,34],[17,-23],[44,43]] }
      ]
    }
  });