
const getCoinPrice = (coin, callback) => {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      callback(xhttp.responseText);
    }
  };
  xhttp.open("GET", "/coin?coin="+coin, true);
  xhttp.send();
}

const getCoinPrices = (coinIds, callback) => {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      callback(JSON.parse(xhttp.responseText));
    }
  };
  const arrStr = encodeURIComponent(JSON.stringify(coinIds));

  xhttp.open("GET", "/coins?coins="+arrStr, true);
  xhttp.send();
}

const coinExist = (id) => {
  let coins = JSON.parse(window.localStorage.getItem("coins"));
  if(coins == null) { return false };
  let temp = false;
  coins.forEach(coin => { if(coin.id == id) { temp = true }});
  return temp
}

const addCoin = () => {
  const id = document.getElementById("selectCoin").value; 
  const amount = document.getElementById("inputAmount").value;

  if (coinExist(id)) { return };

  let coin = {id: id, amount: amount}
  
  let coins = window.localStorage.getItem("coins");
  let new_coins = [];
  let parsed_coins = JSON.parse(coins);
  if (parsed_coins != null) {
    new_coins = new_coins.concat(parsed_coins);
  }
  new_coins.push(coin);
  window.localStorage.setItem("coins", JSON.stringify(new_coins));
  getCoinPrice(coin.id, price => {
    coin.price = parseFloat(price).toFixed(2);
    coin.total = parseFloat((price * coin.amount))
      .toFixed(2);
    addCoinToTable(coin);
    updateTotal();
  });
}

const deleteCoin = (e) => {
  let tbody = e.target.parentNode.parentNode.parentNode;
  let tr = e.target.parentNode.parentNode;
  let id = tr.firstChild.innerHTML;
  let total = tr.querySelector(":nth-child(4)").innerHTML;
  let coins = JSON.parse(window.localStorage.getItem("coins"));
  coins.forEach(c => {
    if (c.id == id) {
      coins.splice(coins.indexOf(c), 1)
    }
  });
  window.localStorage.setItem("coins", JSON.stringify(coins));
  tbody.removeChild(tr);
  updateTotal();
}

const getCoins = (callback) => {
  let coins = JSON.parse(window.localStorage.getItem("coins"));
  let coinIds = [];
  coins.forEach(coin => {
    coinIds.push(coin.id);
  })
  getCoinPrices(coinIds, (prices => {
    console.log(prices);
    for(let i=0; i < coins.length; i++) {
      coins[i].price = parseFloat(prices[i]).toFixed(2);
      coins[i].total = parseFloat((prices[i] * coins[i].amount))
        .toFixed(2);
    }
    callback(coins);
  }));
}

const getCoinIds = (callback) => {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      callback(JSON.parse(xhttp.responseText));
    }
  };
  xhttp.open("GET", "/coin-ids", true);
  xhttp.send();

}


const fillSelect = () => {
  getCoinIds(ids => {
    let select = document.getElementById("selectCoin");
    ids.forEach(id => {
      let option = document.createElement("option");
      let node = document.createTextNode(id);
      option.appendChild(node);
      select.appendChild(option);
    })
  })
}

const addCoinToTable = (coin) => {
  let tr = document.createElement("tr");
  let id = document.createElement("td");
  let node = document.createTextNode(coin.id);
  id.appendChild(node);
  let amount = document.createElement("td");
  node = document.createTextNode(coin.amount);
  amount.appendChild(node);
  let price = document.createElement("td");
  node = document.createTextNode(coin.price + "€");
  price.appendChild(node);
  let total = document.createElement("td");
  node = document.createTextNode(coin.total + "€");
  total.appendChild(node);

  let tdBtn = document.createElement("td");
  let button = document.createElement("button");
  button.classList.add("btnDelete");
  button.onclick = (e) => {deleteCoin(e)};
  tdBtn.appendChild(button);

  tr.append(id);
  tr.append(amount);
  tr.append(price);
  tr.append(total);
  tr.append(tdBtn);
  document.getElementById("tableCoin")
    .getElementsByTagName("tbody")[0]
    .append(tr);
}

const fillTable = () => {
  getCoins(coins => {
    coins.forEach(coin => {
      addCoinToTable(coin)
    });
  }); 
}

//avoid using extra server calls
const updateTotal = () => {
  let span = document.getElementById("total");
  if(!span.innerHTML) {
    span.innerHTML = 0;
  }
  getCoins(coins => { 
    let total = 0;
    coins.forEach(coin => total += parseFloat(coin.total));
    span.innerHTML = total.toFixed(2) + "€";
  });
}

fillSelect();
fillTable();
updateTotal();
