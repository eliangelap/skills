#!/usr/bin/env python3
import argparse, json, os
from pathlib import Path
IGNORE={'.git','node_modules','dist','build','.next','.cache','coverage','vendor','__pycache__','.idea','.vscode'}
MANIFESTS={'package.json','pom.xml','build.gradle','build.gradle.kts','requirements.txt','pyproject.toml','go.mod','Cargo.toml','composer.json','.csproj','Dockerfile','docker-compose.yml','docker-compose.yaml'}
EXTS={'.js','.jsx','.ts','.tsx','.java','.kt','.py','.go','.cs','.php','.xml','.sql','.ini','.toml','.yaml','.yml','.json','.md','.txt','.frm','.pro'}
def scan(root):
    root=Path(root).resolve(); projects=[]; files=[]
    for cur,dirs,names in os.walk(root):
        dirs[:]=[d for d in dirs if d not in IGNORE and not d.startswith('.')]
        cp=Path(cur)
        rel=str(cp.relative_to(root))
        manifests=[n for n in names if n in MANIFESTS or Path(n).suffix=='.csproj']
        if manifests: projects.append({'path':rel,'manifests':sorted(manifests)})
        for n in names:
            p=cp/n
            if p.suffix.lower() in EXTS or n in MANIFESTS:
                try: size=p.stat().st_size
                except OSError: continue
                files.append({'path':str(p.relative_to(root)),'ext':p.suffix.lower(),'size':size})
    by_ext={}
    for f in files: by_ext[f['ext']]=by_ext.get(f['ext'],0)+1
    return {'root':str(root),'projects':projects,'file_count':len(files),'by_extension':dict(sorted(by_ext.items(), key=lambda x:(-x[1],x[0]))),'files':files}
def main():
    ap=argparse.ArgumentParser(description='Inventory a multi-project software ecosystem without modifying it.')
    ap.add_argument('root'); ap.add_argument('--output','-o')
    a=ap.parse_args(); data=scan(a.root); text=json.dumps(data,ensure_ascii=False,indent=2)
    if a.output: Path(a.output).write_text(text,encoding='utf-8')
    else: print(text)
if __name__=='__main__': main()
