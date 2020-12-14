import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import image

if __name__ == '__main__':
    strawberry = image.Image(Path(__file__).resolve().parent.joinpath('media/strawberry.png'))
    sys.stdout.write(str(strawberry.draw()))

    lexi = image.Image(Path(__file__).resolve().parent.joinpath('media/lexi.jpg'))
    sys.stdout.write(str(lexi.draw(h=40)))
