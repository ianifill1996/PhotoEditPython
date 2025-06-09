# 🖼️ PicTool - Image Processing with Python

Welcome to **PicTool**, a lightweight, command-line image editor built entirely with Python. This project showcases the power of core programming concepts—like modular design, memory handling, and pixel manipulation—without relying on heavy frameworks.

## 📌 Project Description

PicTool is a Python-based application that allows users to apply various visual effects to `.png` images using plug-in functions. Users run the tool from the command line and choose from a range of transformations, like blurring, pixelation, vignette, grayscale, flipping, and more.

The project replaces the dependency on student-specific libraries like `introcs` with standard, reusable Python modules—including a custom `RGB` class and the `Pillow` library for image loading/saving.

---

## 🧠 Key Features

- 🎨 **Visual Filters**: Apply effects like `blur`, `pixellate`, `vignette`, `mono` (grayscale), `sepia`, `brighten`, and `scramble`
- 🔁 **Image Transformations**: Rotate, flip (horizontal/vertical), and transpose images
- 🔌 **Plug-in Architecture**: Add new filters by writing functions inside `plugins.py`
- 💻 **Command-Line Interface**: Fully controllable from the terminal using simple commands

---

## 🚀 Example Usage

```bash
# Apply a blur effect with a radius of 5
python pictool.py blur --radius=5 input.png output.png

# Apply a sepia tone
python pictool.py mono --sepia=True input.png output.png

# Brighten the image by 30%
python pictool.py brighten --factor=1.3 input.png output.png

# Randomly scramble 200 pixels
python pictool.py scramble --amount=200 input.png output.png
🧱 Project Structure
.
├── pictool.py       # Main controller script
├── plugins.py       # Image manipulation functions (plug-ins)
├── rgb.py           # Custom RGB class (replaces introcs)
├── input.png        # Your source image
├── output.png       # Result after editing
└── README.md        # You are here!

⚙️ Requirements

Install the Pillow library (for image handling):

pip install pillow
Python version: 3.x

✨ Author

Ian Ifill
Computer Science Student • Software Engineer
GitHub: [ianifill1996] • LinkedIn: [www.linkedin.com/in/ian-ifill-653ab3231]




