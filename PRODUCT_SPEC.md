### Project Overview
The goal of this project is to develop a read-only API that interacts with a collection of markdown notes stored in an Obsidian vault. The API will handle the reading and searching of notes and support functionality for detecting changes in the notes, allowing for a framework suitable for use in agentic AI Model Context Protocol (MCP) servers.

### Table of Contents
1. [Functional Requirements](#functional-requirements)
   - [Reading Notes](#reading-notes)
   - [Finding Links](#finding-links)
   - [Finding Relevant Notes](#finding-relevant-notes)
2. [Note Structure](#note-structure)
3. [Change Detection](#change-detection)
4. [Technologies Used](#technologies-used)
5. [Assumptions and Constraints](#assumptions-and-constraints)

### Functional Requirements

#### Reading Notes
- The API must be able to read markdown files (.md) from a specified directory representing the Obsidian vault.
- Notes should be represented as instances of a `Note` class, initialized with:
  - `filename`: The name of the markdown file (slug).
  - `content`: The content of the markdown file.
  - `frontmatter`: An optional dictionary containing metadata stored in YAML format.

#### Finding Links
- Each `Note` instance must provide functionality to extract links in the format `[[link-name]]` from its content.
- The extracted links must be returned as a unique list of slugs that represent other notes.
- The API must implement a `find_ancestors(slug, max_hops)` method to find notes that can be linked back to the current note within a specified number of hops.

#### Finding Relevant Notes
- The API must implement a breadth-first search (BFS) algorithm to find relevant notes within a specified number of hops.
- The function should take the starting note slug, maximum hops, and character limit for content summaries:
  - Return a JSON-like structure containing:
    - `filename`: Name of the note
    - `contents_summary`: A summary of the note’s content limited to a specified character count.
    - `distance`: The number of hops from the starting note.

### Note Structure
- Markdown files must be structured with optional frontmatter:
  - Frontmatter should be enclosed in triple dashes (`---`) at the top of the file.
  - The content of the note follows the frontmatter after the second occurrence of `---`.
  - Example structure:
    ```markdown
    ---
    title: About Me
    tags: [personal, introduction]
    ---

    This is a note about myself. You can find more in [[projects]] and [[hobbies]].
    ```

### Change Detection
- The API must monitor the notes directory for file system changes (creation, deletion, modification) using the `watchdog` library.
- The system must implement handlers for:
  - **Creation**: Add new notes to the repository upon file creation.
  - **Modification**: Update the content of existing notes when the markdown file is modified.
  - **Deletion**: Remove notes from the repository upon file deletion.

### Technologies Used
- **Python**: Primary programming language for the API development.
- **Watchdog**: Library for monitoring file system events.
- **YAML**: For parsing frontmatter stored in markdown files.

### Assumptions and Constraints
- All markdown files in the specified directory are expected to follow the defined structure and conventions.
- The filenames (slugs) of notes are unique within the vault, but not necessarily in known directories.
- The API is designed for read-only use cases, focusing on fetching and processing existing notes without enabling write capabilities.

### Conclusion
This specification outlines the requirements for a read-only API to manage markdown notes within an Obsidian vault. The designed functionality supports both basic reading operations and enhanced capabilities for navigating and summarizing notes, with a particular emphasis on future adaptability for more extensive agentic AI applications.
