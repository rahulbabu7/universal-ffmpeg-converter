# Universal FFmpeg Converter

A simple, modern Qt GUI application for converting media files using FFmpeg. Built with Python and PyQt6.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## Features

- 🎬 **Multiple Format Support**: MP4, MOV (ProRes), WebM, GIF, MP3
- 📁 **Flexible Output**: Choose custom output directory and filename
- 🔊 **Audio Control**: Keep or remove audio tracks
- 🎨 **Modern UI**: Clean, intuitive interface with real-time conversion log
- ⚡ **Fast Conversion**: Leverages FFmpeg's powerful encoding capabilities
- 📊 **Progress Tracking**: Visual feedback during conversion process

## Supported Formats

### Output Formats
- **MP4 (H.264)** - Universal compatibility, optimized for web and mobile
- **MOV (ProRes 422)** - High-quality intermediate codec for video editing
- **WebM (VP9)** - Web-optimized format with excellent compression
- **GIF (Animated)** - 15fps animated GIFs at 640px width
- **MP3 (Audio only)** - Extract audio at 192kbps

### Input Formats
Supports all common video formats: MP4, MKV, MOV, AVI, WebM, FLV, M4V, MPEG, MPG, and more.

## Screenshots

*Add screenshots here*

## Prerequisites

### System Requirements
- **Python 3.8 or higher**
- **FFmpeg** (must be installed and available in PATH)

### Installing FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Fedora:**
```bash
sudo dnf install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**From source or other methods:**
Visit [FFmpeg official website](https://ffmpeg.org/download.html)

## Installation

### Method 1: Run from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rahulbabu7/universal-ffmpeg-converter.git
   cd universal-ffmpeg-converter
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python3 ffmpeg_converter.py
   ```

### Method 2: Build Standalone Executable

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   pyinstaller --onefile --windowed --name="FFmpeg-Converter" ffmpeg_converter.py
   ```

3. **Run the app:**
   ```bash
   ./dist/FFmpeg-Converter
   ```

### Method 3: Install as System Application

1. **Build the executable** (see Method 2)

2. **Create desktop entry:**
   ```bash
   mkdir -p ~/.local/share/applications
   ```

3. **Create file** `~/.local/share/applications/ffmpeg-converter.desktop`:
   ```ini
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=FFmpeg Converter
   Exec=/full/path/to/dist/FFmpeg-Converter
   Icon=applications-multimedia
   Terminal=false
   Categories=AudioVideo;Video;
   ```

4. **Update desktop database:**
   ```bash
   update-desktop-database ~/.local/share/applications/
   ```

5. **Launch from your application menu!**

## Usage

1. **Select Input File**: Click "Browse Files" to choose your video/audio file
2. **Choose Output Directory**: Click "Choose Folder" to set where the converted file will be saved
3. **Set Output Filename**: Enter a name for your output file (extension added automatically)
4. **Select Format**: Choose your desired output format from the dropdown
5. **Audio Options**: Choose to keep or remove audio (not applicable for audio-only formats)
6. **Convert**: Click the "Convert" button and watch the progress in the log window

## Format Details

| Format | Video Codec | Audio Codec | Use Case |
|--------|-------------|-------------|----------|
| MP4 | H.264 (CRF 22) | AAC/Copy | General purpose, web, mobile |
| MOV | ProRes 422 | Copy | Video editing, post-production |
| WebM | VP9 (CRF 31) | Opus/Copy | Web streaming, modern browsers |
| GIF | GIF | None | Animations, social media |
| MP3 | None | MP3 192k | Audio extraction |

## Configuration

The application uses sensible defaults, but you can modify the encoding parameters by editing the `get_format_settings()` method in `ffmpeg_converter.py`.

### Example Custom Settings:
```python
formats = {
    0: ("mp4", "-c:v libx264 -crf 18 -preset slow"),  # Higher quality, slower
    # Add your custom presets here
}
```

## Troubleshooting

### "ffmpeg not found" error
Make sure FFmpeg is installed and in your system PATH:
```bash
ffmpeg -version
```

### Application won't start
Check that PyQt6 is installed:
```bash
python3 -c "import PyQt6; print('PyQt6 OK')"
```

### Conversion fails
Check the conversion log for detailed FFmpeg error messages. Common issues:
- Unsupported codec in input file
- Insufficient disk space
- Write permissions in output directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Powered by [FFmpeg](https://ffmpeg.org/)
- Icons from system theme

## Author

Name - [@rahulbabu](https://github.com/rahulbabu7)

Project Link: [https://github.com/yourusername/universal-ffmpeg-converter](https://github.com/rahulbabu7/universal-ffmpeg-converter)

## Support

If you find this project helpful, please consider giving it a ⭐ on GitHub!

For issues, bugs, or feature requests, please [open an issue](https://github.com/rahulbabu7/universal-ffmpeg-converter/issues).