from pathlib import Path
from shutil import copy2
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
    files.append((file,rel))
size=sum(f.stat().st_size for f,_ in files)
assert size<950_000_000,('Artefacto excede el margen de publicacion',size)
for file,rel in files:
    dest=target/rel;dest.parent.mkdir(parents=True,exist_ok=True);copy2(file,dest)
(target/'archivos-cad.json').write_text(json.dumps(cad,ensure_ascii=False,indent=2),encoding='utf-8')
print('Pages:',len(files),'archivos,',round(size/1e6,1),'MB. Originales CAD conservados en repositorio.')
