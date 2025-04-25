from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import uuid
import time
from contextvars import ContextVar
from app.core.logging import get_logger

# Context variable to store request ID for the current request context
request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")

# Get the current request ID from the context variable
def get_request_id() -> str:
    return request_id_ctx_var.get()

logger = get_logger(__name__)

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds a correlation ID to each request.
    
    This correlation ID can be used to track a request across multiple services
    and is accessible throughout the request lifecycle.
    """
    
    def __init__(
        self,
        app: ASGIApp,
        header_name: str = "X-Correlation-ID",
        force_new_uuid: bool = False,
        validate_uuid: bool = True
    ):
        super().__init__(app)
        self.header_name = header_name
        self.force_new_uuid = force_new_uuid
        self.validate_uuid = validate_uuid
    
    async def dispatch(self, request: Request, call_next):
        # Try to get the correlation ID from the request headers
        correlation_id = request.headers.get(self.header_name)
        
        # Generate a new UUID if:
        # - No correlation ID was passed
        # - We're configured to always generate a new ID
        # - The passed ID is not a valid UUID (if validation is enabled)
        if (
            correlation_id is None 
            or self.force_new_uuid 
            or (self.validate_uuid and not self._is_valid_uuid(correlation_id))
        ):
            correlation_id = str(uuid.uuid4())
        
        # Store the correlation ID in the request state
        request.state.correlation_id = correlation_id
        
        # Store the correlation ID in the context variable
        token = request_id_ctx_var.set(correlation_id)
        
        # Log the request with correlation ID
        logger.info(
            f"Request started | Correlation ID: {correlation_id} | "
            f"{request.method} {request.url.path}"
        )
        
        # Measure request processing time
        start_time = time.time()
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Add the correlation ID to the response headers
            response.headers[self.header_name] = correlation_id
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log the response with correlation ID
            logger.info(
                f"Request completed | Correlation ID: {correlation_id} | "
                f"{request.method} {request.url.path} | "
                f"Status: {response.status_code} | Time: {process_time:.3f}s"
            )
            
            return response
        except Exception as e:
            # Log the exception with correlation ID
            logger.error(
                f"Request failed | Correlation ID: {correlation_id} | "
                f"{request.method} {request.url.path} | {str(e)}"
            )
            raise
        finally:
            # Reset the context variable token
            request_id_ctx_var.reset(token)
    
    def _is_valid_uuid(self, uuid_str: str) -> bool:
        """
        Check if a string is a valid UUID
        """
        try:
            uuid_obj = uuid.UUID(uuid_str)
            return str(uuid_obj) == uuid_str
        except (ValueError, AttributeError):
            return False


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds timing information to each request.
    
    This middleware measures how long each request takes to process
    and adds this information to response headers.
    """
    
    async def dispatch(self, request: Request, call_next):
        # Measure request processing time
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add timing header (in milliseconds)
        response.headers["X-Process-Time-Ms"] = str(int(process_time * 1000))
        
        return response 