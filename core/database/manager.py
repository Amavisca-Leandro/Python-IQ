"""
Database manager with SQLAlchemy for test data management.

This module provides a DatabaseManager class that handles database connections,
session management, and data operations for test automation.
"""

import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from core.config.settings import get_settings


logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database manager with connection pooling and session management.
    
    Features:
    - Connection pooling for performance
    - Context manager for automatic session cleanup
    - Support for both ORM and raw SQL queries
    - Transaction management with automatic rollback
    - Test data isolation and cleanup
    
    Example:
        >>> db_manager = DatabaseManager()
        >>> with db_manager.get_session() as session:
        ...     user = session.query(User).filter(User.id == 1).first()
        ...     print(user.username)
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            connection_string: Database connection string (defaults to settings)
        """
        self.settings = get_settings()
        self.connection_string = connection_string or self.settings.database_url
        
        # Create engine with connection pooling
        self.engine = self._create_engine()
        
        # Create session factory
        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
        
        logger.info(f"DatabaseManager initialized with connection pooling")
    
    def _create_engine(self) -> Engine:
        """
        Create SQLAlchemy engine with optimized settings.
        
        Returns:
            Engine: Configured SQLAlchemy engine
        """
        engine = create_engine(
            self.connection_string,
            poolclass=QueuePool,
            pool_size=self.settings.db_pool_size,
            max_overflow=self.settings.db_max_overflow,
            pool_pre_ping=self.settings.db_pool_pre_ping,
            pool_recycle=self.settings.db_pool_recycle,
            echo=self.settings.db_echo,
            isolation_level=self.settings.db_isolation_level
        )
        
        logger.debug(
            f"Engine created with pool_size={self.settings.db_pool_size}, "
            f"max_overflow={self.settings.db_max_overflow}"
        )
        
        return engine
    
    @contextmanager
    def get_session(self) -> Session:
        """
        Context manager for database sessions with automatic cleanup.
        
        Provides a session that automatically commits on success and
        rolls back on exceptions. Always closes the session when done.
        
        Yields:
            Session: SQLAlchemy session
            
        Example:
            >>> with db_manager.get_session() as session:
            ...     user = User(username="test", email="test@example.com")
            ...     session.add(user)
            ...     # Automatically commits on success
        """
        session = self.session_factory()
        try:
            yield session
            session.commit()
            logger.debug("Session committed successfully")
        except Exception as e:
            session.rollback()
            logger.error(f"Session rolled back due to error: {e}")
            raise
        finally:
            session.close()
            logger.debug("Session closed")
    
    def execute_raw_sql(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute raw SQL query.
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            Any: Query result
            
        Example:
            >>> result = db_manager.execute_raw_sql(
            ...     "SELECT * FROM users WHERE id = :user_id",
            ...     {"user_id": 123}
            ... )
        """
        with self.get_session() as session:
            result = session.execute(text(sql), params or {})
            
            if self.settings.log_db_queries:
                logger.debug(f"Executed SQL: {sql} with params: {params}")
            
            return result
    
    def query_data(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute query and return results as list of dictionaries.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List[Dict[str, Any]]: Query results
            
        Example:
            >>> users = db_manager.query_data(
            ...     "SELECT id, username FROM users WHERE is_active = :active",
            ...     {"active": True}
            ... )
            >>> for user in users:
            ...     print(user['username'])
        """
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            
            # Convert rows to dictionaries
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            
            if self.settings.log_db_queries:
                logger.debug(
                    f"Query returned {len(rows)} rows: {query} "
                    f"with params: {params}"
                )
            
            return rows
    
    def verify_data_exists(
        self,
        model_class: Any,
        **filters
    ) -> bool:
        """
        Verify if data exists in database.
        
        Args:
            model_class: SQLAlchemy model class
            **filters: Filter conditions
            
        Returns:
            bool: True if data exists, False otherwise
            
        Example:
            >>> exists = db_manager.verify_data_exists(
            ...     User,
            ...     username="test_user",
            ...     is_active=True
            ... )
        """
        with self.get_session() as session:
            query = session.query(model_class)
            
            for key, value in filters.items():
                query = query.filter(getattr(model_class, key) == value)
            
            exists = query.first() is not None
            
            logger.debug(
                f"Data exists check for {model_class.__name__} "
                f"with filters {filters}: {exists}"
            )
            
            return exists
    
    def cleanup_by_test_id(self, test_id: str):
        """
        Cleanup test data by test ID.
        
        This method should be implemented based on your test data
        tracking strategy. It's called automatically by fixtures.
        
        Args:
            test_id: Unique test identifier
        """
        logger.info(f"Cleanup requested for test_id: {test_id}")
        # Implementation depends on test data tracking strategy
        # This is a placeholder that will be enhanced by TestDataFactory
    
    def close(self):
        """Close database connections and cleanup resources."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
