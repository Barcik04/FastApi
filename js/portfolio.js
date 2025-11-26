axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.withCredentials = false;

const showPnlBtn = document.getElementById('showPnlBtn');
const resultDiv = document.getElementById('portfolioResult');
const showPnlGraphBtn = document.getElementById('showPnlGraphBtn');
const showValGraphBtn = document.getElementById('showValGraphBtn');
const showValGraphMultiCoinBtn = document.getElementById('showValGraphMultiCoinBtn');
const showPnlGraphPercentageBtn = document.getElementById('showPnlGraphPercentageBtn');


showPnlBtn.addEventListener('click', async() => {
    const jwt = localStorage.getItem('jwt');

    try {
        const response = await axios.get('/portfolios', {
            headers: {
                Authorization: `Bearer ${jwt}`
            }
        });

        if (response.status === 200) {
            const data = response.data;

            document.getElementById('portfolioId').textContent = `ID: ${data.id}`;
            document.getElementById('coins').textContent = `Coins: ${JSON.stringify(data.coins)}`;
            document.getElementById('boughtPrice').textContent = `Avg Bought Price: ${JSON.stringify(data.bought_price)}`;
            document.getElementById('pnl').textContent = `Profit and loss: ${data.p_and_l}`;
        }
    } catch (error) {
        resultDiv.textContent = "Error loading portfolio.";
        console.log(error);
    }
})


showPnlGraphBtn.addEventListener('click', async() => {
    const jwt = localStorage.getItem('jwt');


    try {
        const graphResponse = await axios.get('/transactions/p_n_l', {
            headers: {
                Authorization: `Bearer ${jwt}`
            },
            responseType: 'arraybuffer'
        });

        if (graphResponse.status === 200) {
            const arrayBufferToBase64 = (buffer) => {
                let binary = '';
                const bytes = new Uint8Array(buffer);
                bytes.forEach((b) => {
                    binary += String.fromCharCode(b);
                });
                return window.btoa(binary);
            };

            const img = document.getElementById('p_n_l_graph');
            const base64Image = arrayBufferToBase64(graphResponse.data);

            img.src = `data:image/png;base64,${base64Image}`;
            img.alt = 'Profit and loss graph';
            img.style.display = 'block';
        }

    } catch (error) {
        resultDiv.textContent = "Error loading pnl graph.";
        console.log(error);
    }
})


showValGraphBtn.addEventListener('click', async() => {
    const jwt = localStorage.getItem('jwt');
    const daysValue = document.getElementById('daysVal')
    const daysVal = daysValue.value.trim();

    try {
        const graphResponse = await axios.get('/transactions/val', {
            params: daysVal ? { days: daysVal } : {},
            headers: {
                Authorization: `Bearer ${jwt}`
            },
            responseType: 'arraybuffer'
        });

        if (graphResponse.status === 200) {
            const arrayBufferToBase64 = (buffer) => {
                let binary = '';
                const bytes = new Uint8Array(buffer);
                bytes.forEach((b) => {
                    binary += String.fromCharCode(b);
                });
                return window.btoa(binary);
            };

            const img = document.getElementById('p_n_l_graph');
            const base64Image = arrayBufferToBase64(graphResponse.data);

            img.src = `data:image/png;base64,${base64Image}`;
            img.alt = 'Profit and loss graph';
            img.style.display = 'block';
        }

    } catch (error) {
        resultDiv.textContent = "Error loading pnl graph.";
        console.log(error);
    }
})



showValGraphMultiCoinBtn.addEventListener('click', async() => {
    const jwt = localStorage.getItem('jwt');
    const daysValue = document.getElementById('daysVal')
    const daysVal = daysValue.value.trim();

    try {
        const graphResponse = await axios.get('/transactions/sep-coins', {
            params: daysVal ? { days: daysVal } : {},
            headers: {
                Authorization: `Bearer ${jwt}`
            },
            responseType: 'arraybuffer'
        });

        if (graphResponse.status === 200) {
            const arrayBufferToBase64 = (buffer) => {
                let binary = '';
                const bytes = new Uint8Array(buffer);
                bytes.forEach((b) => {
                    binary += String.fromCharCode(b);
                });
                return window.btoa(binary);
            };

            const img = document.getElementById('p_n_l_graph');
            const base64Image = arrayBufferToBase64(graphResponse.data);

            img.src = `data:image/png;base64,${base64Image}`;
            img.alt = 'Profit and loss graph';
            img.style.display = 'block';
        }

    } catch (error) {
        resultDiv.textContent = "Error loading pnl graph.";
        console.log(error);
    }
})




