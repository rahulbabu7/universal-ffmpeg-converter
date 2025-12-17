
"""
Universal FFmpeg Converter - Qt GUI
A simple, modern interface for converting media files
"""
import shutil
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QLineEdit, QFileDialog,
    QTextEdit, QGroupBox, QRadioButton, QButtonGroup, QMessageBox,
    QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class FFmpegWorker(QThread):
    """Worker thread for running ffmpeg conversions"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, input_file, output_file, video_args, audio_args):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.video_args = video_args
        self.audio_args = audio_args

    def run(self):
        try:
            # Build command
            cmd = ['ffmpeg', '-i', self.input_file]
            cmd.extend(self.video_args.split())
            cmd.extend(self.audio_args.split())
            cmd.append(self.output_file)

            # Run ffmpeg
            self.progress.emit(f"Running: {' '.join(cmd)}\n")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Read output
            for line in process.stderr:
                self.progress.emit(line)

            process.wait()

            if process.returncode == 0:
                self.finished.emit(True, f"✓ Conversion complete: {self.output_file}")
            else:
                self.finished.emit(False, "✗ Conversion failed")

        except Exception as e:
            self.finished.emit(False, f"✗ Error: {str(e)}")


class FFmpegConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.output_dir = str(Path.home())  # Default to home directory
        self.worker = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Universal FFmpeg Converter")
        self.setMinimumSize(700, 650)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)

        # Title
        title = QLabel("Universal FFmpeg Converter")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Input file section
        input_group = QGroupBox("Input File")
        input_layout = QVBoxLayout()

        self.input_label = QLabel("No file selected")
        self.input_label.setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;")
        input_layout.addWidget(self.input_label)

        btn_layout = QHBoxLayout()
        self.browse_btn = QPushButton("📁 Browse Files")
        self.browse_btn.clicked.connect(self.browse_file)
        self.browse_btn.setMinimumHeight(40)
        btn_layout.addWidget(self.browse_btn)

        input_layout.addLayout(btn_layout)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Output settings
        output_group = QGroupBox("Output Settings")
        output_layout = QVBoxLayout()

        # Output directory
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Save to:"))
        self.dir_label = QLabel(self.output_dir)
        self.dir_label.setStyleSheet("padding: 5px; background: #f0f0f0; border-radius: 3px;")
        self.dir_label.setWordWrap(True)
        dir_layout.addWidget(self.dir_label, 1)

        self.browse_dir_btn = QPushButton("📂 Choose Folder")
        self.browse_dir_btn.clicked.connect(self.browse_directory)
        self.browse_dir_btn.setMinimumHeight(35)
        dir_layout.addWidget(self.browse_dir_btn)
        output_layout.addLayout(dir_layout)

        # Output filename
        basename_layout = QHBoxLayout()
        basename_layout.addWidget(QLabel("Filename:"))
        self.basename_input = QLineEdit()
        self.basename_input.setPlaceholderText("Enter output filename (without extension)")
        basename_layout.addWidget(self.basename_input)
        output_layout.addLayout(basename_layout)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Format selection
        format_group = QGroupBox("Target Format")
        format_layout = QVBoxLayout()

        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "MP4 (H.264) - Universal compatibility",
            "MOV (ProRes 422) - High quality intermediate",
            "WebM (VP9) - Web optimized",
            "GIF (Animated) - 15fps, 640px width",
            "MP3 (Audio only) - 192kbps"
        ])
        self.format_combo.setMinimumHeight(35)
        format_layout.addWidget(self.format_combo)

        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        # Audio options
        audio_group = QGroupBox("Audio Options")
        audio_layout = QHBoxLayout()

        self.audio_group = QButtonGroup()
        self.audio_keep = QRadioButton("Keep audio")
        self.audio_remove = QRadioButton("Remove audio")
        self.audio_keep.setChecked(True)

        self.audio_group.addButton(self.audio_keep)
        self.audio_group.addButton(self.audio_remove)

        audio_layout.addWidget(self.audio_keep)
        audio_layout.addWidget(self.audio_remove)
        audio_layout.addStretch()

        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)

        # Convert button
        self.convert_btn = QPushButton("🎬 Convert")
        self.convert_btn.setMinimumHeight(50)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setEnabled(False)
        layout.addWidget(self.convert_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        # Log output
        log_group = QGroupBox("Conversion Log")
        log_layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(150)
        self.log_output.setStyleSheet("font-family: monospace;")
        log_layout.addWidget(self.log_output)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

    def browse_directory(self):
        """Open directory browser"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.output_dir,
            QFileDialog.Option.ShowDirsOnly
        )

        if dir_path:
            self.output_dir = dir_path
            self.dir_label.setText(dir_path)
            self.log_output.append(f"✓ Output directory: {dir_path}\n")

    def browse_file(self):
        """Open file browser"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            str(Path.home()),
            "Video Files (*.mp4 *.mkv *.mov *.avi *.webm *.flv *.m4v *.mpeg *.mpg);;All Files (*.*)"
        )

        if file_path:
            self.input_file = file_path
            self.input_label.setText(file_path)

            # Auto-fill basename
            if not self.basename_input.text():
                basename = Path(file_path).stem
                self.basename_input.setText(basename)

            # Auto-set output directory to input file's directory
            input_dir = str(Path(file_path).parent)
            self.output_dir = input_dir
            self.dir_label.setText(input_dir)

            self.convert_btn.setEnabled(True)
            self.log_output.append(f"✓ Selected: {file_path}\n")
            self.log_output.append(f"✓ Output directory: {input_dir}\n")

    def get_format_settings(self):
        """Get ffmpeg settings based on format selection"""
        format_idx = self.format_combo.currentIndex()

        formats = {
            0: ("mp4", "-c:v libx264 -crf 22 -preset medium"),
            1: ("mov", "-c:v prores_ks -profile:v 3"),
            2: ("webm", "-c:v libvpx-vp9 -crf 31 -b:v 0"),
            3: ("gif", "-vf fps=15,scale=640:-1 -loop 0 -gifflags +transdiff"),
            4: ("mp3", "-vn")
        }

        return formats.get(format_idx, ("mp4", "-c:v libx264 -crf 22 -preset medium"))

    def get_audio_settings(self):
        """Get audio settings"""
        format_idx = self.format_combo.currentIndex()

        # GIF and MP3 have special audio handling
        if format_idx == 3:  # GIF
            return "-an"
        elif format_idx == 4:  # MP3
            return "-c:a libmp3lame -b:a 192k"

        # Regular formats
        if self.audio_keep.isChecked():
            return "-c:a copy"
        else:
            return "-an"

    def start_conversion(self):
        """Start the conversion process"""
        if not self.input_file:
            QMessageBox.warning(self, "Error", "Please select an input file")
            return

        basename = self.basename_input.text().strip()
        if not basename:
            QMessageBox.warning(self, "Error", "Please enter an output filename")
            return

        # Get settings
        ext, video_args = self.get_format_settings()
        audio_args = self.get_audio_settings()

        # Build output path with directory
        output_file = os.path.join(self.output_dir, f"{basename}.{ext}")

        # Avoid overwrite
        if os.path.exists(output_file):
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_file = os.path.join(self.output_dir, f"{basename}_{timestamp}.{ext}")
            self.log_output.append(f"⚠ Output exists, using: {output_file}\n")

        # Disable UI
        self.convert_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.browse_dir_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate

        self.log_output.append(f"Starting conversion to {ext.upper()}...\n")

        # Start worker thread
        self.worker = FFmpegWorker(self.input_file, output_file, video_args, audio_args)
        self.worker.progress.connect(self.update_log)
        self.worker.finished.connect(self.conversion_finished)
        self.worker.start()

    def update_log(self, text):
        """Update log output"""
        self.log_output.append(text)
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )

    def conversion_finished(self, success, message):
        """Handle conversion completion"""
        self.log_output.append(f"\n{message}\n")

        # Re-enable UI
        self.convert_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.browse_dir_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)


def main():
    ffmpeg_path = shutil.which("ffmpeg")

    if not ffmpeg_path:
        QMessageBox.critical(
            None,
            "FFmpeg not found",
            "FFmpeg was not found in PATH.\n\n"
            "Please ensure ffmpeg is installed and accessible."
        )
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = FFmpegConverter()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
