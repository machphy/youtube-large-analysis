#UPDATE SOON...

This Flask application allows users to input a YouTube channel URL and retrieve detailed information about the channel, including the title, profile picture, description, total videos, average views, and more. It also displays trending videos on YouTube.

## Features

- Extracts channel information from various YouTube URL formats (channel ID, username, custom URL).
- Displays channel statistics such as total videos, average views, total long and short videos.
- Shows trending videos from YouTube.
- User-friendly interface built with HTML and Bootstrap.

## Technologies Used

- **Python**: Backend development using Flask.
- **Flask**: Web framework for building the application.
- **Google YouTube Data API v3**: To fetch channel and video details.
- **HTML/CSS**: For the frontend interface, styled with Bootstrap for responsiveness.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Google API Client Library for Python
- A valid YouTube Data API key.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/machphy/youtube-channel-details-viewer.git
   cd youtube-channel-details-viewer
   ```

2. Install the required packages:

   ```bash
   pip install Flask google-api-python-client
   ```

3. Set your YouTube Data API key in the `app.py` file:

   ```python
   API_KEY = 'YOUR_YOUTUBE_API_KEY'
   ```

4. Run the Flask application:

   ```bash
   python app.py
   ```

5. Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1. Enter a valid YouTube channel URL in the input field.
2. Click the "Submit" button to view the channel details.
3. The application will display:
   - Channel title
   - Profile picture
   - Description
   - Total videos
   - Average views
   - Number of long and short videos
   - Trending videos from YouTube

## Examples

### Valid Channel URLs

- Channel ID: `https://www.youtube.com/channel/CHANNEL_ID`
- Username: `https://www.youtube.com/user/USERNAME`
- Custom URL: `https://www.youtube.com/@USERNAME`

### Error Handling

The application will show error messages for invalid URLs or if the channel is not found.

## Screenshots

![Channel Details](path/to/your/screenshot1.png)
![Trending Videos](path/to/your/screenshot2.png)

## Contributing

Feel free to fork this repository and submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3)
- [Flask Documentation](https://flask.palletsprojects.com/)
```

### Instructions:
1. **Screenshots**: Replace `path/to/your/screenshot1.png` and `path/to/your/screenshot2.png` with the actual paths to your screenshots.
2. **API Key**: Remind users to create their own API key and replace `YOUR_YOUTUBE_API_KEY` in the code.
3. **Testing and Validation**: Ensure that everything works as described, especially the examples and installation steps.

You can copy and paste this into your README file. If you need more details or any specific section expanded, just let me know!
