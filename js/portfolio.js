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
            resultDiv.textContent = JSON.stringify(response.data, null, 2);
            resultDiv.style.whiteSpace = "pre-wrap"
        }
    } catch (error) {
        resultDiv.textContent = "Error loading portfolio.";
        console.log(error);
    }
})