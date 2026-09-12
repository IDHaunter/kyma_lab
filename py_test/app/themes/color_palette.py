from abc import ABC
from typing import Tuple

class ColorPalette(ABC):
    """
    Abstract base class for a color palette used in theming UI components.
    Each concrete implementation should define specific hex color codes.
    """

    COLOR_PRIMARY: str
    COLOR_SECONDARY: str
    COLOR_BACKGROUND: str        # Color for background
    COLOR_CONTAINER: str         # Color for any containers
    COLOR_TEXT: str              # Color for regular text
    COLOR_TEXT_HIGHLIGHTED: str  # Color for emphasized titles or headings

    @staticmethod
    def clamp(value: int) -> int:
        """
        Clamp an integer value between 0 and 255.
        """
        if value < 0:
            return 0
        elif value > 255:
            return 255
        else:
            return value

    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """
        Convert a hex color string (e.g., "#ffcc00" or "#fc0") to an (R, G, B) tuple.
        """
        hex_color = hex_color.lstrip('#')

        if not all(c in "0123456789abcdefABCDEF" for c in hex_color):
            raise ValueError(f"Invalid hex characters: #{hex_color}")

        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: #{hex_color}")
        return (
            int(hex_color[0:2], 16),  # 16 - hexadecimal number system
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """
        Convert an (R, G, B) tuple to a hex color string.
        """
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    @staticmethod
    def adjust_brightness(color: str, percent: float) -> str:
        """
        Adjust brightness of a color by a percentage (-100 to 100).
        Positive values lighten the color, negative values darken it.
        """
        rgb = ColorPalette.hex_to_rgb(color)
        factor = percent / 100.0

        if factor > 0:
            # Lighten: move towards white (255)
            r, g, b = (ColorPalette.clamp(int(c + (255 - c) * factor)) for c in rgb)
        else:
            # Darken: move towards black (0)
            r, g, b = (ColorPalette.clamp(int(c * (1 + factor))) for c in rgb)

        adjusted = (r, g, b)
        return ColorPalette.rgb_to_hex(adjusted)

    @staticmethod
    def lighten(color: str, percent: float = 10.0) -> str:
        """Lightens the given hex color by the specified percentage (default: 10%)."""
        return ColorPalette.adjust_brightness(color, abs(percent))

    @staticmethod
    def darken(color: str, percent: float = 10.0) -> str:
        """Darkens the given hex color by the specified percentage (default: 10%)."""
        return ColorPalette.adjust_brightness(color, -abs(percent))


class LightThemePalette(ColorPalette):
    """A light color palette for UI theming."""
    COLOR_PRIMARY = "#424B67"
    COLOR_SECONDARY = "#008db8"
    COLOR_BACKGROUND = "#f9f9f9"
    COLOR_CONTAINER = "#ffffff"
    COLOR_TEXT = "#000000"
    COLOR_TEXT_HIGHLIGHTED = ColorPalette.darken(COLOR_SECONDARY, 20)


class DarkThemePalette(ColorPalette):
    """A Dark color palette for UI theming."""
    COLOR_PRIMARY = "#424B67"
    COLOR_SECONDARY = "#008db8"
    COLOR_BACKGROUND = "#121212"
    COLOR_CONTAINER = "#1e1e1e"
    COLOR_TEXT = "#aaaaaa"
    COLOR_TEXT_HIGHLIGHTED = ColorPalette.lighten(COLOR_PRIMARY, 70)


# ---------------------------- Color Testing and HTML Generation ----------------------------

def print_color_preview(name: str, hex_color: str, palette: ColorPalette):
    """
    Print the original color and its lightened/darkened variants.
    """
    light = palette.lighten(hex_color, 20)
    dark = palette.darken(hex_color, 20)

    print(f"{name:<18}: {hex_color} | Lighten 20% → {light} | Darken 20% → {dark}")

def print_palette(palette: ColorPalette, title: str):
    """
    Display the full palette with transformations in the console.
    """
    print(f"\n=== {title} ===")
    print_color_preview("COLOR_PRIMARY", palette.COLOR_PRIMARY, palette)
    print_color_preview("COLOR_SECONDARY", palette.COLOR_SECONDARY, palette)
    print_color_preview("COLOR_BACKGROUND", palette.COLOR_BACKGROUND, palette)
    print_color_preview("COLOR_CONTAINER", palette.COLOR_CONTAINER, palette)
    print_color_preview("COLOR_TEXT", palette.COLOR_TEXT, palette)

def generate_realistic_preview_html(palette: type[ColorPalette], title: str, filename: str = "realistic_preview.html"):
    logo_url = "logo.png"

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{
                background-color: {palette.COLOR_BACKGROUND};
                color: {palette.COLOR_TEXT};
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            h1 {{
                color: {palette.COLOR_TEXT_HIGHLIGHTED};
            }}
            .container {{
                background-color: {palette.COLOR_CONTAINER};
                margin: 50px auto;
                padding: 30px;
                border-radius: 12px;
                max-width: 800px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            }}
            .primary-button {{
                background-color: {palette.COLOR_PRIMARY};
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                cursor: pointer;
                margin: 10px 0;
            }}
            .secondary-badge {{
                display: inline-block;
                background-color: {palette.COLOR_SECONDARY};
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 14px;
                margin-left: 10px;
            }}                    
            .footer {{
                        margin-top: 40px;
                        font-size: 14px;
                        color: {palette.COLOR_TEXT};
                    }}
                    .footer img {{
                        height: 30px;
                        vertical-align: middle;
                        margin-top: 0;
                        margin-right: 0px;
                        margin-bottom: 0;
                        margin-left: 1px;
                    }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <p>This is a preview of the theme with realistic layout and colors.</p>

            <button class="primary-button">Primary Action</button>
            <span class="secondary-badge">Secondary</span>

            <p style="margin-top: 30px;">Background: <code>{palette.COLOR_BACKGROUND}</code><br>
            Container: <code>{palette.COLOR_CONTAINER}</code><br>
            Primary: <code>{palette.COLOR_PRIMARY}</code><br>
            Secondary: <code>{palette.COLOR_SECONDARY}</code><br>
            Text: <code>{palette.COLOR_TEXT}</code><br>
            Text Highlighted: <code>{palette.COLOR_TEXT_HIGHLIGHTED}</code></p>
            
            <div class="footer">
            Plant your <img src="{logo_url}" alt="o">wn tree of knowledge
            </div>
        </div>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Realistic HTML preview saved to {filename}")


# Example usage and preview generation
if __name__ == '__main__':
    print_palette(LightThemePalette(), "Light Theme")
    print_palette(DarkThemePalette(), "Dark Theme")

    print()  # Spacer
    generate_realistic_preview_html(LightThemePalette, "Light Theme Preview", "light_theme_preview.html")
    generate_realistic_preview_html(DarkThemePalette, "Dark Theme Preview", "dark_theme_preview.html")
