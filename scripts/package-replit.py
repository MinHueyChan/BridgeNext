"""Package source without dependencies, temporary tools or runtime state."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import os
root=Path(__file__).resolve().parents[1]
excluded={'node_modules','dist','.git','.openai','__pycache__','.venv','.test-tools'}

def package_source(out):
    out=Path(out).resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(out,'w',ZIP_DEFLATED) as archive:
        for directory,children,names in os.walk(root):
            children[:]=sorted(name for name in children if name not in excluded)
            for name in sorted(names):
                file=Path(directory)/name
                relative=file.relative_to(root)
                if relative.parts[:2]==('public','downloads') or file.resolve()==out:continue
                if file.suffix in {'.pyc','.tsbuildinfo'} or '.sqlite' in file.name:continue
                if file.name.startswith('.env') and file.name!='.env.example':continue
                archive.write(file,Path('BridgeNext-Replit')/relative)
    return out.stat().st_size

if __name__=='__main__':
    out=root/'public/downloads/BridgeNext-Replit.zip'
    print(f'Replit source packaged: {package_source(out):,} bytes')
