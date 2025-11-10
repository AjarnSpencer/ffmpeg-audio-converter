
<p align="center">
  <img src="https://raw.githubusercontent.com/AjarnSpencer/ffmpeg-audio-converter/main/ffmpeg-Audio-Converter.png" alt="ffmpeg Audio Converter" width="200"/>
</p>

<h1 align="center">ffmpeg Audio Converter</h1>

A simple, cross-platform desktop GUI application for converting audio files from one format to another using the power of [ffmpeg](https://ffmpeg.org/).

This application was developed by the Gemini CLI Unleashed AI in collaboration with Ajarn Spencer Littlewood.

## Features

- **Cross-Platform:** Works on Windows, macOS, and Linux.
- **Batch Conversion:** Select and convert multiple files at once.
- **Multiple Formats:** Convert to and from a variety of formats, including MP3, WAV, AAC, OGG, FLAC, and M4A.
- **Quality Selection:** Choose your desired audio quality/bitrate for lossy formats.
- **Simple GUI:** An easy-to-use graphical interface that doesn't require command-line knowledge.
- **Standalone:** Packaged as a single executable file for easy use.

## Installation & Usage

You can download the latest version for your operating system from the **[Actions tab](https://github.com/AjarnSpencer/ffmpeg-audio-converter/actions)** on this repository.
1. Click on the latest completed workflow under "Build Application".
2. Scroll down to the "Artifacts" section to find and download the application for your OS.

---

### Windows

1.  Download the `ffmpeg-audio-converter-Windows` artifact.
2.  You will get a single executable file: `main.exe`.
3.  This is a portable application. You can place it anywhere and run it directly. No installation is needed.

---

### macOS

1.  Download the `ffmpeg-audio-converter-macOS` artifact.
2.  Unzip the `ffmpeg-audio-converter-macOS.zip` file.
3.  You will get an application bundle named `main.app`.
4.  Move `main.app` to your "Applications" folder and run it from there.
    *Note: You may need to right-click the app and select "Open" the first time you run it if you get a security warning.*

---

### Linux

1.  Download the `ffmpeg-audio-converter-Linux` artifact.
2.  You will get a single executable file named `main_linux`.
3.  Open a terminal and make the file executable:
    ```bash
    chmod +x main_linux
    ```
4.  Run the application from the terminal:
    ```bash
    ./main_linux
    ```

## System Requirement

This application is a graphical frontend for `ffmpeg`. You **must** have `ffmpeg` installed on your system and accessible in your system's PATH for the application to work.
