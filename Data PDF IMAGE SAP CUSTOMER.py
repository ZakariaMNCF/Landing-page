const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

// Serve static files (HTML, CSS, JS)
app.use(express.static('public'));

// Endpoint to handle file uploads
app.post('/upload/:category/:subcategory', upload.single('file'), (req, res) => {
    const { category, subcategory } = req.params;
    const file = req.file;
    if (!file) {
        return res.status(400).json({ success: false, message: 'No file uploaded.' });
    }

    // Create category and subcategory folders if they don't exist
    const uploadDir = path.join(__dirname, 'uploads', category, subcategory);
    if (!fs.existsSync(uploadDir)) {
        fs.mkdirSync(uploadDir, { recursive: true });
    }

    // Move the file to the correct folder
    const newPath = path.join(uploadDir, file.originalname);
    fs.renameSync(file.path, newPath);

    res.json({ success: true, message: 'File uploaded successfully.' });
});

// Endpoint to list uploaded files
app.get('/files/:category/:subcategory', (req, res) => {
    const { category, subcategory } = req.params;
    const uploadDir = path.join(__dirname, 'uploads', category, subcategory);

    fs.readdir(uploadDir, (err, files) => {
        if (err) {
            return res.status(500).json({ success: false, message: 'Unable to scan files.' });
        }
        res.json({ success: true, files });
    });
});

// Serve uploaded files
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});