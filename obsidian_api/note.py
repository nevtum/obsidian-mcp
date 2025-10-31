class Note:
    def __init__(self, slug, filename, content):
        self.slug = slug
        self.filename = filename.split("/")[-1]  # Strip path, keep only filename
        self.content = content
        self.frontmatter = self._parse_frontmatter(content)

    def _parse_frontmatter(self, content):
        """Extract frontmatter from the content."""
        frontmatter_lines = []
        in_frontmatter = False

        for line in content.splitlines():
            if line.strip() == "---":
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter:
                frontmatter_lines.append(line.strip())

        return self._parse_key_value_pairs(frontmatter_lines)

    def _parse_key_value_pairs(self, lines):
        """Convert frontmatter lines into a dictionary."""
        pairs = {}
        for line in lines:
            key, value = line.split(":", 1)
            pairs[key.strip()] = self._parse_value(value.strip())
        return pairs

    def _parse_value(self, value):
        """Parse values into appropriate types."""
        if value.startswith("[") and value.endswith("]"):
            return [tag.strip() for tag in value[1:-1].split(",")]
        return value

    def extract_links(self):
        """Extract links from the note content."""
        import re

        return re.findall(r"\[\[(.*?)\]\]", self.content)

    def as_json(self):
        return {
            "slug": self.slug,
            "content": self.content,
            "frontmatter": self.frontmatter,
        }
