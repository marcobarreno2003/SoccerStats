# Soccer Stats

**Soccer Stats** is a football statistics analysis application that uses machine learning to predict match outcomes in real time and provides detailed insights into team and player performance. This project combines historical and live data, data processing, and deep learning techniques to offer a unique experience for tracking and analyzing soccer matches.

## Features

- **Match Outcome Prediction**: Uses a machine learning model to predict match outcomes (win, loss, or draw), achieving a validated accuracy of 81.82%.
- **Real-Time Data**: Fetches live match data via the API-Sports to display current statistics during matches.
- **Performance Analysis**: Provides detailed team and player statistics, including passes, key plays, and real-time performance metrics.
- **User Interface**: An interactive web interface built with Flask allows users to view predictions and statistics intuitively.

## Technologies and Tools

- **Python**: Core programming language.
- **TensorFlow / Keras**: For training and running the prediction model.
- **Flask**: Framework for the web interface.
- **Scikit-Learn, Pandas, and API-Sports**: For data processing and real-time data access.
- **Visualization**: Interactive graphs and dashboards using Matplotlib or Plotly.

## Project Structure

```
SoccerStats/
├── backend/                     # Backend folder containing API and Flask server
│   ├── api/                     # API endpoints for data processing
│   ├── templates/               # HTML templates for the web interface
│   ├── .env                     # Environment variables for sensitive configurations
│   └── app.py                   # Main Flask application
├── frontend/                    # Frontend folder with assets and HTML pages
│   ├── assets/                  # Static assets for the frontend
│   │   ├── css/                 # CSS files for styling
│   │   │   └── style.css        # Main stylesheet
│   │   └── images/              # League and team logos
│   │       ├── argentina_first_division.png
│   │       ├── brasileirao_logo.png
│   │       ├── [other league logos...]
│   ├── js/                      # JavaScript files
│   │   └── app.js               # Main JavaScript file
│   ├── about.html               # About page
│   ├── blog.html                # Blog page
│   ├── index.html               # Main landing page
│   ├── live_matches.html        # Page for live match tracking
│   └── predict.html             # Prediction page
├── .gitignore                   # Git ignore file to exclude certain files/folders
├── README.md                    # Project description and usage guide
└── requirements.txt             # List of dependencies

```

## How to Use

1. **Clone the Repository**: Clone the project to your local machine.
   ```bash
   git clone https://github.com/yourusername/SoccerStats.git
   ```

2. **Install Dependencies**: Ensure you have Python installed, then use `pip` to install the required packages.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the API**: Obtain an API key from [API-Sports](https://rapidapi.com/api-sports/api/api-football) for real-time data access and add the key to a configuration file.

4. **Train or Load the Model**: You can train the model using `src/model_training.py` or load the pre-trained model.

5. **Run the Web Application**: Start the Flask server to access the interface.
   ```bash
   python app.py
   ```

6. **Access the Interface**: Open `http://localhost:5000` in your browser to view real-time statistics and predictions.

## Future Enhancements

- **Database Expansion**: Integrate more leagues and tournaments.
- **Improved Model Accuracy**: Experiment with other deep learning models or optimization methods.
- **Personalized User Features**: Allow users to follow specific teams or receive match notifications.
- **Player Analysis**: Add detailed player performance analysis based on live data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
