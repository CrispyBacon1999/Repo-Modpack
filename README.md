# REPO Modpack Packer

Quick and easy script that packs up all files in the `pack` folder as a zip file for easy upload to Thunderstore.

## Running

1. Install `uv`, a modern Python Package Manager

#### Windows

`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

#### Mac/Linux

`curl -LsSf https://astral.sh/uv/install.sh | sh`

2. Build the modpack

`uv run pack.py`
