The scanner collects all forms from the page and checks them for LFI vulnerability

### 1. Install:
```pycon
git clone 
cd LFI_Form_Scanner
```

```pycon
1. Create a virtual environment:
    python -m venv .venv

2. Activate the virtual environment:
    On Windows:
    .venv\Scripts\activate
    
    On macOS/Linux:
    source .venv/bin/activate

pip install -r requirements.txt
pip freeze > requirements.txt
```


```pycon
python run_lfi_form_scanner.py
```

### 2. Setting:
```text
input_data - Folder with the file with links or specify the absolute path in the 'path_to_links_to_crawler' value
logs - Folder with logs
report - Folder with reports

path_to_links_to_crawler - Path to file with links for crawler
submit_form_post - Enable submission of forms via POST
verbose - Show verbose output
max_concurrent_requests - Number of threads

MAX_RETRIES = 2  Retry failed requests с задержкой между попытками
RETRY_DELAY = 2  Delay between attempts to retry unsuccessful requests in seconds
```

### 3. Sample output:
```text
1. http://example.com/wp-content/uploads/404.php
<form method="GET" name="404.php">
<input id="cmd" name="cmd" size="80" type="TEXT"/>
<input type="SUBMIT" value="Execute"/>
</form>
- - - - - - - - - - - - - - - - - - - - - - - - - 
[***] 💉 Payload: [(True, 'ls -la')]
 = = = = = = = = = = = = = = = = = = = = = = = = = 
```