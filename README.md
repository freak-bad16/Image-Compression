# 📦 DWT Image Compression (Color + Grayscale)

A full-stack image compression web app using **Node.js (Express)** and **Python (OpenCV + PyWavelets)**.  
This tool compresses both **color** and **grayscale** versions of an image using **DWT (Haar Wavelet)** and shows you the compression ratio and preview images.

---

## 🚀 Features

- 🔹 Compress both **Color** and **Grayscale** images
- 🔹 Choose between **normal** and **aggressive** compression
- 🔹 View:
  - Original image
  - Compressed color image
  - Compressed grayscale image
- 🔹 See **size before/after** and **compression ratio**

---

## 📷 Example Output

| Type         | Size     | Compression Ratio |
|--------------|----------|--------------------|
| Original     | 8159 KB  | —                  |
| Color Output | 521 KB   | 15.65×             |
| Grayscale    | 456 KB   | 17.86×             |

---

## 📦 Dependencies

From `package.json`:

```json
{
  "express": "^4.18.2",
  "multer": "^1.4.4",
  "ejs": "^3.1.9"
}
Python dependencies (used in Dwt.py):

opencv-python

numpy

pywavelets

Install them using:

bash
Copy code
pip install opencv-python numpy PyWavelets
🛠️ How to Run
bash
Copy code
# 1. Clone this repo
git clone https://github.com/<your-username>/dwt-image-compression.git
cd dwt-image-compression

# 2. Install Node dependencies
npm install

# 3. Start the server
npm start

# 4. Visit in browser
http://localhost:3000
Make sure Python is installed and available in your system PATH.

📁 Project Structure
csharp
Copy code
📦 project-root/
├── app.js              # Express backend
├── Dwt.py              # Python DWT compression script
├── views/
│   └── index.ejs       # Frontend interface
├── public/             # Static assets
├── uploads/            # Temporary image uploads
├── package.json
├── .gitignore
└── README.md
📜 License
MIT License © 2025 Sumit Jha

🙌 Author
Built with 💻 by Sumit Jha
Connect with me on LinkedIn

yaml
Copy code

---

✅ Now your project is clean, properly documented, and ready for GitHub or sharing with recruiters/internships.

Let me know if you'd like me to help you:
- Add a badge (e.g. MIT License / Node version)
- Deploy this to **Render** or **Replit**
- Add screenshot or demo GIF to the README
