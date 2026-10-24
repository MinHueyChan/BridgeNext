"""Package reproducible source, excluding hosted-site identity and runtime state."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parents[1]
out=root/'public/downloads/BridgeNext-Replit.zip'
out.parent.mkdir(parents=True,exist_ok=True)
excluded={'node_modules','dist','.git','.openai','__pycache__','.venv'}
with ZipFile(out,'w',ZIP_DEFLATED) as z:
 for file in sorted(root.rglob('*')):
  relative=file.relative_to(root)
  if not file.is_file() or any(p in excluded for p in relative.parts):continue
  if relative.parts[:2]==('public','downloads') or file.suffix in {'.sqlite','.pyc','.tsbuildinfo'} or '.sqlite' in file.name:continue
  if file.name.startswith('.env') and file.name!='.env.example':continue
  z.write(file,Path('BridgeNext-Replit')/relative)
print(f'Replit source packaged: {out.stat().st_size:,} bytes')