showPnlGraphPercentageBtn.addEventListener('click', async() => {
    const jwt = localStorage.getItem('jwt');


    try {
        const graphResponse = await axios.get('/transactions/p_n_l_perc', {
            headers: {
                Authorization: `Bearer ${jwt}`
            },
            responseType: 'arraybuffer'
        });

        if (graphResponse.status === 200) {
            const arrayBufferToBase64 = (buffer) => {
                let binary = '';
                const bytes = new Uint8Array(buffer);
                bytes.forEach((b) => {
                    binary += String.fromCharCode(b);
                });
                return window.btoa(binary);
            };

            const img = document.getElementById('p_n_l_graph');
            const base64Image = arrayBufferToBase64(graphResponse.data);

            img.src = `data:image/png;base64,${base64Image}`;
            img.alt = 'Profit and loss graph';
            img.style.display = 'block';
        }

    } catch (error) {
        resultDiv.textContent = "Error loading pnl graph.";
        console.log(error);
    }
})




const showTradesBtn = document.getElementById('showTrades');
const tradeResults = document.getElementById('tradeList');

// YOUR TRADES
async function handleTradeAction(requestId, accept) {
    const jwt = localStorage.getItem('jwt');

    try {
        const response = await axios.put(
            '/trade_requests/update',
            {
                accept: accept,
                request_id: requestId
            },
            {
                headers: {
                    Authorization: `Bearer ${jwt}`
                }
            }
        );

        if (response.status === 200) {
            await showTrades.click;
        }
    } catch (error) {
        console.error("Error updating trade:", error);
        alert("Error updating trade: " + (error.response?.data?.detail || "Unknown error"));
    }
}




showTradesBtn.addEventListener('click', async () => {
    const jwt = localStorage.getItem('jwt');

    try {
        const response = await axios.get('/trade_requests', {
            headers: {
                Authorization: `Bearer ${jwt}`
            }
        });

        if (response.status === 200) {
            const trades = response.data;

            tradeResults.innerHTML = "";

            if (trades.length === 0) {
                tradeResults.innerHTML = "<p>No trades found.</p>";
                return;
            }

            const header = document.createElement('header');
            header.className = "tradeListHeader";
            header.textContent = "TRADES LIST";
            tradeResults.appendChild(header);

            const list = document.createElement('ul');
            list.className = "tradeListUl";

            trades.forEach(t => {
                const item = document.createElement('li');
                item.className = "tradeItem";


                const infoDiv = document.createElement('div');
                infoDiv.innerHTML = `
                    <b style="display: block;">${t.coin} → ${t.coin_get}</b>
                    Qty: ${t.quantity} &nbsp; | &nbsp; Qty: ${t.quantity_get}<br>
                    Status: ${t.status}<br>
                    <small>${t.created_at}</small>
                `;

                item.appendChild(infoDiv);


                if (t.status === "PENDING") {
                    const btnContainer = document.createElement('div');
                    btnContainer.style.marginTop = "8px";
                    btnContainer.style.display = "flex";
                    btnContainer.style.gap = "8px";

                    const acceptBtn = document.createElement('button');
                    acceptBtn.textContent = "ACCEPT";
                    acceptBtn.className = "tradeAcceptBtn";

                    const declineBtn = document.createElement('button');
                    declineBtn.textContent = "DECLINE";
                    declineBtn.className = "tradeDeclineBtn";

                    acceptBtn.addEventListener('click', async () => {
                        await handleTradeAction(t.id, true);
                    });

                    declineBtn.addEventListener('click', async () => {
                        await handleTradeAction(t.id, false);
                    });

                    btnContainer.appendChild(acceptBtn);
                    btnContainer.appendChild(declineBtn);
                    item.appendChild(btnContainer);
                }

                list.appendChild(item);
            });

            tradeResults.appendChild(list);
        }
    } catch (error) {
        tradeResults.textContent = "Error loading trades.";
        console.log(error);
    }
});




const createTradeBtn = document.getElementById('createTradeBtn');

createTradeBtn.addEventListener('click', async() => {
    const jwt = localStorage.getItem('jwt');

    const coin = document.getElementById('coinTrade').value;
    const quantity = document.getElementById('quantityTrade').value;
    const coinGet = document.getElementById('coinGetTrade').value;
    const quantityGet = document.getElementById('quantityGetTrade').value;
    const receiverId = document.getElementById('receiverPortfolioId').value;

    try {
        const response = axios.post('/trade_requests/send',
            {
                coin: coin,
                quantity: parseFloat(quantity),
                coin_get: coinGet,
                quantity_get: parseFloat(quantityGet),
                receiver_id: receiverId,
            },
            {
            headers: {
                Authorization: `Bearer ${jwt}`
            },
        })

        if (response.status === 200) {
            console.log('Trade Created Successfully.');
        }
    } catch (error) {
        console.log(error);
    }
})




