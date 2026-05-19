from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from db import conn, cursor
from auth import create_access_token
from security import hash_password, verify_password


app = FastAPI()


@app.get("/listar", status_code=status.HTTP_200_OK)
async def listar_users(request: Request):
    
    query = """
        SELECT * FROM users;
    """
    
    cursor.execute(query)
    
    usuarios = cursor.fetchall()
    
    return usuarios
    


@app.post("/register")
async def criar_users(request: Request):
    
    data = await request.json()
    
    username = data.get("username")
    email = data.get("email")
    incomming_password = data.get("password")
    
    check_username = """
        SELECT * FROM users
        WHERE username = %s;
    """
    
    cursor.execute(check_username, (username,))
    usuario_username = cursor.fetchone()
    
    if usuario_username:
        return JSONResponse(
            content={
                "error": "Username já existe!"
            }, status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    check_email = """
        SELECT * FROM users
        WHERE email = %s;
    """
        
    cursor.execute(check_email, (email,))
    usuario_email = cursor.fetchone()
    
    if usuario_email:
        return JSONResponse(
            content={
                "error": "Email já existe!"
            }, status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    password = hash_password(incomming_password)
    valores = (username, email, password)
    
    query = """
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s);
    """
    
    cursor.execute(query, valores)
    
    conn.commit()
    
    return JSONResponse(
        content={
            "menssage": "Usuario criado com sucesso!",
            "user": {
                "username": username,
                "email": email,
                "password": password
            }
    })
    
@app.post("/login")
async def login_user(request: Request):
    
    data = await request.json()
    
    email = data.get("email")
    password = data.get("password")
    
    query_find_email = """
        SELECT * FROM users
        WHERE email = %s;
    """
    
    cursor.execute(query_find_email, (email,))
    usuario = cursor.fetchone()
    
    if usuario is None:
        return JSONResponse({
            "message": "Email ou senha inválidos"
        }, status_code=status.HTTP_404_NOT_FOUND)
    
    senha_valida = verify_password(password, usuario["password"])
    
    if not senha_valida:
        return JSONResponse({
            "error": "Senha inválida"
        }, status_code=status.HTTP_401_UNAUTHORIZED)
        
            
    token = create_access_token(usuario)
    
    
    return JSONResponse({
        "token": token
    })