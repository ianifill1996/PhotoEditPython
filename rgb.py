rgb_py_content =""
class RGB:
    def __init__(self, red, green, blue, alpha=255):
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)
        self.alpha = int(alpha)

    def rgba(self):
        return (self.red, self.green, self.blue, self.alpha)

    def __repr__(self):
        return f"RGB({self.red}, {self.green}, {self.blue}, {self.alpha})"


# Save this to a file so the user can download it
with open("/mnt/data/rgb.py", "w") as f:
    f.write(rgb_py_content)

"/mnt/data/rgb.py"