from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union

class ProblemDetail(BaseModel):
    """
    Problem Details for HTTP APIs (RFC 9457)
    https://datatracker.ietf.org/doc/html/rfc9457
    """
    type: str = Field(
        default="about:blank",
        description="A URI reference that identifies the problem type"
    )
    title: str = Field(
        description="A short, human-readable summary of the problem type"
    )
    status: int = Field(
        description="The HTTP status code"
    )
    detail: str = Field(
        description="A human-readable explanation specific to this occurrence of the problem"
    )
    instance: Optional[str] = Field(
        default=None,
        description="A URI reference that identifies the specific occurrence of the problem"
    )
    errors: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Additional errors details, typically for validation errors"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "type": "https://example.com/problems/resource-not-found",
                "title": "Resource Not Found",
                "status": 404,
                "detail": "The requested resource was not found",
                "instance": "/api/v1/books/123e4567-e89b-12d3-a456-426614174000"
            }
        }


def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle generic HTTPException instances
    """
    from fastapi import HTTPException
    
    if isinstance(exc, HTTPException):
        problem = ProblemDetail(
            type=f"https://httpstatuses.com/{exc.status_code}",
            title=get_status_title(exc.status_code),
            status=exc.status_code,
            detail=exc.detail,
            instance=request.url.path
        )
    else:
        # For generic exceptions
        problem = ProblemDetail(
            type="about:blank",
            title="Internal Server Error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc) or "An unexpected error occurred",
            instance=request.url.path
        )
    
    return JSONResponse(
        status_code=problem.status,
        content=problem.model_dump(exclude_none=True)
    )


def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle validation errors for request data
    """
    errors = []
    for error in exc.errors():
        # Extract field and location information
        loc = error.get("loc", [])
        field = loc[-1] if loc else None
        location = loc[0] if loc else None
        
        errors.append({
            "field": field,
            "location": location,
            "msg": error.get("msg", ""),
            "type": error.get("type", "")
        })
    
    problem = ProblemDetail(
        type="https://errors.example.com/validation-error",
        title="Validation Error",
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="The request data failed validation",
        instance=request.url.path,
        errors=errors
    )
    
    return JSONResponse(
        status_code=problem.status,
        content=problem.model_dump(exclude_none=True)
    )


def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle 404 Not Found errors
    """
    problem = ProblemDetail(
        type="https://httpstatuses.com/404",
        title="Not Found",
        status=status.HTTP_404_NOT_FOUND,
        detail="The requested resource was not found",
        instance=request.url.path
    )
    
    return JSONResponse(
        status_code=problem.status,
        content=problem.model_dump(exclude_none=True)
    )


def get_status_title(status_code: int) -> str:
    """
    Get a human-readable title for a status code
    """
    titles = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        409: "Conflict",
        422: "Unprocessable Entity",
        429: "Too Many Requests",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable"
    }
    
    return titles.get(status_code, "Unknown Error") 