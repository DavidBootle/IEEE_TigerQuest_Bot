import tomllib

with open('auth.toml', 'rb') as f:
    settings = tomllib.load(f)