"""
app/services/comment_validation.py

Validates comment parent linkage (task XOR project).
"""
from typing import Optional

def validate_comment_parents(
    *,
    task_id: Optional[int],
    project_id: Optional[int],
) -> None:
    has_task = task_id is not None
    has_project = project_id is not None
    if has_task == has_project:
        raise ValueError("Comment must reference exactly one of task_id or project_id.")
