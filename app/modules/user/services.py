from fastapi import HTTPException

from app.core.db import get_db


class UserService:

    @staticmethod
    async def get_all_users():
        pool = await get_db()
        async with pool.acquire() as conn:
            sql = "SELECT id, email, name FROM users;"
            rows = await conn.fetch(sql)
            users = [dict(row) for row in rows]
            return users

    @staticmethod
    async def create_user(name: str, email: str, password: str):
        pool = await get_db()
        async with pool.acquire() as conn:
            sql = """
                INSERT INTO users (name, email, password)
                VALUES ($1, $2, $3)
                RETURNING id, name, email;
            """
            row = await conn.fetchrow(sql, name, email, password)
            if not row:
                raise HTTPException(status_code=400, detail="Could not create the user")
            return dict(row)

    @staticmethod
    async def get_user_by_id(user_id: int):
        pool = await get_db()
        async with pool.acquire() as connection:
            sql = "SELECT id, name, email FROM users WHERE id = $1;"
            row = await connection.fetchrow(sql, user_id)
            if not row:
                raise HTTPException(status_code=404, detail="User not found")
            user = dict(row)
            return user

    # @staticmethod
    # async def update_user(user_id: int, name: str, age: int):
    #     """Update a user's information."""
    #     pool = await get_db()
    #     async with pool.acquire() as connection:
    #         sql = """
    #             UPDATE users
    #             SET name = $1, age = $2
    #             WHERE id = $3
    #             RETURNING id, name, age;
    #         """
    #         row = await connection.fetchrow(sql, name, age, user_id)
    #         if not row:
    #             raise HTTPException(status_code=404, detail="User not found")
    #         return row

    # @staticmethod
    # async def delete_user(user_id: int):
    #     """Delete a user by their ID."""
    #     pool = await get_db()
    #     async with pool.acquire() as connection:
    #         sql = "DELETE FROM users WHERE id = $1 RETURNING id;"
    #         row = await connection.fetchrow(sql, user_id)
    #         if not row:
    #             raise HTTPException(status_code=404, detail="User not found")
    #         return {"message": f"User with ID {user_id} has been deleted."}
