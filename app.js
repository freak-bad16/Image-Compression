const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();

const PORT = 3000;

const upload = multer({ dest: 'uploads/' });

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

app.post('/compress', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.render('index', { result: null, error: 'No file uploaded' });
  }

  const aggressive = req.body.aggressive === 'on';
  const inputPath = req.file.path;

  const colorOutput = `uploads/color_compressed_${Date.now()}.jpg`;
  const grayOutput = `uploads/gray_compressed_${Date.now()}.jpg`;

  const python = spawn('python', [
    'Dwt.py',
    '--image', inputPath,
    aggressive ? '--aggressive' : '',
    '--output_color', colorOutput,
    '--output_gray', grayOutput
  ].filter(Boolean));

  let result = '';
  let error = '';

  python.stdout.on('data', (data) => {
    result += data.toString();
  });

  python.stderr.on('data', (data) => {
    error += data.toString();
  });

  python.on('close', (code) => {
    if (code !== 0 || error) {
      return res.render('index', { result: null, error: error || 'Compression failed' });
    }

    try {
      const json = JSON.parse(result);
      const originalImage = fs.readFileSync(inputPath, { encoding: 'base64' });
      const compressedColor = fs.readFileSync(colorOutput, { encoding: 'base64' });
      const compressedGray = fs.readFileSync(grayOutput, { encoding: 'base64' });

      res.render('index', {
        result: {
          original_size: json.original_size,
          color: {
            compressed_size: json.color.compressed_size,
            compression_ratio: json.color.compression_ratio,
            image: `data:image/jpeg;base64,${compressedColor}`
          },
          grayscale: {
            compressed_size: json.grayscale.compressed_size,
            compression_ratio: json.grayscale.compression_ratio,
            image: `data:image/jpeg;base64,${compressedGray}`
          },
          original_image: `data:image/png;base64,${originalImage}`
        },
        error: null
      });
    } catch (e) {
      console.error('JSON Parse Error:', e);
      res.render('index', { result: null, error: 'Failed to parse Python output' });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
