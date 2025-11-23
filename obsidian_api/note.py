import frontmatter


class Note:
    def __init__(self, slug, filename, text):
        self.slug = slug
        self.filepath = filename
        self.filename = filename.split("/")[-1]  # Strip path, keep only filename
        self.text = text
        self.frontmatter, self.content = frontmatter.parse(text)

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
