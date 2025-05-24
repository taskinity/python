# Contributing to Taskinity

Thank you for your interest in contributing to Taskinity! This document provides guidelines and instructions for contributing to both the Python package and the JavaScript rendering library.

## Table of Contents

- [Contributing to Python Package](#contributing-to-python-package)
- [Contributing to Render Script](#contributing-to-render-script)
- [Development Workflow](#development-workflow)
- [Publishing Process](#publishing-process)
- [Code Style](#code-style)
- [Testing](#testing)

## Contributing to Python Package

### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/taskinity/python.git
   cd python
   ```

2. Install dependencies:
   ```bash
   make install
   ```

3. Run tests to make sure everything is working:
   ```bash
   make test
   ```

### Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and run tests:
   ```bash
   make test
   ```

3. Commit your changes with a descriptive message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

## Contributing to Render Script

### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/taskinity/render.git
   cd render
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

### Making Changes

1. Edit files in the `src` directory
2. Test your changes by opening `examples/index.html` in a browser
3. Build the production version:
   ```bash
   npm run build
   ```

## Development Workflow

We follow a simple GitHub flow:

1. Fork the repository (if you're not a core contributor)
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request
6. Address review comments

## Publishing Process

### Publishing Python Package

To publish a new version of the Python package:

1. Update the version number:
   ```bash
   make version
   ```
   You'll be prompted to specify the version bump type (patch, minor, major).

2. Build and publish the package:
   ```bash
   make publish
   ```
   This will build the package and publish it to PyPI.

### Publishing Render Script

To publish a new version of the render script:

1. Update the version in `package.json`:
   ```bash
   cd render
   npm version patch  # or minor, or major
   ```

2. Build the production version:
   ```bash
   npm run build
   ```

3. Publish to GitHub Pages:
   ```bash
   # Assuming you have the GitHub Pages repository cloned
   cp dist/taskinity-render.min.js /path/to/taskinity.github.io/render/
   cd /path/to/taskinity.github.io
   git add render/taskinity-render.min.js
   git commit -m "Update render script to version X.Y.Z"
   git push
   ```

4. (Optional) Publish to npm:
   ```bash
   cd render
   npm publish
   ```

## Code Style

### Python

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document all public functions and classes

### JavaScript

- Follow ESLint configuration
- Use modern JavaScript features (ES6+)
- Document all public functions and classes with JSDoc

## Testing

### Python

Run tests with:
```bash
make test
```

### JavaScript

Run tests with:
```bash
cd render
npm test
```

## Documentation

When making changes, please update the relevant documentation:

- Update README.md if you change user-facing features
- Update docstrings for any modified functions
- Add examples for new features

## Questions?

If you have any questions about contributing, please open an issue or contact the maintainers.

Thank you for contributing to Taskinity!
