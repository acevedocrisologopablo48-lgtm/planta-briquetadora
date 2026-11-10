from pathlib import Path
from shutil import copy2, copyfileobj
from gzip import GzipFile
import json
root=Path.cwd();target=root/'_site';assets=set(json.loads((root/'.github/pages-assets.json').read_text()))
files=[];cad=[]
for file in root.rglob('*'):
    if not file.is_file():continue
    rel=file.relative_to(root)
    if rel.parts[0] in ['.git','.github','_site']:continue
    if file.suffix.lower() in ['.dxf','.dwg']:
        cad.append({'archivo':str(rel).replace(chr(92),'/'),'url':'https://raw.githubusercontent.com/acevedocrisologopablo48-lgtm/planta-briquetadora/main/'+str(rel).replace(chr(92),'/')})
        continue
    if rel.parts[0]=='assets' and file.name not in assets:continue
    if len(rel.parts)==1 and file.match('catalogo-equipos*.json') and file.name!='catalogo-equipos-r30.json':
        continue  # The viewer loads archived revisions from the public repository on demand.
    files.append((file,rel))
for file,rel in files:
    dest=target/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    if len(rel.parts)==1 and file.match('catalogo-equipos*.json'):
        with file.open('rb') as original, dest.with_suffix('.json.gz').open('wb') as compressed:
            with GzipFile(filename='',mode='wb',fileobj=compressed,compresslevel=5,mtime=0) as archive:
                copyfileobj(original,archive)
        # Retain the plain current catalog for cached builds and fallback clients.
    copy2(file,dest)
(target/'archivos-cad.json').write_text(json.dumps(cad,ensure_ascii=False,indent=2),encoding='utf-8')
size=sum(file.stat().st_size for file in target.rglob('*') if file.is_file())
assert size<500_000_000,('Artefacto excede el margen de publicacion',size)
print('Pages:',len(files),'archivos,',round(size/1e6,1),'MB. Originales CAD conservados en repositorio.')
