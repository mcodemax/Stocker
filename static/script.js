const closing_prices = {};

// this timer is used to wait for api to call and store stuff into the array
setTimeout(() => {
  console.log('this is the first message');
  //could add to only exec this f() after a certain page loads by seeing if a certain ele exists.
  calcPortfolioVal();
}, 3000);

//https://stackoverflow.com/questions/149055/how-to-format-numbers-as-currency-strings
const formatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',

  // These options are needed to round to whole numbers if that's what you want.
  //minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
  //maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
});

/**calculates portfolio value and adds to DOM */
async function calcPortfolioVal() {
  let total = 0;
  const $CHARTS_LIST_AMT = $('.tickerlisting');

  $CHARTS_LIST_AMT.each(function () {
    const id = $(this).attr('id');
    const price = closing_prices[$(this).id];
    const holdings = Number($(this).data('amount'));
    total += closing_prices[id] * Number(holdings);
  });
  //truncate total to 2 decimal places when added to UI
  console.log(total);
  total = formatter.format(total);
  document.getElementById(
    'port-num-val'
  ).innerHTML = `Portfolio Value: ${total}`;
}

async function parseAPIcall(ticker) {
  const URL = '/testapi'; //https://stackoverflow.com/questions/54656818/axios-posting-to-wrong-url
  let res = await axios.post(URL, { ticker });
  console.log({ res });
  console.log(res.data.date_keys);
  console.log(res.data.price_vals);

  return res;
}

$(function () {
  const OPTIMAL_CHART_LEN = 15;
  const $CHARTS_LIST = $('.chart');

  //  https://api.jquery.com/each/ use to iterate over each stock
  //  chart and generate graph by calling chartFunc
  $CHARTS_LIST.each(async function () {
    //Iterate over an array of selected jQuery Objects
    const ticker = $(this).attr('id').replace('-ticker', ''); //works
    console.log(ticker);
    await chartFunc(ticker, $(this));
    //https://docs.sqlalchemy.org/en/14/errors.html#error-3o7r
  });

  Chart.defaults.font.size = 15;
  Chart.defaults.font.color = '#598ec0';
  /**
   * Input: ticker and jQueryChart object
   * Causes a chart to be generated for a ticker on the DOM
   */
  async function chartFunc(ticker, jQueChart) {
    response = await parseAPIcall(ticker);
    console.log(response);
    datesArr = response.data.date_keys;
    priceArr = response.data.price_vals;
    console.log({ datesArr, priceArr });

    closing_prices[ticker] = priceArr[priceArr.length - 1];

    if (datesArr.length > OPTIMAL_CHART_LEN) {
      datesArr = datesArr.slice(datesArr.length - OPTIMAL_CHART_LEN);
      priceArr = priceArr.slice(priceArr.length - OPTIMAL_CHART_LEN);
    }

    let myChart = new Chart(jQueChart, {
      type: 'line',
      data: {
        labels: datesArr,
        datasets: [
          {
            label: `${ticker}`,
            data: priceArr,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
          },
        ],
      },
      options: {
        scales: {
          xAxis: {
            gridLines: {
              display: false,
            },
            ticks: {
              autoSkip: false,
              maxRotation: 90,
              minRotation: 90,
              font: {
                fontSize: 60,
              },
            },
          },
        },
      },
    });
  }
});
