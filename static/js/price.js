ourprice = document.getElementById("price")
  // Функция для получения цены токена с CoinGecko API без использования фреймворков
// function getTokenPrice(tokenId) {
//     return fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${tokenId}&vs_currencies=usd`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('erroe');
//             }
//             return response.json();
//         })
//         .then(data => {
//             const price = data[tokenId].usd;
//             return price;
//         })
//         .catch(error => {
//             console.error('error:', error);
//             return null;
//         });
// }

// // Пример использования функции для получения цены токена Ethereum (ETH) без использования фреймворков
// getTokenPrice('ce9d669e-15d8-45c5-921a-e9e14b608ec5')
//     .then(price => {
//         if (price !== null) {
//             ourprice.innerHTML = `SPJ ${price}$`
//         }
//     });



// url ="https://api.geckoterminal.com/api/v2/simple/networks/bsc/token_price/0x4d41c76622dcb7208c67d2164cca28d4a21fb323"
// r = requests.get(url)
// data = r.json()['data']['attributes']['token_prices']['0x4d41c76622dcb7208c67d2164cca28d4a21fb323']
// data
// function spjprice() {
//     return fetch(`https://api.geckoterminal.com/api/v2/simple/networks/bsc/token_price/0x4d41c76622dcb7208c67d2164cca28d4a21fb323`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('erroe');
//             }
//             let price = response.json()
//             // price = price['data']
//             console.log(price.attributes.price)
//             return response.json();
//         })
//         .then(data => {
            
//             const price = data[tokenId].usd;
//             return price;
//         })
//         .catch(error => {
//             console.error('error:', error);
//             return null;
//         });
// }
// spjprice()
fetch('https://api.geckoterminal.com/api/v2/simple/networks/bsc/token_price/0x4d41c76622dcb7208c67d2164cca28d4a21fb323')
    .then(response => response.json())
    .then(data => {
    let price = data['data']['attributes']['token_prices']['0x4d41c76622dcb7208c67d2164cca28d4a21fb323']
    // console.log(data['data']['attributes']['token_prices']['0x4d41c76622dcb7208c67d2164cca28d4a21fb323']);
    ourprice.innerHTML = `SPJ ${price.substr(0,3) + '...' + price.substr(10,4)}$`
    // ourprice.innerHTML = price.substr(0,3) + '...' + price.substr(10,4)
    })
    .catch(error => {
    console.error('request error:', error);
});