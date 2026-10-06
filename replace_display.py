import json
from pathlib import Path

path = Path("student_analytics.ipynb")
notebook = json.loads(path.read_text(encoding="utf-8"))
for cell in notebook["cells"]:
    source = "".join(cell.get("source", []))
    if "display(df.head(5))" in source:
        cell["source"] = [
            line.replace("display(df.head(5))", "print(df.head(5).to_string(index=False))")
            for line in cell["source"]
        ]
        break
else:
    raise RuntimeError("Notebook preview cell not found")

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("Replaced Jupyter-only preview display with portable text output.")
