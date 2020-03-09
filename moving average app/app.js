yurl = 'https://query1.finance.yahoo.com/v8/finance/chart/ACC.NS?region=IN&lang=en-IN&includePrePost=false&interval=15m&range=5d'
// yurl = 'https://query1.finance.yahoo.com/v8/finance/chart/ACC.NS?region=IN&lang=en-IN&includePrePost=false&interval=15m&range=5d&corsDomain=in.finance.yahoo.com&.tsrc=finance'

temp = []
// fetch(yurl, {
//         headers: {
//             "Content-Type": "application/x-www-form-urlencoded"
//         },
//         mode: 'no-cors'
//     }).then(response => {
//         temp = response
//         return response
//     })
//     .then((data) => {
//         console.log(data)
//     })
// d = []
// let response = fetch("https://query1.finance.yahoo.com/v8/finance/chart/ACC.NS?region=IN&lang=en-IN&includePrePost=false&interval=15m&range=5d", {
//         // "headers": {
//         //     "accept": "*/*",
//         //     "accept-language": "en-US,en;q=0.9",
//         //     "sec-fetch-dest": "empty",
//         //     "sec-fetch-mode": "cors",
//         //     "sec-fetch-site": "same-site"
//         // },
//         // "referrer": "https://in.finance.yahoo.com/quote/ACC.NS/",
//         // "referrerPolicy": "no-referrer-when-downgrade",
//         // "body": null,
//         "headers": {
//             'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0s',
//             // 'Accept': 'application/json'
//             'Content-Type': 'application/json',
//         },
//         "method": "GET",
//         "mode": "no-cors"
//     })

// $.getJSON({
//     url: yurl,
//     // dataType: 'json', // Notice! JSONP <-- P (lowercase)
//     crossOrigin: true,
//     success: function (res) {
//         // do stuff with json (in this case an array)
//         // alert("Success");
//         console.log(res)
//     },
//     error: function () {
//         console.log("Error")
//     }
// })
// x = []

// fetch('https://crossorigin.me/' + yurl, {
//     mode: 'no-cors'
// }).then(res => console.log(res))
console.log('js ready!')