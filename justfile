default: build

build:
    ./build.sh

serve:
    ./build.sh && zola serve

# Regenerate /photos data (zola serve picks up the change automatically)
photos:
    uv run scripts/photos.py

clean:
    rm -rf public content/_git-dates.json content/_photos.json image-meta.json
