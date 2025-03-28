import sys
import json
import os
import keyboard  # Add this import
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QSlider, QComboBox,
                            QFrame, QStackedWidget, QCheckBox, QColorDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QIcon, QColor, QPalette, QFont, QShortcut, QKeySequence

class OverlayUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Define color schemes
        self.color_schemes = {
            "Teal": {
                "accent_color": "#4ecca3",  # Teal
                "menu_color": "#232931",    # Dark blue-gray
                "control_color": "#393e46", # Medium gray
                "text_color": "#eeeeee"     # Off-white
            },
            "Purple": {
                "accent_color": "#ff79c6",  # Pink/Purple (like original)
                "menu_color": "#282a36",    # Dark blue-gray
                "control_color": "#44475a", # Medium gray
                "text_color": "#f8f8f2"     # Off-white
            },
            "Blue": {
                "accent_color": "#61afef",  # Blue
                "menu_color": "#1e2127",    # Dark gray
                "control_color": "#2c313a", # Medium gray
                "text_color": "#abb2bf"     # Light gray
            },
            "Green": {
                "accent_color": "#98c379",  # Green
                "menu_color": "#1e2127",    # Dark gray
                "control_color": "#2c313a", # Medium gray
                "text_color": "#abb2bf"     # Light gray
            },
            "Dark": {
                "accent_color": "#c678dd",  # Purple
                "menu_color": "#000000",    # Black
                "control_color": "#1a1a1a", # Very dark gray
                "text_color": "#ffffff"     # White
            },
            "Light": {
                "accent_color": "#e06c75",  # Red
                "menu_color": "#f0f0f0",    # Light gray
                "control_color": "#e1e1e1", # Slightly darker gray
                "text_color": "#383a42"     # Dark gray (for contrast)
            }
        }
        
        # Define settings first, before any UI initialization
        self.settings = {
            "snow_effect": False,
            "menu_scale": "100%",
            "background_dim": 50,
            "color_scheme": "Teal",
            "accent_color": self.color_schemes["Teal"]["accent_color"],
            "menu_color": self.color_schemes["Teal"]["menu_color"],
            "control_color": self.color_schemes["Teal"]["control_color"],
            "text_color": self.color_schemes["Teal"]["text_color"]
        }
        
        # Track visibility state
        self.is_visible = True
        
        # Set window properties for overlay
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Initialize UI
        self.init_ui()
        
        # Setup global hotkey (Ctrl+Space)
        keyboard.add_hotkey("ctrl+space", self.toggle_visibility)

        # Apply initial settings
        self.apply_settings()
    
    def check_hotkey_pressed(self):
        # This is a workaround for global hotkeys
        # In a real application, you would use a library like keyboard or pynput
        # to register global hotkeys that work even when the window is hidden
        try:
            from PyQt6.QtGui import QGuiApplication
            modifiers = QGuiApplication.keyboardModifiers()
            if modifiers == Qt.KeyboardModifier.ControlModifier:
                # This is not a perfect solution but helps for demonstration
                # In a real app, use a proper global hotkey library
                pass
        except:
            pass
    
    def init_ui(self):
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar and content area
        self.sidebar = self.create_sidebar()
        self.content_area = self.create_content_area()
        
        # Add to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)
        
        # Set window size and title
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle("Azuki | osu! cheats. Redefined.")
        
        # Set the default section name to "Features"
        self.central_widget.findChild(QLabel, "content_header").setText("Features")
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # App title
        title_label = QLabel("Overlay")
        title_label.setObjectName("app_title")
        layout.addWidget(title_label)
        
        # App version
        version_label = QLabel("v1.0.0")
        version_label.setObjectName("app_version")
        layout.addWidget(version_label)
        
        # User info section
        user_frame = QFrame()
        user_frame.setObjectName("user_frame")
        user_layout = QVBoxLayout(user_frame)
        
        user_name = QLabel("User Profile")
        user_name.setObjectName("user_name")
        user_status = QLabel("Active")
        user_status.setObjectName("user_status")
        
        user_layout.addWidget(user_name)
        user_layout.addWidget(user_status)
        
        layout.addWidget(user_frame)
        layout.addSpacing(20)
        
        # Navigation buttons
        nav_buttons = [
            ("Features", self.show_features),
            ("Visuals", self.show_visuals),
            ("Controls", self.show_controls),
            ("Settings", self.show_settings),
            ("Configuration", self.show_configuration)
        ]
        
        for text, callback in nav_buttons:
            button = QPushButton(text)
            button.setObjectName("nav_button")
            button.clicked.connect(callback)
            layout.addWidget(button)
        
        layout.addStretch()
        
        return sidebar
    
    def create_content_area(self):
        content = QWidget()
        content.setObjectName("content_area")
        
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Settings")
        header.setObjectName("content_header")
        layout.addWidget(header)
        
        # Stacked widget for different content pages
        self.stacked_widget = QStackedWidget()
        
        # Create pages
        self.features_page = self.create_features_page()
        self.visuals_page = self.create_visuals_page()
        self.controls_page = self.create_controls_page()
        self.settings_page = self.create_settings_page()
        self.config_page = self.create_config_page()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.features_page)
        self.stacked_widget.addWidget(self.visuals_page)
        self.stacked_widget.addWidget(self.controls_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.config_page)
        
        layout.addWidget(self.stacked_widget)
        
        return content
    
    def create_features_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Feature toggles
        toggle_frame = QFrame()
        toggle_layout = QVBoxLayout(toggle_frame)
        
        # Snow effect toggle
        snow_layout = QHBoxLayout()
        snow_title = QLabel("Snow Effect")
        snow_title.setObjectName("setting_title")
        snow_desc = QLabel("Toggles snow particle effect")
        snow_desc.setObjectName("setting_desc")
        
        # Create the checkbox with a name so we can find it later
        snow_toggle = QCheckBox()
        snow_toggle.setObjectName("snow_toggle")
        
        # Set initial state based on settings
        snow_toggle.setChecked(self.settings["snow_effect"])
        
        # Connect the state changed signal
        snow_toggle.stateChanged.connect(self.on_snow_toggle_changed)
        
        snow_title_layout = QVBoxLayout()
        snow_title_layout.addWidget(snow_title)
        snow_title_layout.addWidget(snow_desc)
        
        snow_layout.addLayout(snow_title_layout)
        snow_layout.addStretch()
        snow_layout.addWidget(snow_toggle)
        
        toggle_layout.addLayout(snow_layout)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("separator")
        toggle_layout.addWidget(separator)
        
        # Menu scale
        scale_layout = QHBoxLayout()
        scale_title = QLabel("Menu Scale")
        scale_title.setObjectName("setting_title")
        scale_desc = QLabel("Adjust the size of UI elements")
        scale_desc.setObjectName("setting_desc")
        
        scale_combo = QComboBox()
        scale_combo.setObjectName("scale_combo")
        scale_options = ["50%", "75%", "100%", "125%", "150%"]
        scale_combo.addItems(scale_options)
        scale_combo.setCurrentText(self.settings["menu_scale"])
        scale_combo.currentTextChanged.connect(lambda text: self.update_setting("menu_scale", text))
        
        scale_title_layout = QVBoxLayout()
        scale_title_layout.addWidget(scale_title)
        scale_title_layout.addWidget(scale_desc)
        
        scale_layout.addLayout(scale_title_layout)
        scale_layout.addStretch()
        scale_layout.addWidget(scale_combo)
        
        toggle_layout.addLayout(scale_layout)
        
        # Add a separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setObjectName("separator")
        toggle_layout.addWidget(separator2)
        
        # Background dim
        dim_layout = QVBoxLayout()
        dim_header = QHBoxLayout()
        dim_title = QLabel("Background Dim")
        dim_title.setObjectName("setting_title")
        dim_value = QLabel(f"{self.settings['background_dim']}%")
        dim_value.setObjectName("setting_value")
        
        dim_header.addWidget(dim_title)
        dim_header.addStretch()
        dim_header.addWidget(dim_value)
        
        dim_desc = QLabel("Adjust the opacity of background elements")
        dim_desc.setObjectName("setting_desc")
        
        dim_slider = QSlider(Qt.Orientation.Horizontal)
        dim_slider.setObjectName("dim_slider")
        dim_slider.setMinimum(0)
        dim_slider.setMaximum(100)
        dim_slider.setValue(self.settings["background_dim"])
        dim_slider.valueChanged.connect(lambda value: (
            dim_value.setText(f"{value}%"),
            self.update_setting("background_dim", value)
        ))
        
        dim_layout.addLayout(dim_header)
        dim_layout.addWidget(dim_desc)
        dim_layout.addWidget(dim_slider)
        
        toggle_layout.addLayout(dim_layout)
        
        layout.addWidget(toggle_frame)
        layout.addStretch()
        
        return page
    
    def on_snow_toggle_changed(self, state):
        # Update the setting
        is_checked = (state == Qt.CheckState.Checked.value)
        self.update_setting("snow_effect", is_checked)
        
        # Print for debugging
        print(f"Snow effect toggled: {is_checked}")
        
        # Here you could start a thread for the snow effect
        if is_checked:
            # Example of how you might start a thread
            print("Starting snow effect thread...")
            # In a real app, you would create and start a worker thread here
    
    def create_visuals_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Color scheme selector
        scheme_layout = QVBoxLayout()
        scheme_header = QHBoxLayout()
        
        scheme_title = QLabel("Color Scheme")
        scheme_title.setObjectName("section_header")
        
        scheme_header.addWidget(scheme_title)
        scheme_header.addStretch()
        
        scheme_desc = QLabel("Choose a predefined color scheme or customize your own")
        scheme_desc.setObjectName("setting_desc")
        
        scheme_combo = QComboBox()
        scheme_combo.setObjectName("scheme_combo")
        scheme_combo.addItems(list(self.color_schemes.keys()))
        scheme_combo.setCurrentText(self.settings["color_scheme"])
        scheme_combo.currentTextChanged.connect(self.apply_color_scheme)
        
        scheme_layout.addLayout(scheme_header)
        scheme_layout.addWidget(scheme_desc)
        scheme_layout.addWidget(scheme_combo)
        
        layout.addLayout(scheme_layout)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("separator")
        layout.addWidget(separator)
        
        # Colors section header
        colors_header = QLabel("Custom Colors")
        colors_header.setObjectName("section_header")
        layout.addWidget(colors_header)
        
        colors_desc = QLabel("Customize individual colors (overrides the selected color scheme)")
        colors_desc.setObjectName("setting_desc")
        layout.addWidget(colors_desc)
        
        # Color settings
        color_settings = [
            ("Accent Color", "accent_color"),
            ("Menu Color", "menu_color"),
            ("Control Color", "control_color"),
            ("Text Color", "text_color")
        ]
        
        for label_text, setting_key in color_settings:
            color_layout = QHBoxLayout()
            
            color_label = QLabel(label_text)
            color_label.setObjectName("setting_title")
            
            color_button = QPushButton()
            color_button.setObjectName(f"{setting_key}_button")
            color_button.setFixedSize(30, 30)
            color_button.setStyleSheet(f"background-color: {self.settings[setting_key]};")
            color_button.clicked.connect(lambda checked, key=setting_key: self.pick_color(key))
            
            color_layout.addWidget(color_label)
            color_layout.addStretch()
            color_layout.addWidget(color_button)
            
            layout.addLayout(color_layout)
        
        # Reset to scheme button
        reset_button = QPushButton("Reset to Selected Scheme")
        reset_button.setObjectName("action_button")
        reset_button.clicked.connect(self.reset_to_scheme)
        layout.addWidget(reset_button)
        
        layout.addStretch()
        
        return page
    
    def apply_color_scheme(self, scheme_name):
        if scheme_name in self.color_schemes:
            # Update the color scheme setting
            self.update_setting("color_scheme", scheme_name)
            
            # Apply the colors from the scheme
            for key, value in self.color_schemes[scheme_name].items():
                self.settings[key] = value
            
            # Update the UI
            self.apply_settings()
            
            # Update color buttons
            for setting_key in ["accent_color", "menu_color", "control_color", "text_color"]:
                button = self.findChild(QPushButton, f"{setting_key}_button")
                if button:
                    button.setStyleSheet(f"background-color: {self.settings[setting_key]};")
            
            print(f"Applied color scheme: {scheme_name}")
    
    def reset_to_scheme(self):
        # Reset to the currently selected color scheme
        scheme_name = self.settings["color_scheme"]
        self.apply_color_scheme(scheme_name)
    
    def create_controls_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        controls_label = QLabel("Controls Settings")
        controls_label.setObjectName("section_header")
        layout.addWidget(controls_label)
        
        # Hotkey settings
        hotkey_layout = QHBoxLayout()
        hotkey_label = QLabel("Toggle Visibility Hotkey")
        hotkey_label.setObjectName("setting_title")
        hotkey_value = QLabel("Ctrl+Space")
        hotkey_value.setObjectName("setting_value")
        
        hotkey_layout.addWidget(hotkey_label)
        hotkey_layout.addStretch()
        hotkey_layout.addWidget(hotkey_value)
        
        layout.addLayout(hotkey_layout)
        
        # Add a note about the hotkey
        hotkey_note = QLabel("Note: Press Ctrl+Space to show/hide the overlay. If the overlay is hidden, you'll need to use the hotkey to bring it back.")
        hotkey_note.setObjectName("setting_desc")
        hotkey_note.setWordWrap(True)
        layout.addWidget(hotkey_note)
        
        # Add a button to show the overlay (useful for testing)
        show_button = QPushButton("Show Overlay")
        show_button.setObjectName("action_button")
        show_button.clicked.connect(self.show_overlay)
        layout.addWidget(show_button)
        
        layout.addStretch()
        
        return page
    
    def show_overlay(self):
        # Force show the overlay
        self.show()
        self.activateWindow()
        self.is_visible = True
    
    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        settings_label = QLabel("Application Settings")
        settings_label.setObjectName("section_header")
        layout.addWidget(settings_label)
        
        # Start with Windows
        startup_layout = QHBoxLayout()
        startup_label = QLabel("Start with Windows")
        startup_label.setObjectName("setting_title")
        startup_toggle = QCheckBox()
        startup_toggle.setObjectName("startup_toggle")
        
        startup_layout.addWidget(startup_label)
        startup_layout.addStretch()
        startup_layout.addWidget(startup_toggle)
        
        layout.addLayout(startup_layout)
        
        # Minimize to tray
        tray_layout = QHBoxLayout()
        tray_label = QLabel("Minimize to System Tray")
        tray_label.setObjectName("setting_title")
        tray_toggle = QCheckBox()
        tray_toggle.setObjectName("tray_toggle")
        
        tray_layout.addWidget(tray_label)
        tray_layout.addStretch()
        tray_layout.addWidget(tray_toggle)
        
        layout.addLayout(tray_layout)
        
        layout.addStretch()
        
        return page
    
    def create_config_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        config_label = QLabel("Configuration")
        config_label.setObjectName("section_header")
        layout.addWidget(config_label)
        
        # Save/Load settings
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Configuration")
        save_button.setObjectName("action_button")
        save_button.clicked.connect(self.save_config)
        
        load_button = QPushButton("Load Configuration")
        load_button.setObjectName("action_button")
        load_button.clicked.connect(self.load_config)
        
        reset_button = QPushButton("Reset to Defaults")
        reset_button.setObjectName("action_button")
        reset_button.clicked.connect(self.reset_config)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(load_button)
        buttons_layout.addWidget(reset_button)
        
        layout.addLayout(buttons_layout)
        
        # Preview section
        preview_label = QLabel("Color Scheme Preview")
        preview_label.setObjectName("section_header")
        layout.addWidget(preview_label)
        
        # Create a grid of color scheme previews
        from PyQt6.QtWidgets import QGridLayout
        preview_grid = QGridLayout()
        
        row, col = 0, 0
        for scheme_name, colors in self.color_schemes.items():
            preview_frame = QFrame()
            preview_frame.setObjectName("preview_frame")
            preview_frame.setFixedSize(150, 100)
            preview_frame.setStyleSheet(f"""
                #preview_frame {{
                    background-color: {colors["menu_color"]};
                    border: 1px solid #555555;
                    border-radius: 5px;
                }}
                #preview_title {{
                    color: {colors["accent_color"]};
                    font-weight: bold;
                }}
                #preview_content {{
                    background-color: {colors["control_color"]};
                    border-radius: 3px;
                }}
                #preview_text {{
                    color: {colors["text_color"]};
                }}
            """)
            
            preview_layout = QVBoxLayout(preview_frame)
            
            preview_title = QLabel(scheme_name)
            preview_title.setObjectName("preview_title")
            preview_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            preview_content = QFrame()
            preview_content.setObjectName("preview_content")
            content_layout = QVBoxLayout(preview_content)
            
            preview_text = QLabel("Sample Text")
            preview_text.setObjectName("preview_text")
            preview_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            content_layout.addWidget(preview_text)
            
            preview_layout.addWidget(preview_title)
            preview_layout.addWidget(preview_content)
            
            # Add a button to apply this scheme
            apply_button = QPushButton(f"Apply {scheme_name}")
            apply_button.setObjectName("small_button")
            apply_button.clicked.connect(lambda checked, name=scheme_name: self.apply_color_scheme(name))
            
            preview_layout.addWidget(apply_button)
            
            preview_grid.addWidget(preview_frame, row, col)
            
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        layout.addLayout(preview_grid)
        layout.addStretch()
        
        return page
    
    def show_features(self):
        self.stacked_widget.setCurrentIndex(0)
        self.central_widget.findChild(QLabel, "content_header").setText("Features")
    
    def show_visuals(self):
        self.stacked_widget.setCurrentIndex(1)
        self.central_widget.findChild(QLabel, "content_header").setText("Visuals")
    
    def show_controls(self):
        self.stacked_widget.setCurrentIndex(2)
        self.central_widget.findChild(QLabel, "content_header").setText("Controls")
    
    def show_settings(self):
        self.stacked_widget.setCurrentIndex(3)
        self.central_widget.findChild(QLabel, "content_header").setText("Settings")
    
    def show_configuration(self):
        self.stacked_widget.setCurrentIndex(4)
        self.central_widget.findChild(QLabel, "content_header").setText("Configuration")
    
    def toggle_visibility(self):
        if self.is_visible:
            self.hide()
            self.is_visible = False
            print("UI hidden - press Ctrl+Space to show again")
        else:
            self.show()
            self.activateWindow()  # Bring to front
            self.is_visible = True
            print("UI shown")
    
    def update_setting(self, key, value):
        self.settings[key] = value
        print(f"Updated {key} to {value}")
        
        # Apply the setting immediately
        if key in ["accent_color", "menu_color", "control_color", "text_color"]:
            self.apply_settings()
    
    def pick_color(self, setting_key):
        current_color = QColor(self.settings[setting_key])
        color = QColorDialog.getColor(current_color, self)
        
        if color.isValid():
            self.settings[setting_key] = color.name()
            
            # Update the button color directly
            button = self.findChild(QPushButton, f"{setting_key}_button")
            if button:
                button.setStyleSheet(f"background-color: {color.name()};")
            
            # Set color scheme to "Custom" since we're customizing colors
            self.settings["color_scheme"] = "Custom"
            scheme_combo = self.findChild(QComboBox, "scheme_combo")
            if scheme_combo and "Custom" not in [scheme_combo.itemText(i) for i in range(scheme_combo.count())]:
                scheme_combo.addItem("Custom")
            if scheme_combo:
                scheme_combo.setCurrentText("Custom")
        
        self.apply_settings()
    
    def apply_settings(self):
        # Apply colors and other settings to the UI
        stylesheet = f"""
            QWidget {{
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            #sidebar {{
                background-color: {self.settings["menu_color"]};
                border-right: 1px solid #3a3a3a;
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
            }}
            
            #content_area {{
                background-color: {self.settings["control_color"]};
                color: {self.settings["text_color"]};
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }}
            
            #app_title {{
                color: {self.settings["accent_color"]};
                font-size: 24px;
                font-weight: bold;
            }}
            
            #app_version {{
                color: #888888;
                font-size: 12px;
            }}
            
            #user_frame {{
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
                padding: 10px;
            }}
            
            #user_name {{
                color: {self.settings["text_color"]};
                font-size: 16px;
                font-weight: bold;
            }}
            
            #user_status {{
                color: {self.settings["accent_color"]};
                font-size: 12px;
            }}
            
            #nav_button {{
                background-color: transparent;
                color: {self.settings["text_color"]};
                border: none;
                text-align: left;
                padding: 10px;
                border-radius: 5px;
            }}
            
            #nav_button:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            
            #content_header {{
                color: {self.settings["accent_color"]};
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            
            #section_header {{
                color: {self.settings["accent_color"]};
                font-size: 18px;
                font-weight: bold;
                margin-top: 10px;
                margin-bottom: 15px;
            }}
            
            #setting_title {{
                color: {self.settings["text_color"]};
                font-size: 16px;
                font-weight: bold;
            }}
            
            #setting_desc {{
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
            }}
            
            #setting_value {{
                color: {self.settings["accent_color"]};
                font-size: 14px;
            }}
            
            #separator {{
                background-color: rgba(255, 255, 255, 0.1);
                height: 1px;
                margin: 15px 0;
            }}
            
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #555555;
            }}
            
            QCheckBox::indicator:unchecked {{
                background-color: transparent;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {self.settings["accent_color"]};
                border: 2px solid {self.settings["accent_color"]};
            }}
            
            QSlider::groove:horizontal {{
                height: 8px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }}
            
            QSlider::handle:horizontal {{
                background: {self.settings["accent_color"]};
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }}
            
            QSlider::sub-page:horizontal {{
                background: {self.settings["accent_color"]};
                border-radius: 4px;
            }}
            
            QComboBox {{
                background-color: rgba(0, 0, 0, 0.2);
                color: {self.settings["text_color"]};
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                min-width: 100px;
            }}
            
            QComboBox::drop-down {{
                border: none;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {self.settings["menu_color"]};
                color: {self.settings["text_color"]};
                selection-background-color: {self.settings["accent_color"]};
                selection-color: {self.settings["text_color"]};
                border: 1px solid #555555;
            }}
            
            #color_button {{
                border: 2px solid #555555;
                border-radius: 15px;
            }}
            
            #action_button {{
                background-color: rgba(0, 0, 0, 0.2);
                color: {self.settings["text_color"]};
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px 15px;
            }}
            
            #action_button:hover {{
                background-color: {self.settings["accent_color"]};
                color: #ffffff;
                border: 1px solid {self.settings["accent_color"]};
            }}
            
            #small_button {{
                background-color: rgba(0, 0, 0, 0.2);
                color: {self.settings["text_color"]};
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 4px 8px;
                font-size: 11px;
            }}
            
            #small_button:hover {{
                background-color: {self.settings["accent_color"]};
                color: #ffffff;
                border: 1px solid {self.settings["accent_color"]};
            }}
        """
        
        self.setStyleSheet(stylesheet)
        
        # Update color buttons
        for setting_key in ["accent_color", "menu_color", "control_color", "text_color"]:
            button = self.findChild(QPushButton, f"{setting_key}_button")
            if button:
                button.setStyleSheet(f"background-color: {self.settings[setting_key]};")
    
    def save_config(self):
        # In a real app, you would save to a file
        try:
            with open('overlay_config.json', 'w') as f:
                json.dump(self.settings, f)
            print("Configuration saved to overlay_config.json")
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def load_config(self):
        # In a real app, you would load from a file
        try:
            if os.path.exists('overlay_config.json'):
                with open('overlay_config.json', 'r') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
                    self.apply_settings()
                    
                    # Update UI elements with loaded settings
                    snow_toggle = self.findChild(QCheckBox, "snow_toggle")
                    if snow_toggle:
                        snow_toggle.setChecked(self.settings["snow_effect"])
                    
                    scale_combo = self.findChild(QComboBox, "scale_combo")
                    if scale_combo:
                        scale_combo.setCurrentText(self.settings["menu_scale"])
                    
                    dim_slider = self.findChild(QSlider, "dim_slider")
                    if dim_slider:
                        dim_slider.setValue(self.settings["background_dim"])
                    
                    scheme_combo = self.findChild(QComboBox, "scheme_combo")
                    if scheme_combo:
                        if self.settings["color_scheme"] not in [scheme_combo.itemText(i) for i in range(scheme_combo.count())]:
                            scheme_combo.addItem(self.settings["color_scheme"])
                        scheme_combo.setCurrentText(self.settings["color_scheme"])
                    
                print("Configuration loaded from overlay_config.json")
            else:
                print("No configuration file found")
        except Exception as e:
            print(f"Error loading configuration: {e}")
    
    def reset_config(self):
        # Reset to default settings
        self.settings = {
            "snow_effect": False,
            "menu_scale": "100%",
            "background_dim": 50,
            "color_scheme": "Teal",
            "accent_color": self.color_schemes["Teal"]["accent_color"],
            "menu_color": self.color_schemes["Teal"]["menu_color"],
            "control_color": self.color_schemes["Teal"]["control_color"],
            "text_color": self.color_schemes["Teal"]["text_color"]
        }
        
        # Update UI elements with default settings
        snow_toggle = self.findChild(QCheckBox, "snow_toggle")
        if snow_toggle:
            snow_toggle.setChecked(False)
        
        scale_combo = self.findChild(QComboBox, "scale_combo")
        if scale_combo:
            scale_combo.setCurrentText("100%")
        
        dim_slider = self.findChild(QSlider, "dim_slider")
        if dim_slider:
            dim_slider.setValue(50)
        
        scheme_combo = self.findChild(QComboBox, "scheme_combo")
        if scheme_combo:
            scheme_combo.setCurrentText("Teal")
        
        self.apply_settings()
        print("Reset to default configuration")
    
    def mousePressEvent(self, event):
        # For dragging the window
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        # For dragging the window
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def closeEvent(self, event):
        # Remove the global hotkey when the application is closed
        keyboard.unhook_all_hotkeys()
        super().closeEvent(event)

# Example of a worker thread that could be used for checkbox functionality
class Worker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self, function):
        super().__init__()
        self.function = function
    
    def run(self):
        # Run the function
        self.function()
        self.finished.emit()

def main():
    app = QApplication(sys.argv)
    window = OverlayUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()