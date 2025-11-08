# GymIA Integration Project

This project integrates the GymIA library for hand pose detection and other functionalities. It is structured to facilitate easy development and testing.

## Project Structure

```
gymia-vscode-project
├── .vscode
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
├── src
│   ├── main.py
│   ├── gymia_integration
│   │   ├── __init__.py
│   │   └── connector.py
│   └── utils
│       └── __init__.py
├── notebooks
│   └── Handpose Tutorial.ipynb
├── third_party
│   └── GymIA
│       └── (cloned or added as a git submodule)
├── tests
│   └── test_integration.py
├── requirements.txt
├── environment.yml
├── .gitignore
└── README.md
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/hachemboudoukha/GymIA.git
cd gymia-vscode-project
pip install -r requirements.txt
```

Alternatively, you can create a conda environment using the `environment.yml` file:

```bash
conda env create -f environment.yml
```

## Usage

Run the main application using:

```bash
python src/main.py
```

For hand pose detection, refer to the Jupyter notebook located in the `notebooks` directory.

## Testing

To run the tests, execute:

```bash
python -m unittest discover -s tests
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.