import sys
from textnode import TextType
from textnode import TextNode

def main() -> int:
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

    print(node)

if __name__ == '__main__':
    sys.exit(main())
