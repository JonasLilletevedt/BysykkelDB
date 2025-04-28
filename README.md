# OBLIG2 INF115

>[] Jobbet med
> @mkn0536

## TL;DR (Quick Start)

```bash
git clone [https://github.com/JL2023-coder/OBLIG-2](https://github.com/JL2023-coder/OBLIG-2)
cd OBLIG-2/
python3 -m venv .venv
source .venv/bin/activate  # Use appropriate activate command for your OS/shell (see below)
pip install -r requirements.txt
shiny run 1app.py          # Or 2app.py / 3and4app.py
```


## How to Set Up and Run

Follow these steps to set up the environment and run the Shiny web applications.

1.  **Clone the Repository:**
    Open your terminal or command prompt and download the project files from GitHub.
    ```bash
    git clone [https://github.com/JL2023-coder/OBLIG-2](https://github.com/JL2023-coder/OBLIG-2)
    ```

2.  **Navigate into Project Directory:**
    Change into the newly created project directory.
    ```bash
    cd OBLIG-2/
    ```

3.  **Create a Virtual Environment:**
    Create an isolated Python environment for the project. We'll name it `.venv`.
    ```bash
    python3 -m venv .venv
    ```

4.  **Activate the Virtual Environment:**
    Activate the environment using the command specific to your shell:

    * **Linux/macOS (bash/zsh):**
        ```bash
        source .venv/bin/activate
        ```
    * **Linux/macOS (fish):**
        ```fish
        source .venv/bin/activate.fish
        ```
    * **Windows (Command Prompt):**
        ```batch
        .\.venv\Scripts\activate.bat
        ```
    * **Windows (PowerShell):**
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```

    Your terminal prompt should now indicate that the `.venv` environment is active.

5.  **Install Requirements:**
    Install the necessary Python packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

6.  **Run the Websites:**
    The project contains three separate Shiny applications: `1app.py`, `2app.py`, and `3and4app.py`. 
    Each file creates its own website with its respective tasks.

    To run a specific application, use the `shiny run` command followed by the filename. For example:

    * **To run the first app:**
        ```bash
        shiny run 1app.py
        ```
    * **To run the second app:**
        ```bash
        shiny run 2app.py
        ```
    * **To run the third/fourth app:**
        ```bash
        shiny run 3and4app.py
        ```

    After running the command, Shiny will output a local URL (usually like `http://127.0.0.1:8000`). 
    Open this URL in your web browser to view the application. 
    You might need to stop one app (usually with `Ctrl+C` in the terminal) before starting another.

