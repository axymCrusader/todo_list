from fastapi import HTTPException, status

task_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)

task_type_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task type not found"
)

not_task_owner = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not the task owner"
)
