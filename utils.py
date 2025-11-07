import subprocess
from pathlib import Path
import shutil 
import os
import ast
import re
import os
import json 

BASE_CLONE_DIR = Path('repos')

def clone_repo(url: str, repo_name: str) -> str:
    if not url.endswith('.git'):
        url += '.git'

    repo_dir = BASE_CLONE_DIR / repo_name
    
    BASE_CLONE_DIR.mkdir(parents=True, exist_ok=True) 

    if (repo_dir / '.git').exists():
        return str(repo_dir) 

    try:
        subprocess.run(
            ['git', 'clone', url, str(repo_dir)], 
            check=True, 
            capture_output=True,
            text=True
        )
        
        return str(repo_dir)
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or e.stdout
        if repo_dir.is_dir() and not (repo_dir / '.git').exists():
            shutil.rmtree(repo_dir) 
            
        raise ValueError(f"Failed to clone repo to {repo_dir}: {e.cmd}\n{error_output}")
    
def file_tree_generator(repo_dir:str) -> list[dict]:
    result = []
    ignore_dirs = ['.git', 'node_modules', '__pycache__', 'venv', '.venv', '.env', 'dist', 'build']
    
    # Files/extensions to ignore within directories (like compiled files or logs)
    ignore_file_extensions = ('.log', '.bak', '.swp') 
    
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        rel_root = os.path.relpath(root, repo_dir)
        
        # Filter files: include all files EXCEPT those with ignored extensions
        relevant_files = [
            f for f in files 
            if not f.endswith(ignore_file_extensions) 
            and not f.startswith('.') # Ignore dotfiles like .gitignore
        ]
        
        if relevant_files:  
            result.append({'dir': rel_root if rel_root != '.' else '', 'files': relevant_files})
    return result



def analyze_repo_structure(repo_dir: str, tree_structure: str) -> str:

    file_tree = json.loads(tree_structure)
    ccg = {}
    
    for item in file_tree:
        # Handle the case where 'dir' might be missing or None
        current_dir = item.get('dir', ''); 
        
        # Ensure 'files' is present and iterable
        if 'files' not in item or not isinstance(item['files'], list):
            continue 
            
        for f in item['files']:
            # Construct the full file path
            if current_dir:
                full_path = os.path.join(repo_dir, current_dir, f)
            else:
                full_path = os.path.join(repo_dir, f)

            analysis = parse_source_file(full_path)
            
            ccg[f] = analysis
            

    return str(ccg) 
    

def parse_source_file(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {'type': 'error', 'message': f'File not found: {file_path}'}
    except Exception as e:
        return {'type': 'error', 'message': f'Error reading file: {e}'}

    if file_path.endswith('.py'):
        try:
            tree = ast.parse(content)
            # Find function and class definitions
            funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            return {'type': 'python', 'funcs': list(set(funcs)), 'classes': list(set(classes))}
        except SyntaxError:
            return {'type': 'python', 'error': 'Parse error', 'funcs': [], 'classes': []}

    elif file_path.endswith('.jac'):
        # Extract walker/node names via simple regex
        walkers = re.findall(r'walker\s+(\w+)', content)
        nodes = re.findall(r'node\s+(\w+)', content)
        return {'type': 'jac', 'walkers': list(set(walkers)), 'nodes': list(set(nodes))}

    return {'type': 'unknown', 'content': content[:500]}



    