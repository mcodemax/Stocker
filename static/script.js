const CHART = $('#stock-chart');
const CHART2 = $('#stock-chart2');
const OPTIMAL_CHART_LEN = 20;
//const TICKER = ticker

// show 3 charts at a time.
Chart.defaults.font.size = 10;

async function chartFunc(ticker, jQueChart){
    response = await parseAPIcall(ticker);
    console.log(response)
    datesArr = response.data.date_keys;
    priceArr = response.data.price_vals;
    console.log({datesArr, priceArr})

    if(datesArr.length > OPTIMAL_CHART_LEN){
        datesArr = datesArr.slice(datesArr.length - OPTIMAL_CHART_LEN)
        priceArr = priceArr.slice(priceArr.length - OPTIMAL_CHART_LEN)
    }


    let myChart = new Chart(jQueChart, {
        type: 'line',
        data: {
            labels: datesArr,
            datasets: [{
              label: `${ticker}`,
              data: priceArr,
              fill: false,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1
            }]
        },
        options: {
            scales: {
                xAxis: {
                    gridLines: {
                      display: false
                    },
                    ticks: {
                        autoSkip: false,
                        maxRotation: 90,
                        minRotation: 90,
                        font: {
                           // family: 'Raleway', // Your font family
                            fontSize: 60
                        }
                    }
    
                }
            }
        }
    });
    

}


let myChart2 = new Chart(CHART2, {
    type: 'line',
    data: {
        labels: ['may', 'zsegszegeszg', 'zegseszgszgt', 'g', 'g'],
        datasets: [{
          label: 'My First Dataset',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
    },
    options: {
        // plugins: {
        //     legend: {
        //         labels: {
        //             // This more specific font property overrides the global property
        //             font: {
        //                 size: 56
        //             }
        //         }
        //     }
        // },
        scales: {
            xAxis: {
                gridLines: {
                  display: false
                },
                ticks: {
                    autoSkip: false,
                    maxRotation: 45,
                    minRotation: 45,
                    font: {
                       // family: 'Raleway', // Your font family
                        fontSize: 60
                    }
                }

              }
        }
    }
});




async function parseAPIcall(ticker){
    const URL = 'testapi'
    let res = await axios.post(URL, { ticker })
    console.log({res})
    console.log(res.data.date_keys)
    console.log(res.data.price_vals)

    return res;
}

//make an evt handler that detects canvas's with diff ticker ids






// let myChart = new Chart(CHART, {
//     type: 'line',
//     data: {
//         labels: ['may', 'zsegszegeszg', 'zegseszgszgt', 'g', 'g', 'zsegzsegop', 'g'],
//         datasets: [{
//           label: 'My First Dataset',
//           data: [65, 59, 80, 81, 56, 55, 40],
//           fill: false,
//           borderColor: 'rgb(75, 192, 192)',
//           tension: 0.1
//         }]
//     },
//     options: {
//         // plugins: {
//         //     legend: {
//         //         labels: {
//         //             // This more specific font property overrides the global property
//         //             font: {
//         //                 size: 56
//         //             }
//         //         }
//         //     }
//         // },
//         scales: {
//             xAxis: {
//                 gridLines: {
//                   display: false
//                 },
//                 ticks: {
//                     autoSkip: false,
//                     maxRotation: 45,
//                     minRotation: 45,
//                     font: {
//                        // family: 'Raleway', // Your font family
//                         fontSize: 60
//                     }
//                 }

//               }
//         }
//     }
// });
