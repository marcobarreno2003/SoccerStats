document.addEventListener("DOMContentLoaded", function () {
    // Fetch live matches directly from the /live-matches endpoint
    fetch('/live-matches')
        .then(response => response.json())
        .then(data => {
            const liveMatchesDiv = document.getElementById('live-matches');
            liveMatchesDiv.innerHTML = ''; // Clear the "Loading" message

            if (data.response && data.response.length > 0) {
                data.response.forEach(match => {
                    const matchInfo = `
                        <div class="match-card">
                            <h3>${match.teams.home.name} vs ${match.teams.away.name}</h3>
                            <p><strong>League:</strong> ${match.league.name}</p>
                            <p><strong>Time:</strong> ${new Date(match.fixture.date).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}</p>
                        </div>
                    `;
                    liveMatchesDiv.innerHTML += matchInfo;
                });
            } else {
                liveMatchesDiv.innerHTML = '<p>No live matches at the moment.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching live matches:', error);
            document.getElementById('live-matches').innerHTML = '<p>Failed to load live matches.</p>';
        });
});
