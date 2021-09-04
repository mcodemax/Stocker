const OPTIMAL_CHART_LEN = 20;
const $CHARTS_LIST = $('.chart');

//  https://api.jquery.com/each/ use to iterate over each stock
//  chart and generate graph by calling chartFunc
$CHARTS_LIST.each(async function(){ //Iterate over an array of selected jQuery Objects
        
        const ticker = $(this).attr('id').replace('-ticker', '');//works
        console.log(ticker)
        await chartFunc(ticker, $(this));
        
    }
    
);

Chart.defaults.font.size = 10;

/** 
 * Input: ticker and jQueryChart object
 * Causes a chart to be generated for a ticker on the DOM
 */
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


async function parseAPIcall(ticker){
    const URL = '/testapi' //https://stackoverflow.com/questions/54656818/axios-posting-to-wrong-url
    let res = await axios.post(URL, { ticker })
    console.log({res})
    console.log(res.data.date_keys)
    console.log(res.data.price_vals)

    return res;
}

//make an evt handler that detects canvas's with diff ticker ids

/*
$(function() {
    
});
*/