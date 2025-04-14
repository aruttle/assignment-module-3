  // ==========================
    //  API Functionality
    // ==========================   

    async function getWeather() {
        const lat = 53.3498; 
        const lon = -6.2603;
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            document.getElementById("weather-info").innerHTML = `
                <p>Temp: ${data.current_weather.temperature}°C</p>
                <p>Wind: ${data.current_weather.windspeed} km/h</p>
            `;
        } catch (error) {
            console.error("Error fetching weather:", error);
            document.getElementById("weather-info").innerHTML = "Could not load weather.";
        }
    }

    getWeather();