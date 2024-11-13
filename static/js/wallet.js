let walletconnect = document.getElementById("wallet_hesh")
let initialization = !1,
    account,
    ether

let wallet_hesh = document.querySelector('.wallet_hesh'),
    wallet_balance = document.querySelector('.wallet_balance')



let show = async () =>{
    if (window.ethereum !== "undefined" ){
        ether = window.ethereum
        let accounts = await ether.request({method:'eth_requestAccounts'}).catch(error => {

        })
        account = accounts[0]
        initialization = !0
    }else{
        console.log('plz download metamask')
        wallet_balance.innerHTML = "connect wallet"
        wallet_hesh.innerHTML = ""
    }
    let balance = await ether.request({
        "method":'eth_getBalance',
        'params':[
            account
        ]
    })
    balance = (parseInt(balance)/ 10 ** 18).toFixed(3)
    // console.log()
    wallet_hesh.innerHTML = account.substr(0,5) + '...' + account.substr(39,4)
    wallet_balance.innerHTML = balance + ' BNB'
}
// show();
// console.log("fgfdgdfgdfg")
    
walletconnect.addEventListener('click', async () =>{
    await show().catch(error => {
        wallet_balance.innerHTML = "connect wallet"
        wallet_hesh.innerHTML = ""
    })
    wallet_hesh.innerHTML = account.substr(0,5) + '...' + account.substr(39,4)
    
    let balance = await ether.request({
        "method":'eth_getBalance',
        'params':[
            account
        ]
    })
    balance = (parseInt(balance)/ 10 ** 18).toFixed(3)
    // console.log()
    wallet_balance.innerHTML = balance + ' BNB'
    })
// })




