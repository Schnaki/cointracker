const getCoinPrices = (coinNames, callback) => {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      callback(JSON.parse(xhttp.responseText));
    }
  };
  const arrStr = encodeURIComponent(JSON.stringify(coinNames));

  xhttp.open("GET", "/coins?coins="+arrStr, true);
  xhttp.send();
}

const addCoin = () => {
  const name = document.getElementById("selectCoin").value; 
  const amount = document.getElementById("inputAmount").value;

  let coin = {name: name, amount: amount}
  
  let coins = window.localStorage.getItem("coins");
  let new_coins = [];
  let parsed_coins = JSON.parse(coins);
  if (parsed_coins != null) {
    new_coins = new_coins.concat(parsed_coins);
  }
  new_coins.push(coin);
  window.localStorage.setItem("coins", JSON.stringify(new_coins));
}

const getCoins = (callback) => {
  let coins = JSON.parse(window.localStorage.getItem("coins"));
  let coinNames = [];
  coins.forEach(coin => {
    coinNames.push(coin.name);
  })
  getCoinPrices(coinNames, (prices => {
    console.log(prices);
    for(let i=0; i < coins.length; i++) {
      coins[i].price = prices[i];
      coins[i].total = prices[i] * coins[i].amount;
    }
    callback(coins);
  }));
}

const fillTable = () => {
  getCoins(coins => {
    coins.forEach(coin => {
      let tr = document.createElement("tr");
      let name = document.createElement("td");
      let node = document.createTextNode(coin.name);
      name.appendChild(node);
      let amount = document.createElement("td");
      node = document.createTextNode(coin.amount);
      amount.appendChild(node);
      let price = document.createElement("td");
      node = document.createTextNode(coin.price);
      price.appendChild(node);
      let total = document.createElement("td");
      node = document.createTextNode(coin.total);
      total.appendChild(node);
      tr.append(name);
      tr.append(amount);
      tr.append(price);
      tr.append(total);
      document.getElementById("tableCoin")
        .getElementsByTagName("tbody")[0]
        .append(tr);
    })
  }); 
}

fillTable();
