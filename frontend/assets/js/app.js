document.addEventListener('DOMContentLoaded', () => {
    // Función para obtener los partidos en vivo desde el backend de Flask
    const fetchLiveMatches = async () => {
        try {
            const response = await fetch('/live-matches');
            if (!response.ok) {
                throw new Error('Error loading live matches.');
            }

            const data = await response.json();
            console.log(data); // Para depurar los datos recibidos

            // Llamamos a la función para actualizar el DOM con los datos recibidos
            displayLiveMatches(data.response);
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('matches-container').innerHTML = '<p>Error loading live matches.</p>';
        }
    };

    // Función para mostrar los partidos en vivo en el contenedor
    const displayLiveMatches = (matches) => {
        const container = document.getElementById('matches-container');
        container.innerHTML = ''; // Limpiamos el contenido previo

        if (matches.length === 0) {
            container.innerHTML = '<p>No live matches at the moment.</p>';
            return;
        }

        matches.forEach(match => {
            const matchDiv = document.createElement('div');
            matchDiv.classList.add('match');

            const homeTeam = match.teams.home.name;
            const awayTeam = match.teams.away.name;
            const homeScore = match.goals.home !== null ? match.goals.home : '-';
            const awayScore = match.goals.away !== null ? match.goals.away : '-';

            matchDiv.innerHTML = `
                <h3>${homeTeam} vs ${awayTeam}</h3>
                <p>Score: ${homeScore} - ${awayScore}</p>
                <p>Status: ${match.status.long}</p>
            `;

            container.appendChild(matchDiv);
        });
    };

    // Llamada inicial para cargar los partidos en vivo
    fetchLiveMatches();
});

