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

