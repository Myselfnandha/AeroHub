import importlib.machinery
import importlib.util
from pathlib import Path
import sys

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

p = root / 'MovieSongDownloader' / 'MovieSongDownloader.py'
loader = importlib.machinery.SourceFileLoader('movieapp', str(p))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)

print('app', mod.app)
api = getattr(mod.app, '_api', None)
print('api type', type(api))
print('has get', hasattr(api, 'get'))
print('has add_route', hasattr(api, 'add_route'))
print('dir get', [name for name in dir(api) if 'get' in name.lower()])
