# YouTube Channel Details Viewer

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
