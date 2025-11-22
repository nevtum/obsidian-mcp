import frontmatter


class Note:
    def __init__(self, slug, filename, content):
        self.slug = slug
        self.filename = filename.split("/")[-1]  # Strip path, keep only filename
        self.content = content
        self.frontmatter = self._parse_frontmatter(content)

    def _parse_frontmatter(self, content):
        """Extract frontmatter from the content."""
        metadata, _ = frontmatter.parse(content)
        return metadata

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
