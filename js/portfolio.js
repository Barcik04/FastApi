axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.withCredentials = false;

const showPnlBtn = document.getElementById('showPnlBtn');
const resultDiv = document.getElementById('portfolioResult');

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

    try {
        const graphResponse = await axios.get('/transactions/p_n_l', {
            headers: {
                Authorization: `Bearer ${jwt}`
            },
            responseType: 'arraybuffer'
        });

        if (graphResponse.status === 200) {
            const blob = new Blob([graphResponse.data], { type: 'image/png' });
            const url = URL.createObjectURL(blob);

            const img = document.getElementById('p_n_l_graph');
            img.src = url;
        }
    } catch (error) {
        resultDiv.textContent = "Error loading p_n_l_graph.";
        console.log(error);
    }

})