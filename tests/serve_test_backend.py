"""Optional local browser harness: never opens the application database."""
import sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import uvicorn
from backend import main as server
with tempfile.TemporaryDirectory(prefix='bridgenext-browser-') as tmp:
    server.DB=Path(tmp)/'browser.sqlite'
    uvicorn.run(server.app,host='127.0.0.1',port=8011,access_log=False)
