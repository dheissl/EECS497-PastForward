# Setting Up Your Environment to Run the Application

## Prerequisites
- Ensure you have **Python 3.6+** installed on your system.
- Install **pip**, Python's package manager (usually included with Python installations).
- Install **virtualenv** if it’s not already installed:

```bash
pip install virtualenv
```

## Step 1: Create a Virtual Environment
Navigate to the directory where this project is located:

```bash
cd /path/to/your/project
```

Create a virtual environment named `venv`:

```bash
python -m virtualenv venv
```

## Step 2: Activate the Virtual Environment
On **Windows**:

```bash
venv\Scripts\activate
```

On **macOS/Linux**:

```bash
source venv/bin/activate
```

You should now see `(venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

## Step 3: Install Requirements
Ensure you have a `requirements.txt` file in your project directory.  
Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application
Once the dependencies are installed, you need to create the database and run the application.

### Destroy the old data:
```bash
./bin/pastforwarddb destroy
```

### Reset the data:
```bash
./bin/pastforwarddb create
```

### Run the application:
```bash
./bin/pastforwardrun
```

## Step 5: Using the Application
### Sign in the application:
For the most part the application is pretty simple. I do have premade accounts you must sign into to show off the full functionality though.
# USE USERNAME=sherry AND PASSWORD=password

## Step 6: Stop the Application

### Deactivate the port:
Push control + z to deactivate the application. ONLY USE THIS COMBO. control + z will keep the ports open and the application will not correctly shut down.

## Deactivating the Virtual Environment
When you're done working, deactivate the virtual environment by running:

```bash
deactivate
```

## Additional Notes
If you encounter issues message Dylan. There are some known bugs we will have to work around.

Always use the virtual environment to avoid conflicts with global Python packages.
