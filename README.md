
# GenZ

**GenZ** is a static site generator designed to create fast and lightweight websites using customizable templates. It leverages Python and shell scripting to generate static HTML content from source files, making it ideal for blogs, portfolios, and simple content-driven sites.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

GenZ is a static site generator aimed at developers and users who prefer simplicity and control over their web content. With minimal dependencies, this project allows you to generate websites using markdown files and templates. The site is built locally and can be easily deployed to any static web hosting provider.

## Features

- **Markdown Support**: Generate HTML content from Markdown files.
- **Custom Templates**: Use customizable HTML templates to control the layout.
- **Lightweight**: No heavy frameworks; focused on speed and simplicity.
- **Python-based**: Uses Python for generating the static site, making it easy to extend or modify.
- **Shell Scripts**: Contains convenient scripts for automating tasks.

## Installation

### Prerequisites

- Python 3.x
- Basic knowledge of shell scripting

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/username/GenZ.git
   cd GenZ
   ```

2. Install dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

3. Make the shell scripts executable:

   ```bash
   chmod +x main.sh
   chmod +x test.sh
   ```

## Usage

To generate the static site:

1. Run the main script to build the site:

   ```bash
   ./main.sh
   ```

   This script will take content from the `content` folder, apply the `template.html` layout, and generate the final HTML files in the `public` folder.

2. Preview the site locally by running the Python server:

   ```bash
   python server.py
   ```

   This will host the site locally at `http://localhost:8000`.

## File Structure

```
GenZ/
│
├── content/               # Source markdown files for the content
│   ├── index.md
│   └── majesty/
│       └── index.md
│
├── public/                # Generated HTML files
│   └── index.html
│
├── src/                   # Python source code
│   ├── htmlnode.py
│   ├── main.py
│   ├── test_htmlnode.py
│   ├── textnode.py
│   └── utils.py
│
├── static/                # Static assets (CSS, images)
│   ├── index.css
│   └── images/
│       └── rivendell.png
│
├── template.html          # HTML template for content rendering
├── main.sh                # Main script to generate the site
├── test.sh                # Test script
├── server.py              # Local server for previewing the site
└── README.md              # Project README file
```

## Configuration

- Modify the `template.html` file to customize the layout of the website.
- Place your content in the `content/` folder using markdown (`.md`) files.
- The generated HTML files will be output in the `public/` folder, ready for deployment.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

